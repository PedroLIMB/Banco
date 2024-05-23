from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'SECRETO'

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancodip.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definição do modelo de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    saldo = db.Column(db.Numeric, nullable=False, default=0.0)
    limite_cheque_especial = db.Column(db.Numeric, nullable=False, default=0.0)

@app.route("/")
def cadastro_pagina():
    return render_template("cadastro.html")

@app.route("/processar_cadastro", methods=["POST"])
def processar_cadastro():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    confirmar_senha = request.form["cSenha"]
    saldo_inicial = request.form.get("depositoInicial")

    if senha != confirmar_senha:
        flash("As senhas não coincidem.")
        return redirect(url_for("cadastro_pagina"))

    if not saldo_inicial or Decimal(saldo_inicial) <= 0:
        flash("Por favor, insira um saldo inicial válido.")
        return redirect(url_for("cadastro_pagina"))

    if Usuario.query.filter_by(email=email).first():
        flash("Este endereço de e-mail já está em uso. Por favor, escolha outro.")
        return redirect(url_for("cadastro_pagina"))

    hashed_senha = generate_password_hash(senha, method='pbkdf2:sha256')
    limite_cheque_especial = Decimal(saldo_inicial) * 4
    novo_usuario = Usuario(nome=nome, email=email, senha=hashed_senha, saldo=saldo_inicial, limite_cheque_especial=limite_cheque_especial)
    
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for("login_pagina"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao cadastrar usuário: {str(e)}")
        return redirect(url_for("cadastro_pagina"))

@app.route("/login")
def login_pagina():
    return render_template("login.html")

@app.route("/processar_login", methods=["POST"])
def processar_login():
    email = request.form["email"]
    senha = request.form["senha"]

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        session['email'] = email
        flash("Login bem-sucedido!")
        return redirect(url_for("index_pagina"))
    else:
        flash("Email ou senha incorretos.")
        return redirect(url_for("login_pagina"))

@app.route("/index")
def index_pagina():
    if 'email' not in session:
        return redirect(url_for('login_pagina'))

    return render_template("index.html")

@app.route("/obter_saldo_e_limite", methods=["GET"])
def obter_saldo_e_limite():
    if 'email' not in session:
        return jsonify(success=False, message="Você precisa estar logado para obter o saldo e o limite de cheque especial.")
    
    usuario = Usuario.query.filter_by(email=session['email']).first()

    if not usuario:
        return jsonify(success=False, message="Usuário não encontrado.")

    return jsonify(success=True, saldo=str(usuario.saldo), limite_cheque_especial=str(usuario.limite_cheque_especial))


@app.route("/processar_saque", methods=["POST"])
def processar_saque():
    if 'email' not in session:
        return jsonify(success=False, message="Você precisa estar logado para realizar saques.")
    
    data = request.get_json()
    valor = Decimal(data["valor"])

    if valor <= 0:
        return jsonify(success=False, message="O valor do saque deve ser maior que zero.")

    usuario = Usuario.query.filter_by(email=session['email']).first()

    if valor > usuario.saldo + usuario.limite_cheque_especial:
        return jsonify(success=False, message="Saldo e limite de cheque especial insuficientes para o saque.")

    usuario.saldo -= valor
    db.session.commit()

    return jsonify(success=True, saldo=str(usuario.saldo))

@app.route("/processar_deposito", methods=["POST"])
def processar_deposito():
    if 'email' not in session:
        return jsonify(success=False, message="Você precisa estar logado para realizar depósitos.")
    
    data = request.get_json()
    valor = Decimal(data["valor"])

    if valor <= 0:
        return jsonify(success=False, message="O valor do depósito deve ser maior que zero.")

    usuario = Usuario.query.filter_by(email=session['email']).first()
    usuario.saldo += valor
    db.session.commit()

    return jsonify(success=True, saldo=str(usuario.saldo))

@app.route("/processar_transferencia", methods=["POST"])
def processar_transferencia():
    if 'email' not in session:
        return jsonify(success=False, message="Você precisa estar logado para realizar transferências.")
    
    data = request.get_json()
    valor = Decimal(data["valor"])
    destinatario_email = data["destinatario"]

    if valor <= 0:
        return jsonify(success=False, message="O valor da transferência deve ser maior que zero.")

    remetente = Usuario.query.filter_by(email=session['email']).first()

    if valor > remetente.saldo + remetente.limite_cheque_especial:
        return jsonify(success=False, message="Saldo e limite de cheque especial insuficientes para a transferência.")

    destinatario = Usuario.query.filter_by(email=destinatario_email).first()

    if not destinatario:
        return jsonify(success=False, message="O destinatário não existe.")

    remetente.saldo -= valor
    destinatario.saldo += valor
    db.session.commit()

    return jsonify(success=True, saldo=str(remetente.saldo), limite_cheque_especial=str(remetente.limite_cheque_especial))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
