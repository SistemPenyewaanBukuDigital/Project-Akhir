import csv
import os
import time
import pwinput
from datetime import datetime, timedelta
from prettytable import PrettyTable

# KONSTANTA
FILE_AKUN = 'akun.csv'
FILE_BUKU = 'buku.csv'
FILE_SEWA = 'sewa.csv'
FILE_TRANSAKSI = 'transaksi.csv'
FILE_SALDO = 'saldo.csv'

MIN_SALDO = 10000
MAX_SALDO = 500000
MAX_DURASI = 365

# Validasi akun
MAX_PERCOBAAN_LOGIN = 3
JEDA_BLOKIR_LOGIN = 5 
MIN_NAMA = 4
MIN_SANDI = 6

DETIK_PER_HARI = 86400
FORMAT_TANGGAL = "%Y-%m-%d %H:%M:%S"

ROLE_ADMIN = "admin"
ROLE_PENGGUNA = "pengguna"
DAFTAR_ROLE = (ROLE_ADMIN, ROLE_PENGGUNA)

MENU_AWAL = ("Login", "Daftar Akun Baru", "Keluar")
MENU_ADMIN = (
    "Lihat Daftar Buku",
    "Tambah Buku Baru",
    "Edit Buku",
    "Hapus Buku",
    "Lihat Buku yang Sedang Disewa",
    "Lihat Riwayat Transaksi Semua User",
    "Laporan Ringkas",
    "Keluar",
)
MENU_PENGGUNA = (
    "Lihat Daftar Buku",
    "Sewa Buku",
    "Buku yang Sedang Saya Sewa",
    "Cek Saldo E-money",
    "Top Up Saldo",
    "Riwayat Transaksi Saya",
    "Keluar",
)

FORMAT = {
    "akun": (FILE_AKUN, ('nama_pengguna', 'sandi', 'role')),
    "buku": (FILE_BUKU, ('id', 'judul', 'penulis', 'harga', 'stok')),
    "sewa": (FILE_SEWA, ("id_sewa", "nama_pengguna", "id_buku", "judul", "durasi", "total", "waktu_sewa", "status")),
    "transaksi": (FILE_TRANSAKSI, ("id_transaksi", "nama_pengguna", "jenis", "nominal", "keterangan", "tanggal")),
    "saldo": (FILE_SALDO, ("nama_pengguna", "saldo")),
}

# FUNGSI UMUM
def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def jeda(detik=1.0):
    time.sleep(detik)


def integer(nilai, default=0):
    try:
        return int(nilai)
    except (ValueError, TypeError):
        return default


def sekarang_teks():
    return datetime.now().strftime(FORMAT_TANGGAL)


def input_teks(pesan):
    while True:
        nilai = input(pesan).strip()
        if nilai:
            return nilai
        print("Input tidak boleh kosong.")


def input_angka(pesan, minimal=0, maksimal=None):
    while True:
        try:
            angka = int(input(pesan))
        except ValueError:
            print("Input harus berupa angka.")
            continue
        if angka < minimal:
            print(f"Nilai minimal adalah {minimal}.")
        elif maksimal is not None and angka > maksimal:
            print(f"Nilai maksimal adalah {maksimal}.")
        else:
            return angka

def konfirmasi(pesan):
    while True:
        jawab = input(f"{pesan} (y/n): ").strip().lower()
        if jawab in ("y", "n"):
            return jawab == "y"
        print("Pilihan tidak valid.")

def tampilkan_menu(judul, daftar_menu):
    print(f"\n=========== {judul} ===========")
    for nomor, teks in enumerate(daftar_menu, start=1):
        print(f"{nomor}. {teks}")
    print("=" * (len(judul) + 24))

# FILE CSV
def baca_csv(nama_file):
    data = []
    try:
        with open(nama_file, mode="r", newline='', encoding='utf-8') as file:
            for baris in csv.DictReader(file):
                data.append(baris)
    except FileNotFoundError:
        print(f"File {nama_file} tidak ditemukan, akan dibuat otomatis saat data disimpan.")
    except (OSError, csv.Error):
        print(f"Gagal membaca {nama_file}. Program dihentikan.")
        raise SystemExit
    return data

