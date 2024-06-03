import customtkinter
from PIL import Image
import os
import requests
import json

linkFirebase = 'https://bancodip-61293-default-rtdb.firebaseio.com/'

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
            self.saldo -= valor
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
        saldoGet = float(saldoinicial.get())

        if saldoGet <= 0:
            print("Saldo inicial deve ser maior que zero.")
        else:
            usuarios['nome'] = usuarioGet
            usuarios['email'] = emailGet
            usuarios['senha'] = senhaGet
            usuarios['saldo'] = saldoGet
            usuarios['cheque_especial'] = saldoGet * 4
            inserirDados = requests.post('{}/usuarios/.json'.format(linkFirebase), json.dumps(usuarios))
            print(inserirDados)
            print(inserirDados.text)

    @staticmethod
    def login():
        emailGet = email_login.get()
        senhaGet = senha_login.get()

        pegarValores = requests.get('{}/usuarios/.json'.format(linkFirebase))
        pegarValoresDic = pegarValores.json()

        global id_usuario
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

    @staticmethod
    def saque():
        valor_saque = float(valor.get())
        pegarValores = requests.get('{}/usuarios/{}.json'.format(linkFirebase, id_usuario))
        usuario = pegarValores.json()

        saldo_db = float(usuario['saldo'])
        cheque_especial_db = float(usuario['cheque_especial'])

        if saldo_db + cheque_especial_db >= valor_saque:
            saldo_db -= valor_saque

            dados = {'saldo': saldo_db}
            requests.patch('{}/usuarios/{}/.json'.format(linkFirebase, id_usuario), json.dumps(dados))
            print(f'Saque de {valor_saque} realizado com sucesso.')
        else:
            print("Saldo insuficiente.")

    @staticmethod
    def deposito():
        valor_deposito = float(valor.get())
        pegarValores = requests.get('{}/usuarios/{}.json'.format(linkFirebase, id_usuario))
        usuario = pegarValores.json()

        saldo_db = float(usuario['saldo'])

        saldo_db += valor_deposito

        dados = {'saldo': saldo_db}
        requests.patch('{}/usuarios/{}/.json'.format(linkFirebase, id_usuario), json.dumps(dados))
        print(f'Depósito de {valor_deposito} realizado com sucesso.')

    @staticmethod
    def transferencia():
        email_destino = email_transferencia.get()
        valor_transferencia = float(valor.get())

        pegarValores = requests.get('{}/usuarios/{}.json'.format(linkFirebase, id_usuario))
        remetente = pegarValores.json()

        saldo_remetente = float(remetente['saldo'])
        cheque_especial_remetente = float(remetente['cheque_especial'])

        if saldo_remetente + cheque_especial_remetente >= valor_transferencia:
            pegarValoresTodos = requests.get('{}/usuarios/.json'.format(linkFirebase))
            pegarValoresDic = pegarValoresTodos.json()

            id_destino = None
            for id_usuario_destino in pegarValoresDic:
                if pegarValoresDic[id_usuario_destino]['email'] == email_destino:
                    id_destino = id_usuario_destino
                    break

            if id_destino:
                pegarValoresDestino = requests.get('{}/usuarios/{}.json'.format(linkFirebase, id_destino))
                destinatario = pegarValoresDestino.json()

                saldo_destinatario = float(destinatario['saldo'])

                saldo_remetente -= valor_transferencia

                dados_remetente = {'saldo': saldo_remetente}
                requests.patch('{}/usuarios/{}/.json'.format(linkFirebase, id_usuario), json.dumps(dados_remetente))

                saldo_destinatario += valor_transferencia
                dados_destinatario = {'saldo': saldo_destinatario}
                requests.patch('{}/usuarios/{}/.json'.format(linkFirebase, id_destino), json.dumps(dados_destinatario))

                print(f'Transferência de {valor_transferencia} realizada com sucesso para {email_destino}.')
            else:
                print("Destinatário não encontrado.")
        else:
            print("Saldo insuficiente.")

    @staticmethod
    def consultar_dados_usuario():
        pegarValores = requests.get('{}/usuarios/{}.json'.format(linkFirebase, id_usuario))
        usuario = pegarValores.json()
        saldo_db = float(usuario['saldo'])
        cheque_especial_db = float(usuario['cheque_especial'])
        return saldo_db, cheque_especial_db

