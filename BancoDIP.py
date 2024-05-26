import customtkinter
from PIL import Image
import os
import requests
import json
from tkinter import CENTER, simpledialog

linkFirebase = 'https://bancodip-cb201-default-rtdb.firebaseio.com/'

# dados = {'nome': 'pedro', 'email': 'pedro@gmail.com', 'senha': '12', 'saldo': '1000', 'cheque_especial': '4000'}
# inserirDados = requests.post('{}.json'.format(linkFirebase), json.dumps(dados))
# print(inserirDados)
#print(inserirDados.text)


# dados = {'nome': 'bluezão'}
# inserirDados = requests.patch('{}usuario/-NyfQ3u3U71FOawOTN7r/.json'.format(linkFirebase), json.dumps(dados))
# print(inserirDados)
# print(inserirDados.text)


# dados = {'nome': 'pedro', 'email': 'pedro@gmail.com', 'senha': '12', 'saldo': '1000', 'cheque_especial': '4000'}
# inserirDados = requests.get('{}.json'.format(linkFirebase), json.dumps(dados))
# print(inserirDados)
# print(inserirDados.text)


# Classe para representar uma conta
class Conta:
    def __init__(self, id, titular, email, senha, saldo, cheque_especial):
        self.id = id
        self.titular = titular
        self.email = email
        self.senha = senha
        self.saldo = saldo
        self.cheque_especial = cheque_especial

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if self.saldo + self.cheque_especial >= valor:
            if self.saldo >= valor:
                self.saldo -= valor
            else:
                valor_excedente = valor - self.saldo
                self.saldo = 0
                self.cheque_especial -= valor_excedente
        else:
            print("Saldo insuficiente.")

    def consultar_saldo(self):
        return self.saldo, self.cheque_especial


class Banco:
    @staticmethod
    def registrar():
        usuarios = {}

        usuarioGet = usuario.get()
        emailGet = email.get()
        senhaGet = senha.get()
        saldoGet = saldoinicial.get()

        if float(saldoGet) <= 0:
            print("Passa o dinheiro e faz o L")
        else:
            usuarios['nome'] = usuarioGet
            usuarios['email'] = emailGet
            usuarios['senha'] = senhaGet
            usuarios['saldo'] = saldoGet
            usuarios['cheque_especial'] = float(saldoGet) * 4
            inserirDados = requests.post('{}/usuario/.json'.format(linkFirebase), json.dumps(usuarios))
            print(inserirDados)
            print(inserirDados.text)

    @staticmethod
    def login():
        emailGet = email_login.get()
        senhaGet = senha_login.get()

        pegarValores = requests.get('{}/usuario/.json'.format(linkFirebase))
        print(pegarValores)
        pegarValoresDic = pegarValores.json()

        for id_usuario in pegarValoresDic:
            email_db = pegarValoresDic[id_usuario]['email']
            senha_db = pegarValoresDic[id_usuario]['senha']
            nome_db = pegarValoresDic[id_usuario]['nome']
            saldo_db = float(pegarValoresDic[id_usuario]['saldo'])
            cheque_especial_db = float(pegarValoresDic[id_usuario]['cheque_especial'])
            if emailGet == email_db and senhaGet == senha_db:
                usuario_info = (id_usuario, nome_db, email_db, senha_db, saldo_db, cheque_especial_db)
                Interface.janela_principal(usuario_info)
                return
        print("Email ou senha incorretos")


