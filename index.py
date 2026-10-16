import os
import json
import time
import pwinput
from prettytable import PrettyTable 

file_user = "user.json"
file_buku = "buku.json"

os.system('cls')

def buka(nama_file):
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {nama_file} tidak di temukan")
        return[]

def simpan(nama_file, data):
     with open(nama_file, "w", encoding="utf-8") as f:
         json.dump(data, f, indent=4)

def registrasi(user):
    print("=== Registrasi ===")
    username = input("masukkan username: ")
    password = pwinput.pwinput ("Masukkan password: ")
    user.append({"username": username, "password": password, "role": "user"})
    simpan(file_user, user)
    print("berhasil registrasi! silahkan login")

def login(user):
    print("=== LOGIN ===")
    username  = input("masukkan username: ")
    password = pwinput.pwinput ("masukkan password: ")
    for i in user:
        if i["username"] == username and i["password"] == password:
            return i
    if user and user["password"] == password:
        print(f"Login berhasil!")
    return None
