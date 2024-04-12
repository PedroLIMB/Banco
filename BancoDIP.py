import mysql.connector
from tkinter import *
import customtkinter
from PIL import Image
import os
#Bibliotecas necessarias para o codigo rodar
#pip install pillow
#pip install customtkinter

bd = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = bd.cursor()

def criar_bd():
    nome_bd = ("bancodip").lower()

    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(nome_bd))
    cursor.execute("USE {}".format(nome_bd))
    bd.commit()

def criar_tabela():
    nome_tabela = ("tabeladip").lower()

    tabela = '''CREATE TABLE IF NOT EXISTS {} (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                usuario VARCHAR(20) NOT NULL,
                email VARCHAR(45) NOT NULL,
                senha VARCHAR(30) NOT NULL,
                saldo DECIMAL(7,2) NOT NULL)'''.format(nome_tabela)
    cursor.execute(tabela)
    bd.commit()

class Interface():

    def tela_login():
        #Criando janela de login
        janela_login = customtkinter.CTkToplevel()
        janela_login.geometry("700x400")
        janela_login.title("BancoDIP")
        
        #Customizando janela no geral
        direito = customtkinter.CTkFrame(master=janela_login, width=340, height=400, fg_color="#192042")
        direito.place(x=360, y=0)
        
        #Adição de elementos
        logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
        imagem = customtkinter.CTkImage(light_image=Image.open(logo))
        label_logo = customtkinter.CTkLabel(master=direito, image=imagem, text="")
        nomebanco = customtkinter.CTkLabel(janela_login, text="Banco DIP")
        email = customtkinter.CTkEntry(janela_login, placeholder_text="Email")
        senha = customtkinter.CTkEntry(janela_login, placeholder_text="Senha", show="*")
        login = customtkinter.CTkButton(janela_login, text="Login")
        cadastrar = customtkinter.CTkButton(janela_login, text="Criar Conta")
        
        #Customização dos elementos
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
    
    # Criar janela
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
    cadastrar = customtkinter.CTkButton(janela, text="Registrar-se")
    login = customtkinter.CTkButton(janela, text="Fazer Login", command=tela_login)

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