def tulis_csv(nama_file, kolom, data):
    try:
        with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=kolom, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data)
        return True
    except OSError:
        print(f"Gagal menyimpan {nama_file}. Pastikan file tidak sedang dibuka di program lain.")
        return False

def muat_semua():
    db = {}
    for nama, (nama_file, _kolom) in FORMAT.items():
        db[nama] = baca_csv(nama_file)
    if not db["akun"]:
        db["akun"].append({"nama_pengguna": "admin", "sandi": "admin123", "role": ROLE_ADMIN})
        print("Belum ada akun. Akun admin default dibuat (admin / admin123).")
    return db

def simpan_semua(db):
    berhasil = True
    for nama, (nama_file, kolom) in FORMAT.items():
        if not tulis_csv(nama_file, kolom, db[nama]):
            berhasil = False
    return berhasil

# DATA BUKU, SALDO, TRANSAKSI
def cari_buku(buku, id_buku):
    for item in buku:
        if item["id"] == id_buku:
            return item
    return None

def tampilkan_buku(buku):
    if not buku:
        print("Belum ada data buku.")
        return False
    tabel = PrettyTable(["ID", "Judul", "Penulis", "Harga/hari", "Stok"])
    for item in buku:
        tabel.add_row([item['id'], item['judul'], item['penulis'], item['harga'], item['stok']])
    print(tabel)
    return True

def cari_saldo(db, nama):
    for row in db["saldo"]:
        if row["nama_pengguna"] == nama:
            return row
    data_saldo = {"nama_pengguna": nama, "saldo": "0"}
    db["saldo"].append(data_saldo)
    return data_saldo

def id_berikutnya(data, kunci):
    return str(max([integer(item[kunci]) for item in data], default=0) + 1)

def catat_transaksi(db, nama, jenis, nominal, keterangan, tanggal=None):
    catatan = {
        "id_transaksi": id_berikutnya(db["transaksi"], "id_transaksi"),
        "nama_pengguna": nama,
        "jenis": jenis,
        "nominal": str(nominal),
        "keterangan": keterangan,
        "tanggal": tanggal or sekarang_teks(),
    }
    db["transaksi"].append(catatan)
    return catatan

def hitung_waktu_berakhir(data_sewa):
    try:
        mulai = datetime.strptime(data_sewa["waktu_sewa"], FORMAT_TANGGAL)
        return mulai + timedelta(seconds=int(data_sewa["durasi"]) * DETIK_PER_HARI)
    except (ValueError, TypeError, KeyError, OverflowError):
        return None

def format_sisa_waktu(waktu_berakhir, sekarang):
    sisa = max(waktu_berakhir - sekarang, timedelta(0))
    jam, sisa_detik = divmod(sisa.seconds, 3600)
    return f"{sisa.days} hari {jam} jam {sisa_detik // 60} menit"

def proses_sewa_berakhir(db):
    sekarang = datetime.now()
    jumlah = 0
    for data_sewa in db["sewa"]:
        if data_sewa.get("status") != "aktif":
            continue
        waktu_berakhir = hitung_waktu_berakhir(data_sewa)
        if waktu_berakhir is None or sekarang < waktu_berakhir:
            continue

        data_sewa["status"] = "selesai"
        item = cari_buku(db["buku"], data_sewa["id_buku"])
        if item is not None:
            item["stok"] = str(integer(item["stok"]) + 1)
        catat_transaksi(
            db, data_sewa["nama_pengguna"], "Sewa Berakhir", 0,
            f"Masa sewa '{data_sewa['judul']}' berakhir, buku otomatis tertutup",
        )
        jumlah += 1
    return jumlah

# AUTENTIKASI
def username_terpakai(akun, nama):
    return any(row["nama_pengguna"].lower() == nama.lower() for row in akun)

