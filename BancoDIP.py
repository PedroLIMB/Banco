import mysql.connector
import tkinter
import customtkinter

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

#Arrumar design
class Inteface():

    janela = customtkinter.CTk()
    janela.geometry("700x350")

    nomebanco = customtkinter.CTkLabel(janela, text="Banco DPI")
    nomebanco.pack(padx=10, pady=10)
    nomebanco.configure(font=("Roboto", 20, "bold"))

    usuario = customtkinter.CTkEntry(janela, placeholder_text="Usuario")
    usuario.pack(padx=10, pady=10)
    
    email = customtkinter.CTkEntry(janela, placeholder_text="Email")
    email.pack(padx=10, pady=10)

    senha = customtkinter.CTkEntry(janela, placeholder_text="Senha", show="*")
    senha.pack(padx=10, pady=10)

    confirmarsenha = customtkinter.CTkEntry(janela, placeholder_text="Confirmar Senha", show="*")
    confirmarsenha.pack(padx=10, pady=10)

    janela.mainloop()