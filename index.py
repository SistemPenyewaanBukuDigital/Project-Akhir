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

def input_teks(pesan):
    """Input teks, tidak boleh kosong."""
    while True:
        nilai = input(pesan).strip()
        if nilai:
            return nilai
        print("Input tidak boleh kosong")


def input_angka(pesan):
    """Input bilangan bulat, tidak boleh negatif."""
    while True:
        nilai = input(pesan).strip()
        try:
            angka = int(nilai)
        except ValueError:
            print("Input harus berupa angka")
            continue
        if angka < 0:
            print("Angka tidak boleh negatif")
            continue
        return angka


def tanya_lanjut():
    """Return True kalau user mau lanjut, False kalau tidak."""
    while True:
        jawab = input("Apakah masih ingin melanjutkan (y/n)?: ").strip().lower()
        if jawab == "y":
            return True
        elif jawab == "n":
            return False
        print("Pilihan tidak valid")


def cari_buku(buku, id_buku):
    for item in buku:
        if item["id"] == id_buku:
            return item
    return None

def registrasi(user):
    print("=== Registrasi ===")
    while True:
        username = input_teks("Masukkan username: ")
        if username == "":
            print("Username tidak boleh kosong")
            continue
        elif any (u["username"] == username for u in user):
                print("Username sudah dipakai")
        else:
            break
    while True:
        password = pwinput.pwinput ("Masukkan password: ")
        if password == "":
            print("Password tidak boleh kosong")
        else:
            break
        
    user.append({"username": username, "password": password, "role": "user"})
    simpan(file_user, user)
    print("berhasil registrasi! silahkan login")

def login(user):
    print("=== LOGIN ===")
    username  = input("masukkan username: ")
    password = pwinput.pwinput ("masukkan password: ")
    for i in user:
            if i["username"] == username and i["password"] == password:
                print("Login berhasil!")
                return i
    print("Username atau password salah")
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
        judul = input_teks("Masukkan judul buku: ")
        penulis = input_teks("Masukkan nama penulis: ")
        harga = input_angka("Masukkan harga sewa: Rp")
        stok = input_angka("Masukkan stok: ")
        id_baru = max((b["id"] for b in buku), default=0) + 1
        buku.append (
            {
                "id":id_baru, "judul": judul, "penulis": penulis, "harga": harga, "stok": stok
                }
        )
        if simpan(file_buku, buku):
            print("Buku berhasil ditambahkan")
        else:
            buku.pop()
        if not tanya_lanjut():
            break

def ubah_buku(buku):
    tampilkan(buku)
    while True:
        ubah = input("Masukkan id buku yang ingin diubah: ")
        if not ubah.isdigit():
            print("ID harus berupa angka")
            continue

        buku_dipilih = None
        for item in buku:
            if item["id"] == int(ubah):
                buku_dipilih = item
                break

        if buku_dipilih is None:
            print("Buku tidak ditemukan")
            continue

        while True:
            print("\nPilih data yang ingin diubah:")
            print("1. Judul")
            print("2. Penulis")
            print("3. Harga sewa")
            print("4. Stok")
            pilihan = input("Pilihan: ")

            if pilihan == "1":
                buku_dipilih["judul"] = input_teks("Masukkan judul: ")
            elif pilihan == "2":
                buku_dipilih["penulis"] = input_teks("Masukkan nama penulis: ")
            elif pilihan == "3":
                buku_dipilih["harga"] = input_angka("Masukkan harga sewa: Rp")
            elif pilihan == "4":
                buku_dipilih["stok"] = input_angka("Masukkan stok: ")
            elif pilihan == "0":
                break
            else:
                print("Pilihan tidak valid")
                continue

            if simpan(file_buku, buku):
                print("Data berhasil diubah")

        if not tanya_lanjut():
            break

def hapus_buku(buku):
    while True:
        tampilkan(buku)
        hapus = input("Masukkan ID buku yang ingin di hapus: ").strip()
        if not hapus.isdigit():
            print("ID harus berupa angka")
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
        if not tanya_lanjut():
            break

def menu_admin(buku):
    while True:
        print("=== Menu Admin===")
        print("1. Lihat Buku")
        print("2. Tambah Buku")
        print("3. Ubah Buku")
        print("4. Hapus Buku")
        print("5. Logout")

        pilihan = input("Masukkan Pilihanmu: ").strip()
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

        pilihan = input("Masukkan Pilihanmu: ").strip()
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
