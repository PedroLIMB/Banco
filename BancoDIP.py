import sqlite3
from tkinter import *
import customtkinter
from PIL import Image
import os
# Bibliotecas necessarias para o codigo rodar
# pip install pillow
# pip install customtkinter


class conta():
    def __init__(self, titular, email, saldo, cheque_especial):
        self.titular = titular
        self.email = email
        self.saldo = saldo
        self.cheque_especial = cheque_especial
