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

def tampilkan(buku):
    if not buku:
        print("belum ada buku")
        return
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Judul","Penulis", "harga", "Stok"]
    for item in buku:
        tabel.add_row(
            [
                item["id"], item["judul"], item["penulis"], item["harga"], item["stok"]
            ]
        )
    print(tabel) 

def tambah_buku(buku):
    while True:
        print("=== Tambah Buku ===")
        judul = input("Masukkan judul buku: ")
        if judul == "selesai":
            break 
        else:
            penulis = input("Masukkan nama penulis: ")
            harga = input("Masukkan Harga Sewa: Rp")
            stok = input("Masukkan stok: ")
        id_baru = buku[-1]["id"] + 1 if buku else 1
        buku.append (
            {
                "id":id_baru, "judul": judul, "penulis": penulis, "harga": harga, "stok": stok
            }
        )
        simpan(file_buku, buku)

def ubah_buku(buku):
    tampilkan(buku)
    while True:
        print("Ketik selesai jika tidak ingin mengubah lagi")
        ubah =  input("Masukkan id buku yang ingin di ubah: ")
        if ubah == "selesai":
            break
        else:
            buku_dipilih = None
            for item in buku:
                if item["id"] == int(ubah):
                    buku_dipilih = item
            if buku_dipilih is None:
                print("Buku tidak ditemukan")
                continue
            buku_dipilih["judul"] = input("Masukkan Judul: ")
            buku_dipilih["penulis"] = input("Masukkan nama penulis: ")
            buku_dipilih["harga"] = input("Masukkan harga sewa: Rp")
            buku_dipilih["stok"] = input("Masukkan stok: ")

            simpan(file_buku, buku)
            print("data telah diubah")
            
def hapus_buku(buku):
    while True:
        tampilkan(buku)
        hapus = input("Masukkan ID buku yang ingin di hapus")
        if hapus == "selesai":
            break
        else:
            buku_dipilih = None
            for item in buku:
                if item["id"] == int(hapus):
                    buku_dipilih = item
            if buku_dipilih is None:
                print("Buku tidak ditemukan")
            else:
                buku.remove(buku_dipilih)
                simpan(file_buku, buku)
                print("buku dihapus")

def menu_admin(buku):
    while True:
        print("=== Menu Admin===")
        print("1. Lihat Buku")
        print("2. Tambah Buku")
        print("3. Ubah Buku")
        print("4. Hapus Buku")
        print("5. Logout")

        pilihan = input("Masukkan Pilihanmu: ")
        if pilihan == "1":
            tampilkan(buku)
        elif pilihan == "2":
            tambah_buku(buku)
        elif pilihan == "3":
            ubah_buku(buku)
        elif pilihan == "4":
            hapus_buku(buku)
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak ada")

def menu_user(buku):
    while True:
        print("=== Menu User===")
        print("1. Lihat Buku")
        print("2. Logout")

        pilihan = input("Masukkan Pilihanmu: ")
        if pilihan == "1":
            tampilkan(buku)
        elif pilihan == "2":
            break
        else:
            print("Pilihan tidak ada")

user = buka(file_user)
buku = buka(file_buku)
while True:
    print("=== Menu Utama===")
    print("1. Login")
    print("2. Registrasi")
    print("3. Logout")

    pilihan = input("Masukkan Pilihanmu: ")
    if pilihan == "1":
        akun = login(user)
        if akun is None:
            continue
        elif akun["role"] == "admin":
            menu_admin(buku)
        else:
            menu_user(buku)
    elif pilihan == "2":
        registrasi(user)
    elif pilihan == "3":
        break
    else:
        print("Pilihan tidak ada")