def validasi_akun(nama, sandi):
    if len(nama) < MIN_NAMA:
        return False, f"Nama pengguna minimal {MIN_NAMA} karakter."
    if not nama.isascii() or not nama.replace("_", "").isalnum():
        return False, "Nama pengguna hanya boleh huruf, angka, dan underscore (tanpa spasi)."
    if len(sandi) < MIN_SANDI:
        return False, f"Sandi minimal {MIN_SANDI} karakter."
    return True, ""

def registrasi(db):
    print("\n====================================")
    print("         DAFTAR AKUN BARU           ")
    print("====================================")
    nama = input("Masukkan nama pengguna baru: ").strip()
    sandi = pwinput.pwinput("Masukkan sandi: ")

    valid, pesan = validasi_akun(nama, sandi)
    if not valid:
        print(pesan)
        return False
    if username_terpakai(db["akun"], nama):
        print("Nama pengguna sudah terdaftar!")
        return False

    db["akun"].append({"nama_pengguna": nama, "sandi": sandi, "role": ROLE_PENGGUNA})
    db["saldo"].append({"nama_pengguna": nama, "saldo": "0"})
    print("Akun berhasil didaftarkan! Silakan login.")
    return True

def login(db):
    print("\n========== Login ==========")
    for percobaan in range(1, MAX_PERCOBAAN_LOGIN + 1):
        nama = input("Nama pengguna: ")
        sandi = pwinput.pwinput("Sandi: ")

        for row in db["akun"]:
            if row["nama_pengguna"] == nama and row["sandi"] == sandi:
                print(f"\nLogin berhasil sebagai {row['role']}")
                print(f"Selamat datang, {row['nama_pengguna']}")
                return row

        sisa = MAX_PERCOBAAN_LOGIN - percobaan
        print("Login gagal. Periksa kembali username, password, serta apakah akunmu telah terdaftar!")
        if sisa > 0:
            print(f"Sisa percobaan: {sisa}")

    print(f"\nTerlalu banyak percobaan gagal. Tunggu {JEDA_BLOKIR_LOGIN} detik...")
    for detik in range(JEDA_BLOKIR_LOGIN, 0, -1):
        print(f"  {detik}...")
        jeda(1)
    return None

# FITUR ADMIN

def tambah_buku(db):
    buku = db["buku"]
    while True:
        tampilkan_buku(buku)
        id_baru = id_berikutnya(buku, "id")
        judul = input_teks("Masukkan judul buku baru: ")
        penulis = input_teks("Masukkan nama penulis: ")
        harga = input_angka("Masukkan harga sewa per hari: Rp", minimal=0)
        stok = input_angka("Masukkan stok: ", minimal=0)

        buku.append({"id": id_baru, "judul": judul, "penulis": penulis,
                    "harga": str(harga), "stok": str(stok)})
        print("Buku berhasil ditambahkan!")

        if not  konfirmasi("Apakah masih ingin menambah buku?"):
            break

def edit_buku(db):
    buku = db["buku"]
    if not buku:
        print("Belum ada data buku.")
        return

    while True:
        tampilkan_buku(buku)
        id_edit = input("Masukkan ID buku yang ingin diubah: ").strip()
        buku_dipilih = cari_buku(buku, id_edit)

        if buku_dipilih is None:
            print("ID buku tidak ditemukan!")
        else:
            print("\nPilih data yang ingin diubah:")
            print("1. Judul")
            print("2. Penulis")
            print("3. Harga sewa")
            print("4. Stok")
            pilihan = input("Pilihan: ").strip()

            if pilihan == "1":
                buku_dipilih["judul"] = input_teks("Masukkan judul baru: ")
            elif pilihan == "2":
                buku_dipilih["penulis"] = input_teks("Masukkan nama penulis baru: ")
            elif pilihan == "3":
                buku_dipilih["harga"] = str(input_angka("Masukkan harga sewa baru per hari: Rp", minimal=0))
            elif pilihan == "4":
                buku_dipilih["stok"] = str(input_angka("Masukkan stok baru: ", minimal=0))
            else:
                print("Pilihan tidak valid!")

            if pilihan in ("1", "2", "3", "4"):
                print("Data buku berhasil diubah!")

        if not  konfirmasi("Apakah masih ingin mengubah buku?"):
            break

