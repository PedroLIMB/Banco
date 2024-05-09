import sqlite3
from tkinter import *
import customtkinter
from PIL import Image
import os
from tkinter import simpledialog
 
# Classe para representar uma conta
class Conta():
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
 
# Classe para manipular o banco de dados
class Banco():
    def __init__(self):
        self.banco = sqlite3.connect("bancoDip.db")
        self.cursor = self.banco.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS banco(id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titular VARCHAR(80),
                            email VARCHAR(80),
                            senha VARCHAR(24),
                            saldo DECIMAL,
                            cheque_especial DECIMAL)
                            ''')
       
        self.banco.commit()
        self.banco.close()
       
    def criar_conta(self, conta):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor()
            self.cursor.execute("INSERT INTO banco (titular, email, senha, saldo, cheque_especial) VALUES (?, ?, ?, ?, ?)", (conta.titular, conta.email, conta.senha, conta.saldo,
                                                                                                                             conta.cheque_especial))
            self.banco.commit()
            self.banco.close()
           
        except sqlite3.Error as err:
            print(err)
           
    def verificar_login(self, email, senha):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor()
            self.cursor.execute("SELECT * FROM banco WHERE email = ? AND senha = ?", (email, senha))
            usuario = self.cursor.fetchone()
            return usuario
           
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.close()
   
    def depositar(self, email, valor):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor()
            self.cursor.execute("UPDATE banco SET saldo = saldo + ? WHERE email = ?", (valor, email))
            self.banco.commit()
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.close()
   
    def sacar(self, email, valor):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor()
            saldo_atual, cheque_especial = self.cursor.execute("SELECT saldo, cheque_especial FROM banco WHERE email = ?", (email,)).fetchone()
            if saldo_atual + cheque_especial >= valor:
                if saldo_atual >= valor:
                    self.cursor.execute("UPDATE banco SET saldo = saldo - ? WHERE email = ?", (valor, email))
                else:
                    valor_excedente = valor - saldo_atual
                    self.cursor.execute("UPDATE banco SET saldo = 0, cheque_especial = cheque_especial - ? WHERE email = ?", (valor_excedente, email))
                self.banco.commit()
            else:
                print("Saldo insuficiente.")
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.close()
   
    def transferir(self, email_origem, email_destino, valor):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor()
            saldo_atual, cheque_especial = self.cursor.execute("SELECT saldo, cheque_especial FROM banco WHERE email = ?", (email_origem,)).fetchone()
            if saldo_atual + cheque_especial >= valor:
                if saldo_atual >= valor:
                    self.cursor.execute("UPDATE banco SET saldo = saldo - ? WHERE email = ?", (valor, email_origem))
                else:
                    valor_excedente = valor - saldo_atual
                    self.cursor.execute("UPDATE banco SET saldo = 0, cheque_especial = cheque_especial - ? WHERE email = ?", (valor_excedente, email_origem))
                self.cursor.execute("UPDATE banco SET saldo = saldo + ? WHERE email = ?", (valor, email_destino))
                self.banco.commit()
            else:
                print("Saldo insuficiente para transferência.")
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.close()
 
# Classe para a interface do usuário
class Interface():
    @staticmethod
    def tela_login():
        def janela_login():
            # Criando janela de login
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
            email = customtkinter.CTkEntry(janela_login, placeholder_text="Email")
            senha = customtkinter.CTkEntry(janela_login, placeholder_text="Senha", show="*")
            login = customtkinter.CTkButton(janela_login, text="Login", command=lambda: Interface.fazer_login(email.get(), senha.get()))
            cadastrar = customtkinter.CTkButton(janela_login, text="Criar Conta", command=Interface.registrar_conta)
 
            # Customização dos elementos
            label_logo.place(x=-87, y=-45)
            imagem.configure(size=(500, 500))
 
            nomebanco.place(x=140, y=80)
            nomebanco.configure(font=("Roboto", 22, "bold"))
 
            email.place(x=40, y=150)
            email.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
            senha.place(x=40, y=200)
            senha.configure(font=("Roboto", 16), width=300, height=38, border_width=0)
 
            login.place(x=40, y=250)
            login.configure(font=("Roboto", 16), width=300, height=38, fg_color="#192042")
 
            cadastrar.place(x=40, y=290)
            cadastrar.configure(font=("Roboto", 14), width=300, height=38, fg_color="#192042")
 
        janela_login()
 
    @staticmethod
    def janela_principal(usuario):
        def atualizar_saldo():
            banco = Banco()
            saldo_atual, cheque_especial = banco.verificar_login(usuario[2], usuario[3])[4:]
            texto_info.configure(text=f"Olá, {usuario[1]}!\nSaldo Disponível: R${saldo_atual:.2f}\nCheque Especial: R${cheque_especial:.2f}")
            janela_principal.after(1000, atualizar_saldo)  # Atualizar a cada 1 segundo
 
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
 
        # Iniciar atualização do saldo em tempo real
        atualizar_saldo()
 
    @staticmethod
    def registrar_conta():
        titular = usuario.get()
        email_val = email.get()
        senha_val = senha.get()
        saldo_inicial_str = saldoinicial.get()
       
        if saldo_inicial_str:  # Verifica se o campo de saldo inicial não está vazio
            saldo_inicial = float(saldo_inicial_str)
            conta = Conta(None, titular, email_val, senha_val, saldo_inicial, saldo_inicial * 4)
            banco = Banco()
            banco.criar_conta(conta)
            Interface.tela_login()  # Após criar a conta com sucesso, ir para a tela de login
        else:
            print("Por favor, insira um saldo inicial válido.")
 
    @staticmethod
    def fazer_login(email, senha):
        banco = Banco()
        usuario = banco.verificar_login(email, senha)
        if usuario:
            Interface.janela_principal(usuario)
        else:
            print("Credenciais inválidas. Por favor, tente novamente.")
   
    @staticmethod
    def realizar_operacao(tipo_operacao, usuario):
        banco = Banco()
        if tipo_operacao == "saque":
            valor = simpledialog.askfloat("Saque", "Informe o valor do saque:")
            if valor is not None:
                banco.sacar(usuario[2], valor)
        elif tipo_operacao == "deposito":
            valor = simpledialog.askfloat("Depósito", "Informe o valor do depósito:")
            if valor is not None:
                banco.depositar(usuario[2], valor)
        elif tipo_operacao == "transferencia":
            email_destino = simpledialog.askstring("Transferência", "Informe o email de destino:")
            if email_destino:
                valor = simpledialog.askfloat("Transferência", "Informe o valor da transferência:")
                if valor is not None:
                    banco.transferir(usuario[2], email_destino, valor)
 
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
cadastrar = customtkinter.CTkButton(janela, text="Registrar-se", command=Interface.registrar_conta)
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