# Classe para a interface do usuário
class Interface:
    @staticmethod
    def tela_login():
        janela_login = customtkinter.CTkToplevel()
        janela_login.geometry("700x400")
        janela_login.title("BancoDIP")

        # Customizando janela no geral
        direito = customtkinter.CTkFrame(master=janela_login, width=340, height=400, fg_color="#192042")
        direito.place(x=360, y=0)

        # Adição de elementos
        logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
        imagem = customtkinter.CTkImage(light_image=Image.open(logo))
        label_logo = customtkinter.CTkLabel(master=direito, image=imagem, text="")
        nomebanco = customtkinter.CTkLabel(janela_login, text="Banco DIP")
        global email_login, senha_login
        email_login = customtkinter.CTkEntry(janela_login, placeholder_text="Email")
        senha_login = customtkinter.CTkEntry(janela_login, placeholder_text="Senha", show="*")
        login_button = customtkinter.CTkButton(janela_login, text="Login", command=Banco.login)

        # Customização dos elementos
        label_logo.place(x=-87, y=-45)
        imagem.configure(size=(500, 500))

        nomebanco.place(x=140, y=80)
        nomebanco.configure(font=("Roboto", 22, "bold"))

        email_login.place(x=40, y=150)
        email_login.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
        senha_login.place(x=40, y=200)
        senha_login.configure(font=("Roboto", 16), width=300, height=38, border_width=0)

        login_button.place(x=40, y=250)
        login_button.configure(font=("Roboto", 16), width=300, height=38, fg_color="#192042")

    @staticmethod
    def tela_cadastro():
        def janela_cadastro():
            # Criando janela de cadastro
            janela_cadastro = customtkinter.CTkToplevel()
            janela_cadastro.geometry("700x400")
            janela_cadastro.title("BancoDIP")

            # Customizando janela no geral
            direito = customtkinter.CTkFrame(master=janela_cadastro, width=340, height=400, fg_color="#192042")
            direito.place(x=360, y=0)

            # Adição de elementos
            logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
            imagem = customtkinter.CTkImage(light_image=Image.open(logo))
            label_logo = customtkinter.CTkLabel(master=direito, image=imagem, text="")
            nomebanco = customtkinter.CTkLabel(janela_cadastro, text="Banco DIP")
            global usuario, email, senha, confirmarsenha, saldoinicial
            usuario = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Usuario")
            email = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Email")
            senha = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Senha", show="*")
            confirmarsenha = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Confirmar Senha", show="*")
            saldoinicial = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Insira um saldo inicial")
            cadastrar_button = customtkinter.CTkButton(janela_cadastro, text="Registrar-se", command=Banco.registrar)
            login_button = customtkinter.CTkButton(janela_cadastro, text="Fazer Login", command=Interface.tela_login)

            # Customização dos elementos
            label_logo.place(x=-87, y=-45)
            imagem.configure(size=(500, 500))

            nomebanco.place(x=140, y=80)
            nomebanco.configure(font=("Roboto", 22, "bold"))

            usuario.place(x=40, y=150)
            usuario.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
            email.place(x=40, y=200)
            email.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
            senha.place(x=40, y=250)
            senha.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
            confirmarsenha.place(x=40, y=300)
            confirmarsenha.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
            saldoinicial.place(x=40, y=350)
            saldoinicial.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
            cadastrar_button.place(x=40, y=400)
            cadastrar_button.configure(font=("Roboto", 16), width=300, height=38, fg_color="#192042")

            login_button.place(x=40, y=450)
            login_button.configure(font=("Roboto", 14), width=300, height=38, fg_color="#192042")

        janela_cadastro()

    @staticmethod
    def janela_principal(usuario):
        # Criando janela principal
        janela_principal = customtkinter.CTkToplevel()
        janela_principal.geometry("1000x650")
        janela_principal.title("BancoDIP")

        # Customizando janela no geral
        header = customtkinter.CTkFrame(master=janela_principal, width=1000, height=200, fg_color="white")
        header.place(x=0, y=0)
        frame_info = customtkinter.CTkFrame(master=janela_principal, width=1000, height=100, fg_color="#192042")
        frame_info.place(x=0, y=200)
        frame_transacoes = customtkinter.CTkFrame(master=janela_principal, width=1000, height=300, fg_color="#192042")
        frame_transacoes.place(x=0, y=300)

        # Adição de elementos
        logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
        imagem = customtkinter.CTkImage(light_image=Image.open(logo))
        label_logo = customtkinter.CTkLabel(master=header, image=imagem, text="")
        texto_info = customtkinter.CTkLabel(master=frame_info, text=f"Olá, {usuario[1]}!\nSaldo Disponível: R${usuario[4]:.2f}\nCheque Especial: R${usuario[5]:.2f}")

        # Botões de transações
        botao_saque = customtkinter.CTkButton(master=frame_transacoes, text="Saque", command=lambda: Interface.realizar_operacao("saque", usuario))
        botao_deposito = customtkinter.CTkButton(master=frame_transacoes, text="Depósito", command=lambda: Interface.realizar_operacao("deposito", usuario))
        botao_transferencia = customtkinter.CTkButton(master=frame_transacoes, text="Transferência", command=lambda: Interface.realizar_operacao("transferencia", usuario))

        # Customização dos elementos
        label_logo.place(relx=0.5, rely=0.5, anchor=CENTER)
        imagem.configure(size=(300, 300))

        texto_info.configure(font=("Roboto", 20), text_color="white")
        texto_info.place(relx=0.5, rely=0.5, anchor=CENTER)

        botao_saque.configure(font=("Roboto", 18), text_color="#192042", fg_color="white")
        botao_saque.place(relx=0.25, rely=0.5, anchor=CENTER)

        botao_deposito.configure(font=("Roboto", 18), text_color="#192042", fg_color="white")
        botao_deposito.place(relx=0.5, rely=0.5, anchor=CENTER)

        botao_transferencia.configure(font=("Roboto", 18), text_color="#192042", fg_color="white")
        botao_transferencia.place(relx=0.75, rely=0.5, anchor=CENTER)


# Criar janela principal
janela = customtkinter.CTk()
janela.geometry("700x400")
janela.title("BancoDIP")

# Customizando janela no geral
customtkinter.set_appearance_mode('Light')
esquerdo = customtkinter.CTkFrame(master=janela, width=340, height=400, fg_color="#192042")
esquerdo.place(x=-10, y=0)

# Adição de elementos
logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
imagem = customtkinter.CTkImage(light_image=Image.open(logo))
label_logo = customtkinter.CTkLabel(master=esquerdo, image=imagem, text="")
nomebanco = customtkinter.CTkLabel(janela, text="Banco DIP")
usuario = customtkinter.CTkEntry(janela, placeholder_text="Usuario")
email = customtkinter.CTkEntry(janela, placeholder_text="Email")
senha = customtkinter.CTkEntry(janela, placeholder_text="Senha", show="*")
confirmarsenha = customtkinter.CTkEntry(janela, placeholder_text="Confirmar Senha", show="*")
saldoinicial = customtkinter.CTkEntry(janela, placeholder_text="Insira um saldo inicial")
cadastrar = customtkinter.CTkButton(janela, text="Registrar-se", command=Banco.registrar)
login = customtkinter.CTkButton(janela, text="Fazer Login", command=Interface.tela_login)

# Customização dos elementos
label_logo.place(x=-87, y=-45)
imagem.configure(size=(500, 500))
nomebanco.place(x=465, y=15)
nomebanco.configure(font=("Roboto", 22, "bold"))
usuario.place(x=370, y=60)
usuario.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
email.place(x=370, y=110)
email.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
senha.place(x=370, y=160)
senha.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
confirmarsenha.place(x=370, y=210)
confirmarsenha.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
saldoinicial.place(x=370, y=260)
saldoinicial.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
cadastrar.place(x=370, y=310)
cadastrar.configure(font=("Roboto", 16), width=300, height=38, fg_color="#192042")
login.place(x=370, y=350)
login.configure(font=("Roboto", 14), width=300, height=38, fg_color="#192042")

janela.mainloop()