def hapus_buku(db):
    buku = db["buku"]
    if not buku:
        print("Belum ada data buku.")
        return

    while True:
        tampilkan_buku(buku)
        id_hapus = input("Masukkan ID buku yang ingin dihapus: ").strip()

        # ID tidak diurutkan ulang, karena ID dipakai oleh data sewa
        buku_dihapus = cari_buku(buku, id_hapus)

        if buku_dihapus is None:
            print("ID buku tidak ditemukan!")
        else:
            masih_disewa = any(s["id_buku"] == id_hapus and s.get("status") == "aktif"
                                for s in db["sewa"])
            if masih_disewa:
                print("Peringatan: buku ini sedang disewa oleh pengguna.")
            if  konfirmasi(f"Yakin ingin menghapus '{buku_dihapus['judul']}'?"):
                buku.remove(buku_dihapus)
                print("Buku berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")

        if not buku:
            print("Semua buku sudah terhapus.")
            break
        if not  konfirmasi("Apakah masih ingin menghapus buku?"):
            break

def tampilkan_sewa_aktif(db, nama_pengguna=None):
    kolom = ["ID Sewa", "Judul", "Durasi", "Mulai", "Sisa Waktu"]
    if nama_pengguna is None:
        kolom.insert(1, "Penyewa")
    tabel = PrettyTable(kolom)

    sekarang = datetime.now()
    ada = False
    for data in db["sewa"]:
        if data.get("status") != "aktif":
            continue
        if nama_pengguna is not None and data["nama_pengguna"] != nama_pengguna:
            continue
        waktu_berakhir = hitung_waktu_berakhir(data)
        if waktu_berakhir is None:
            continue

        baris = [data["id_sewa"], data["judul"], f"{data['durasi']} hari",
                data["waktu_sewa"], format_sisa_waktu(waktu_berakhir, sekarang)]
        if nama_pengguna is None:
            baris.insert(1, data["nama_pengguna"])
        tabel.add_row(baris)
        ada = True

    if ada:
        print(tabel)
    else:
        print("Tidak ada buku yang sedang disewa.")
    return ada

def tampilkan_transaksi(db, nama_pengguna=None):
    if nama_pengguna is None:
        riwayat = db["transaksi"]
        kolom = ["ID", "Pengguna", "Jenis", "Nominal", "Keterangan", "Tanggal"]
    else:
        riwayat = [t for t in db["transaksi"] if t["nama_pengguna"] == nama_pengguna]
        kolom = ["ID", "Jenis", "Nominal", "Keterangan", "Tanggal"]

    if not riwayat:
        print("Belum ada data transaksi.")
        return False

    tabel = PrettyTable(kolom)
    for t in riwayat:
        baris = [t["id_transaksi"], t["jenis"], f"Rp {t['nominal']}", t["keterangan"], t["tanggal"]]
        if nama_pengguna is None:
            baris.insert(1, t["nama_pengguna"])
        tabel.add_row(baris)
    print(tabel)
    return True

def hitung_laporan(db):
    transaksi_sewa = [t for t in db["transaksi"] if t["jenis"] == "Sewa"]
    total_pendapatan = sum(integer(t["nominal"]) for t in transaksi_sewa)

    hitung = {}
    for data in db["sewa"]:
        hitung[data["judul"]] = hitung.get(data["judul"], 0) + 1
    terlaris = sorted(hitung.items(), key=lambda item: item[1], reverse=True)[:3]

    return total_pendapatan, len(db["transaksi"]), len(transaksi_sewa), terlaris

def laporan_ringkas(db):
    total, jumlah_transaksi, jumlah_sewa, terlaris = hitung_laporan(db)

    print("\n========== LAPORAN RINGKAS ==========")
    print(f"Total pendapatan sewa : Rp {total}")
    print(f"Jumlah semua transaksi: {jumlah_transaksi}")
    print(f"Jumlah transaksi sewa : {jumlah_sewa}")

    if not terlaris:
        print("Belum ada buku yang disewa.")
        return

    tabel = PrettyTable(["Peringkat", "Judul", "Disewa (kali)"])
    for peringkat, (judul, jumlah) in enumerate(terlaris, start=1):
        tabel.add_row([peringkat, judul, jumlah])
    print("Buku terlaris:")
    print(tabel)

