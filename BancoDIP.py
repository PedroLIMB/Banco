import mysql.connector
from tkinter import *
import customtkinter
from PIL import Image
import os

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

    # Criar janela
    janela = customtkinter.CTk()
    janela.geometry("700x400")
    janela.title("BancoDIP")

    # Customizando janela no geral
    customtkinter.set_appearance_mode('Light')
    esquerdo = customtkinter.CTkFrame(master=janela, width=340, height=400, fg_color="#192042")
    esquerdo.place(x=-10, y=0)

    # Adição elementos
    logo = os.path.join(os.path.dirname(__file__), 'Logo/Logo.png')
    imagem = customtkinter.CTkImage(light_image=Image.open(logo))
    label_logo = customtkinter.CTkLabel(master=esquerdo, image=imagem, text="")
    

    nomebanco = customtkinter.CTkLabel(janela, text="Banco DIP")
    usuario = customtkinter.CTkEntry(janela, placeholder_text="Usuario")
    email = customtkinter.CTkEntry(janela, placeholder_text="Email")
    senha = customtkinter.CTkEntry(janela, placeholder_text="Senha", show="*")
    confirmarsenha = customtkinter.CTkEntry(janela, placeholder_text="Confirmar Senha", show="*")
    cadastrar = customtkinter.CTkButton(janela, text="Cadastrar")
    login = customtkinter.CTkLabel(janela, text="Login")

    # Customização dos elementos
    label_logo.place(x=-87, y=-45)
    imagem.configure(size=(500, 500))

    nomebanco.place(x=465, y=35)
    nomebanco.configure(font=("Roboto", 22, "bold"))

    usuario.place(x=370, y=90)
    usuario.configure(font=("Roboto", 16), width=300, height=45, border_width=0)

    email.place(x=370, y=140)
    email.configure(font=("Roboto", 16), width=300, height=45, border_width=0)

    senha.place(x=370, y=190)
    senha.configure(font=("Roboto", 16), width=300, height=45, border_width=0)

    confirmarsenha.place(x=370, y=240)
    confirmarsenha.configure(font=("Roboto", 16), width=300, height=45, border_width=0)

    cadastrar.place(x=370, y=290)
    cadastrar.configure(font=("Roboto", 16), width=300, height=45, fg_color="#192042")

    login.place(x=370, y=340)
    login.configure(font=("Roboto", 16), width=300, height=45)

    janela.mainloop()