class Interface:
    @staticmethod
    def tela_login():
        janela_login = customtkinter.CTkToplevel()
        janela_login.geometry("700x400")
        janela_login.title("BancoDIP")

        direito = customtkinter.CTkFrame(master=janela_login, width=340, height=400, fg_color="#192042")
        direito.place(x=360, y=0)

        logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
        imagem = customtkinter.CTkImage(light_image=Image.open(logo))
        label_logo = customtkinter.CTkLabel(master=direito, image=imagem, text="")
        nomebanco = customtkinter.CTkLabel(janela_login, text="Banco DIP")
        global email_login, senha_login
        email_login = customtkinter.CTkEntry(janela_login, placeholder_text="Email")
        senha_login = customtkinter.CTkEntry(janela_login, placeholder_text="Senha", show="*")
        login_button = customtkinter.CTkButton(janela_login, text="Login", command=Banco.login)

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
            janela_cadastro = customtkinter.CTkToplevel()
            janela_cadastro.geometry("700x400")
            janela_cadastro.title("BancoDIP")

            direito = customtkinter.CTkFrame(master=janela_cadastro, width=340, height=400, fg_color="#192042")
            direito.place(x=360, y=0)

            logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
            imagem = customtkinter.CTkImage(light_image=Image.open(logo))
            label_logo = customtkinter.CTkLabel(master=direito, image=imagem, text="")
            nomebanco = customtkinter.CTkLabel(janela_cadastro, text="Banco DIP")

            global usuario, email, senha, saldoinicial
            usuario = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Nome")
            email = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Email")
            senha = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Senha", show="*")
            saldoinicial = customtkinter.CTkEntry(janela_cadastro, placeholder_text="Saldo Inicial")
            registrar = customtkinter.CTkButton(janela_cadastro, text="Registrar", command=Banco.registrar)

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
            
            saldoinicial.place(x=40, y=300)
            saldoinicial.configure(font=("Roboto", 16), width=300, height=38, border_width=0)

            registrar.place(x=40, y=350)
            registrar.configure(font=("Roboto", 16), width=300, height=38, fg_color="#192042")

        janela_inicial = customtkinter.CTk()
        janela_inicial.geometry("700x400")
        janela_inicial.title("BancoDIP")

        esquerdo = customtkinter.CTkFrame(master=janela_inicial, width=340, height=400, fg_color="#192042")
        esquerdo.place(x=0, y=0)

        logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
        imagem = customtkinter.CTkImage(light_image=Image.open(logo))
        label_logo = customtkinter.CTkLabel(master=esquerdo, image=imagem, text="")
        nomebanco = customtkinter.CTkLabel(janela_inicial, text="Banco DIP")
        registrar = customtkinter.CTkButton(janela_inicial, text="Cadastrar-se", command=janela_cadastro)
        login = customtkinter.CTkButton(janela_inicial, text="Login", command=Interface.tela_login)

        label_logo.place(x=-87, y=-45)
        imagem.configure(size=(500, 500))

        nomebanco.place(x=475, y=100)
        nomebanco.configure(font=("Roboto", 22, "bold"))

        registrar.place(x=440, y=180)
        registrar.configure(font=("Roboto", 16), width=180, height=38, fg_color="#192042")

        login.place(x=440, y=230)
        login.configure(font=("Roboto", 16), width=180, height=38, fg_color="#192042")

        janela_inicial.mainloop()

    @staticmethod
    def janela_principal(usuario_info):
        global id_usuario, usuario
        id_usuario, nome, email, senha, saldo, cheque_especial = usuario_info
        usuario = Conta(id_usuario, nome, email, senha, saldo, cheque_especial)

        janela_principal = customtkinter.CTk()
        janela_principal.geometry("700x400")
        janela_principal.title("BancoDIP")

        frame = customtkinter.CTkFrame(master=janela_principal, width=680, height=380)
        frame.place(x=10, y=10)

        label_bem_vindo = customtkinter.CTkLabel(master=frame, text=f"Bem-vindo, {nome}!", font=("Roboto", 22, "bold"))
        label_bem_vindo.place(x=10, y=10)

        global valor, email_transferencia
        valor = customtkinter.CTkEntry(master=frame, placeholder_text="Valor")
        email_transferencia = customtkinter.CTkEntry(master=frame, placeholder_text="Email do Destinatário")

        valor.place(x=10, y=50)
        valor.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
        email_transferencia.place(x=10, y=100)
        email_transferencia.configure(font=("Roboto", 16), width=300, height=38, border_width=0)

        botao_saque = customtkinter.CTkButton(master=frame, text="Sacar", command=Banco.saque)
        botao_deposito = customtkinter.CTkButton(master=frame, text="Depositar", command=Banco.deposito)
        botao_transferencia = customtkinter.CTkButton(master=frame, text="Transferir", command=Banco.transferencia)
        botao_consultar = customtkinter.CTkButton(master=frame, text="Consultar Saldo", command=Interface.consultar_saldo)

        botao_saque.place(x=10, y=150)
        botao_saque.configure(font=("Roboto", 16), width=140, height=38, fg_color="#192042")

        botao_deposito.place(x        =160, y=150)
        botao_deposito.configure(font=("Roboto", 16), width=140, height=38, fg_color="#192042")

        botao_transferencia.place(x=10, y=200)
        botao_transferencia.configure(font=("Roboto", 16), width=140, height=38, fg_color="#192042")

        botao_consultar.place(x=160, y=200)
        botao_consultar.configure(font=("Roboto", 16), width=140, height=38, fg_color="#192042")

        # Exibição do saldo e cheque especial
        label_saldo = customtkinter.CTkLabel(master=frame, text=f"Saldo: {saldo}", font=("Roboto", 16))
        label_cheque_especial = customtkinter.CTkLabel(master=frame, text=f"Cheque Especial: {cheque_especial}", font=("Roboto", 16))
        label_saldo.place(x=10, y=250)
        label_cheque_especial.place(x=10, y=280)

        def atualizar_saldo_cheque_especial():
            saldo, cheque_especial = Banco.consultar_dados_usuario()
            label_saldo.configure(text=f"Saldo: {saldo}")
            label_cheque_especial.configure(text=f"Cheque Especial: {cheque_especial}")
            label_saldo.after(1000, atualizar_saldo_cheque_especial)  # Atualiza a cada segundo

        atualizar_saldo_cheque_especial()  # Chama a função para iniciar a atualização automática

        janela_principal.mainloop()

    @staticmethod
    def consultar_saldo():
        saldo, cheque_especial = Banco.consultar_dados_usuario()
        print(f'Saldo: {saldo}')
        print(f'Cheque Especial: {cheque_especial}')

if __name__ == "__main__":
    Interface.tela_cadastro()