def menu_admin(db, akun):
    tampilkan_menu("Admin", MENU_ADMIN)
    pilihan = input(f"Pilih menu (1-{len(MENU_ADMIN)}): ").strip()

    if pilihan == "1":
        tampilkan_buku(db["buku"])
    elif pilihan == "2":
        tambah_buku(db)
    elif pilihan == "3":
        edit_buku(db)
    elif pilihan == "4":
        hapus_buku(db)
    elif pilihan == "5":
        tampilkan_sewa_aktif(db)
    elif pilihan == "6":
        tampilkan_transaksi(db)
    elif pilihan == "7":
        laporan_ringkas(db)
    elif pilihan == "8":
        print("\n------------------------------")
        print("  Keluar dari menu admin      ")
        print("------------------------------")
        return None
    else:
        print("Pilihan tidak valid!")
    return akun

# FITUR PENGGUNA

def hitung_total(buku_dipilih, durasi):
    return integer(buku_dipilih["harga"]) * durasi

def proses_sewa(db, nama, buku_dipilih, durasi):
    data_saldo = cari_saldo(db, nama)
    saldo_user = integer(data_saldo["saldo"])
    total = hitung_total(buku_dipilih, durasi)

    # Saldo dan stok tidak boleh negatif
    if saldo_user < total or integer(buku_dipilih["stok"]) <= 0:
        return None

    tanggal = sekarang_teks()
    db["sewa"].append({
        "id_sewa": id_berikutnya(db["sewa"], "id_sewa"),
        "nama_pengguna": nama,
        "id_buku": buku_dipilih["id"],
        "judul": buku_dipilih["judul"],
        "durasi": str(durasi),
        "total": str(total),
        "waktu_sewa": tanggal,
        "status": "aktif",
    })
    buku_dipilih["stok"] = str(integer(buku_dipilih["stok"]) - 1)
    data_saldo["saldo"] = str(saldo_user - total)
    catat_transaksi(db, nama, "Sewa", total,
                    f"Sewa '{buku_dipilih['judul']}' selama {durasi} hari", tanggal)

    return {"nama": nama, "judul": buku_dipilih["judul"], "durasi": durasi,
            "total": total, "sisa_saldo": saldo_user - total, "tanggal": tanggal}

def cetak_invoice(invoice):
    print(f"Sewa berhasil! Buku: {invoice['judul']}")
    print("\n==========================================")
    print("         INVOICE SEWA BUKU DIGITAL        ")
    print("==========================================")
    print(f"Nama Pengguna : {invoice['nama']}")
    print(f"Judul Buku    : {invoice['judul']}")
    print(f"Lama Sewa     : {invoice['durasi']} hari")
    print(f"Total Bayar   : Rp {invoice['total']}")
    print(f"Sisa Saldo    : Rp {invoice['sisa_saldo']}")
    print(f"Tanggal Sewa  : {invoice['tanggal']}")
    print("==========================================")
    print("Buku otomatis tertutup setelah masa sewa habis.\n")

def sewa_buku(db, akun):
    nama = akun["nama_pengguna"]
    if not db["buku"]:
        print("Belum ada buku tersedia.")
        return

    while True:
        saldo_user = integer(cari_saldo(db, nama)["saldo"])
        tampilkan_buku(db["buku"])
        print(f"Saldo Anda: Rp {saldo_user}")

        id_pilih = input("Masukkan ID buku yang ingin disewa: ").strip()
        buku_dipilih = cari_buku(db["buku"], id_pilih)

        if buku_dipilih is None:
            print("ID buku tidak ditemukan.")
        elif integer(buku_dipilih["stok"]) <= 0:
            print("Maaf, stok buku habis.")
        else:
            durasi = input_angka("Masukkan lama sewa (hari): ", minimal=1, maksimal=MAX_DURASI)
            total = hitung_total(buku_dipilih, durasi)
            if saldo_user < total:
                print(f"Saldo Anda tidak cukup. Total Rp {total}, saldo Anda Rp {saldo_user}.")
            else:
                invoice = proses_sewa(db, nama, buku_dipilih, durasi)
                if invoice is not None:
                    cetak_invoice(invoice)

        if not  konfirmasi("Apakah masih ingin menyewa buku lagi?"):
            break


