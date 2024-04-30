import sqlite3
from tkinter import *
import customtkinter
from PIL import Image
import os
# Bibliotecas necessarias para o codigo rodar
# pip install pillow
# pip install customtkinter


class Conta():
    def __init__(self, titular, email, saldo, cheque_especial):
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
                            CREATE TABLE IF NOT EXISTS banco(id INTEGER PRIMARY KEY AUTOINCREMENT, titular VARCHAR(80), email VARCHAR(80), saldo DECIMAL, )
                            
                            
                            
                            ''')