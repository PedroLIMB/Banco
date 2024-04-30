import sqlite3
from tkinter import *
import customtkinter
from PIL import Image
import os

# Bibliotecas necessárias para o código rodar
# pip install pillow
# pip install customtkinter

# Conexão com o banco de dados

class Conta():
    def __init__(self, titular, email, senha, saldo, cheque_especial):
        self.titular = titular
        self.email = email
        self.saldo = saldo
        self.cheque_especial = cheque_especial
        
    def depositar(self, valor):
        self.saldo += valor
    
    def sacar(self, valor):
        if self.saldo > 0:
            self.saldo -= valor
        else:
            pass
    
    def consultar_saldo(self):
        return self.saldo


class Banco():
    def __init__(self):
        self.banco = sqlite3.connect("bancoDip.db")
        self.cursor = self.banco.cursor();
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
            self.cursor = self.banco.cursor();
            self.cursor.execute("INSERT INTO banco (titular, email, senha, saldo, cheque_especial) VALUES (?, ?, ?, ?, ?)", (conta.titular, conta.email, conta.senha, conta.saldo, 
                                                                                                                             conta.saldo * 4))
            self.banco.commit()
            self.banco.close()
            
        except sqlite3.Error as err:
            print(err)
            
    def depositar(self, email, valor):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor();
            self.cursor.execute("UPDATE banco SET saldo = saldo + ? where email = ?", (valor, email))
    
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.commit()
            self.banco.close() 
            
    def sacar(self, email, valor):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor();
            
            cheque_especial = self.cursor.execute("SELECT cheque_especial FROM banco WHERE email = ?", (email,))
            saldo = self.cursor.execute("SELECT saldo FROM banco WHERE email = ?", (email,))
            
            if cheque_especial > 0:
                self.cursor.execute("UPDATE banco SET saldo = saldo - ? where email = ?", (valor, email))
            elif saldo <= 0:
                self.cursor.execute("UPDATE banco SET cheque_especial = cheque_especial - ? where email = ?", (valor, email))
            
                
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.commit()
            self.banco.close()
        
    def transferir(self, valor, email, email_transf):
        try:
            self.banco = sqlite3.connect("bancoDip.db")
            self.cursor = self.banco.cursor();
            
            saldo = self.cursor.execute("SELECT saldo FROM banco WHERE email = ?", (email,))
            
            if saldo > 0:
                self.cursor.execute("UPDATE banco SET saldo = saldo + ? where email = ?", (valor, email_transf))
            else:
                pass
            
                
        except sqlite3.Error as err:
            print(err)
        finally:
            self.banco.commit()
            self.banco.close()
            
    
            

class Interface():
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
            login = customtkinter.CTkButton(janela_login, text="Login")
            cadastrar = customtkinter.CTkButton(janela_login, text="Criar Conta")

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

    def janela_principal():
        # Criando janela principal
        janela_principal = customtkinter.CTkToplevel()
        janela_principal.geometry("1000x750")
        janela_principal.title("BancoDIP")

        # Customizando janela no geral
        header = customtkinter.CTkFrame(master=janela_principal, width=1000, height=200, fg_color="#192042")
        header.place(x=0, y=0)
        frame_saque = customtkinter.CTkFrame(master=janela_principal, width=300, height=400, fg_color="#192042")
        frame_saque.place(x=25, y=300)
        frame_deposito = customtkinter.CTkFrame(master=janela_principal, width=300, height=400, fg_color="#192042")
        frame_deposito.place(x=350, y=300)
        frame_transferencia = customtkinter.CTkFrame(master=janela_principal, width=300, height=400, fg_color="#192042")
        frame_transferencia.place(x=675, y=300)

        # Adição de elementos
        logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
        imagem = customtkinter.CTkImage(light_image=Image.open(logo))
        label_logo = customtkinter.CTkLabel(master=header, image=imagem, text="")
        titulo_saque = customtkinter.CTkLabel(master=frame_saque, text="Saque")
        texto_saque = customtkinter.CTkLabel(master=frame_saque, text="Informe um valor para sacar:")
        entry_saque = customtkinter.CTkEntry(master=frame_saque, placeholder_text="Valor")

        # Customização dos elementos
        label_logo.place(x=350, y=-50)
        imagem.configure(size=(300, 300))
        titulo_saque.configure(font=("Roboto", 28), text_color="white")
        titulo_saque.place(x=115, y=30)

        texto_saque.configure(font=("Roboto", 18), text_color="white")
        texto_saque.place(x=35, y=90)

        entry_saque.configure(font=("Roboto", 18))
        entry_saque.place(x=35, y=170)


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
cadastrar = customtkinter.CTkButton(janela, text="Registrar-se", command=Interface.janela_principal)
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