def top_up(db, akun):
    nama = akun["nama_pengguna"]
    data_saldo = cari_saldo(db, nama)

    try:
        tambah = int(input("Masukkan jumlah top-up: "))
    except ValueError:
        print("Input tidak valid. Masukkan angka.")
        return False

    if tambah < MIN_SALDO:
        print(f"Minimal top-up adalah Rp{MIN_SALDO}.")
        return False
    if tambah > MAX_SALDO:
        print(f"Maksimal top-up per transaksi adalah Rp{MAX_SALDO}.")
        return False

    if not  konfirmasi(f"Yakin ingin top-up sebesar Rp{tambah}?"):
        print("Top up dibatalkan.")
        return False

    saldo_baru = integer(data_saldo["saldo"]) + tambah
    data_saldo["saldo"] = str(saldo_baru)
    catat_transaksi(db, nama, "Top Up", tambah, "Top up saldo")
    print(f"Top up berhasil! Saldo sekarang: Rp{saldo_baru}")
    return True


def menu_pengguna(db, akun):
    nama = akun["nama_pengguna"]
    tampilkan_menu("Menu Pengguna", MENU_PENGGUNA)
    pilihan = input(f"Pilih menu (1-{len(MENU_PENGGUNA)}): ").strip()

    if pilihan == "1":
        tampilkan_buku(db["buku"])
    elif pilihan == "2":
        sewa_buku(db, akun)
    elif pilihan == "3":
        tampilkan_sewa_aktif(db, nama)
    elif pilihan == "4":
        print(f"Saldo E-money Anda: Rp {integer(cari_saldo(db, nama)['saldo'])}")
    elif pilihan == "5":
        top_up(db, akun)
    elif pilihan == "6":
        tampilkan_transaksi(db, nama)
    elif pilihan == "7":
        print("\n------------------------------")
        print("  Keluar dari menu pengguna.")
        print("------------------------------")
        return None
    else:
        print("Pilihan tidak valid!")
    return akun

# MENU AWAL & PROGRAM UTAMA
def menu_awal(db):
    print("\n====================================")
    print("   Selamat Datang di Sewa Buku Digital   ")
    print("====================================")
    for nomor, teks in enumerate(MENU_AWAL, start=1):
        print(f"[{nomor}] {teks}")

    pilihan = input("Pilih menu: ").strip()

    if pilihan == "1":
        akun = login(db)
        if akun is not None:
            jeda(1.5)
            bersihkan_layar()
        return akun, False
    if pilihan == "2":
        registrasi(db)
        return None, False
    if pilihan == "3":
        print("Terima kasih telah menggunakan sistem Sewa Buku Digital.")
        return None, True

    print("Pilihan tidak valid.")
    return None, False

bersihkan_layar()
db = muat_semua()
akun_login = None

while True:
    keluar = False
    try:
        proses_sewa_berakhir(db)

        if akun_login is None:
            akun_login, keluar = menu_awal(db)
        else:
            if akun_login["role"] == ROLE_ADMIN:
                akun_login = menu_admin(db, akun_login)
            else:
                akun_login = menu_pengguna(db, akun_login)
            if akun_login is None:   
                jeda(1)
                bersihkan_layar()

    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
    except EOFError:
        print("\nJangan tekan CTRL + Z ya!")
    except Exception as e:
        print(f"\nTerjadi kesalahan yang tidak terduga: {type(e).__name__}: {e}")
    finally:
        simpan_semua(db)

    if keluar:
        break
