<div align="center">

<h1 id="readme-top">SISTEM PENYEWAAN BUKU DIGITAL</h1>

Aplikasi CLI berbasis Python untuk menyewa buku secara digital, lengkap dengan sistem registrasi, login, dua role pengguna, e-money, invoice, dan penyimpanan data permanen dalam file CSV.


**Disusun Oleh :**
- Nama : Muhammad Irfan Nazir | NIM : 070
- Nama : Muhammad Agustyon | NIM : 049
- Nama : Naufa Fauza Eky | NIM : 060
- Nama : Gresius Krisna Samuel | NIM : 057 

</div>

---

## Daftar Isi

1. [Tentang Program](#tentang-program)
2. [Flowchart dan Penjelasan Alur](#flowchart-dan-penjelasan-alur)
3. [Penjelasan Code](#penjelasan-code)
4. [Screenshot Output](#screenshot-output)

---

## Tentang Program

Program ini adalah aplikasi CLI (command line) untuk menyewa buku digital. Pengguna dapat mendaftar akun, login, mengisi saldo e-money, lalu menyewa buku dengan lama sewa tertentu. Admin mengelola katalog buku dan memantau seluruh aktivitas penyewaan. Semua data disimpan permanen di file **CSV**, sehingga tidak hilang saat program ditutup.

| Role | Akses Menu | Data yang Terlihat |
|---|---|---|
| admin | Lihat, Tambah, Edit, Hapus Buku, Lihat Buku yang Sedang Disewa, Riwayat Transaksi Semua User, Laporan Ringkas, Keluar | Data buku, penyewaan, dan transaksi semua user |
| pengguna | Lihat Buku, Sewa Buku, Buku yang Sedang Saya Sewa, Cek Saldo, Top Up, Riwayat Transaksi Saya, Keluar | Hanya sewa dan transaksi miliknya sendiri |

Seluruh data di dalam program disimpan sebagai **list yang berisi dictionary** (satu dictionary per baris CSV), lalu dikumpulkan dalam satu dictionary besar bernama `db`:

```python
db = {
    "akun":      [ {...}, {...} ],
    "buku":      [ {...}, {...} ],
    "sewa":      [ {...}, {...} ],
    "transaksi": [ {...}, {...} ],
    "saldo":     [ {...}, {...} ],
}
```

Program juga mendukung **logout dan ganti akun** tanpa menutup aplikasi, sehingga mudah diuji:

1. Daftar akun baru (menu 2), lalu login sebagai pengguna.
2. Top up saldo dan sewa buku.
3. Keluar dari menu pengguna, lalu login sebagai admin untuk melihat sewa aktif, riwayat transaksi, dan laporan.

---

## Fitur

- **Registrasi akun** dengan validasi nama pengguna (minimal 4 karakter, hanya huruf, angka, dan underscore) dan sandi (minimal 6 karakter).
- **Login dengan batas percobaan.** Maksimal 3 kali salah, sandi tersembunyi saat diketik, lalu akun diblokir sementara dengan hitung mundur 5 detik.
- **Hak akses berdasarkan role.** Admin dan pengguna mendapat menu yang berbeda.
- **CRUD buku** (khusus admin): tambah, lihat, edit, dan hapus buku.
- **Sewa buku** dengan lama sewa 1 sampai 365 hari, pengecekan saldo dan stok, serta **invoice** setelah sewa berhasil.
- **E-money.** Cek saldo dan top up (minimal Rp10.000, maksimal Rp500.000 per transaksi) dengan konfirmasi y/n.
- **Masa sewa otomatis berakhir.** Saat waktu sewa habis, status berubah menjadi selesai dan stok buku kembali bertambah.
- **Riwayat transaksi.** Admin melihat semua transaksi, pengguna hanya melihat miliknya.
- **Laporan ringkas** (admin): total pendapatan, jumlah transaksi, dan tiga buku terlaris.
- **Penyimpanan permanen** ke lima file CSV.
- **Penanganan error** dengan `try-except`, sehingga program tidak langsung crash saat terjadi kesalahan.
- **Clear screen sesuai OS** (Windows memakai `cls`, selain itu memakai `clear`).

---

## Akun Awal dan Hak Akses

Jika file `akun.csv` belum ada atau kosong, program otomatis membuat akun admin default:

| Username | Password | Role |
|---|---|---|
| admin | admin123 | admin |

Akun pengguna dibuat lewat menu **Daftar Akun Baru**. Setiap akun pengguna baru otomatis mendapat saldo awal Rp0.

Menu admin:

| Menu | Fitur |
|:---:|---|
| 1 | Lihat Daftar Buku |
| 2 | Tambah Buku Baru |
| 3 | Edit Buku |
| 4 | Hapus Buku |
| 5 | Lihat Buku yang Sedang Disewa |
| 6 | Lihat Riwayat Transaksi Semua User |
| 7 | Laporan Ringkas |
| 8 | Keluar |

Menu pengguna:

| Menu | Fitur |
|:---:|---|
| 1 | Lihat Daftar Buku |
| 2 | Sewa Buku |
| 3 | Buku yang Sedang Saya Sewa |
| 4 | Cek Saldo E-money |
| 5 | Top Up Saldo |
| 6 | Riwayat Transaksi Saya |
| 7 | Keluar |

---

## Struktur Data

Data disimpan dalam lima file CSV. Setiap file dibaca dengan `csv.DictReader` dan ditulis dengan `csv.DictWriter`.

| File | Kolom | Keterangan |
|---|---|---|
| `akun.csv` | `nama_pengguna`, `sandi`, `role` | Data akun login |
| `buku.csv` | `id`, `judul`, `penulis`, `harga`, `stok` | Katalog buku, harga adalah harga sewa per hari |
| `sewa.csv` | `id_sewa`, `nama_pengguna`, `id_buku`, `judul`, `durasi`, `total`, `waktu_sewa`, `status` | Data penyewaan, status `aktif` atau `selesai` |
| `transaksi.csv` | `id_transaksi`, `nama_pengguna`, `jenis`, `nominal`, `keterangan`, `tanggal` | Riwayat transaksi: Top Up, Sewa, Sewa Berakhir |
| `saldo.csv` | `nama_pengguna`, `saldo` | Saldo e-money tiap pengguna |

Contoh satu data buku:

```python
{
    "id": "1",
    "judul": "Pemrograman Python Dasar",
    "penulis": "Budi Santoso",
    "harga": "5000",
    "stok": "3"
}
```

Contoh satu data sewa:

```python
{
    "id_sewa": "1",
    "nama_pengguna": "irfan",
    "id_buku": "1",
    "judul": "Pemrograman Python Dasar",
    "durasi": "7",
    "total": "35000",
    "waktu_sewa": "2026-11-02 10:30:00",
    "status": "aktif"
}
```

| Aturan Data | Keterangan |
|---|---|
| ID buku, ID sewa, ID transaksi | Dibuat otomatis, nilai terbesar yang ada ditambah 1 |
| `harga` dan `stok` buku | Bilangan bulat, minimal 0 |
| `durasi` sewa | 1 sampai 365 hari |
| `total` | `harga` dikali `durasi` |
| Saldo dan stok | Tidak boleh negatif |


<p align="right">(<a href="#readme-top">back to top</a>)</p>


---

## Flowchart dan Penjelasan Alur

<!-- Ganti baris di bawah dengan gambar flowchart kamu -->
<img width="1507" height="990" alt="flowchart_program" src="LINK_GAMBAR_FLOWCHART" />

### 1. Awal program

Program dimulai dari **Mulai**. Layar dibersihkan, lalu semua file CSV dimuat ke dalam `db`. Jika belum ada akun sama sekali, akun admin default dibuat.

### 2. Menu awal

Pengguna memilih salah satu dari tiga menu:

| Pilihan | Aksi |
|---|---|
| 1. Login | Masuk ke proses login |
| 2. Daftar Akun Baru | Membuat akun pengguna baru, lalu kembali ke menu awal |
| 3. Keluar | Tampil "Terima kasih", lalu **Selesai** |

Jika pilihan selain 1 sampai 3, tampil "Pilihan tidak valid" dan menu awal ditampilkan lagi.

### 3. Validasi login

Program meminta **nama pengguna dan sandi**, lalu mengecek: **Login benar?** Artinya, ada akun dengan nama pengguna dan sandi yang cocok.

- **Tidak:** tampil pesan login gagal beserta sisa percobaan. Program mengecek **Gagal 3 kali?**
  - **Tidak:** pengguna kembali mengisi nama pengguna dan sandi.
  - **Ya:** tampil hitung mundur 5 detik, lalu pengguna kembali ke **menu awal**.
- **Ya:** tampil "Login berhasil sebagai (role)" dan pesan selamat datang, lalu lanjut ke pengecekan role.

### 4. Validasi role (admin atau pengguna)

Program mengecek: **Role = admin?**

- **Ya:** tampil **Menu Admin (1-8)**.
- **Tidak:** tampil **Menu Pengguna (1-7)**.

### 5. Alur menu admin

| Menu | Proses |
|---|---|
| 1. Lihat Daftar Buku | Menampilkan semua buku dalam tabel |
| 2. Tambah Buku Baru | Input judul, penulis, harga, stok, lalu tanya "masih ingin menambah?" |
| 3. Edit Buku | Pilih ID buku, pilih data yang diubah (judul, penulis, harga, atau stok) |
| 4. Hapus Buku | Pilih ID buku, tampil peringatan jika sedang disewa, lalu konfirmasi y/n |
| 5. Lihat Buku yang Sedang Disewa | Tabel sewa aktif semua penyewa beserta sisa waktu |
| 6. Riwayat Transaksi Semua User | Tabel seluruh transaksi |
| 7. Laporan Ringkas | Total pendapatan, jumlah transaksi, dan buku terlaris |
| 8. Keluar | Kembali ke menu awal |

### 6. Alur menu pengguna

| Menu | Proses |
|---|---|
| 1. Lihat Daftar Buku | Menampilkan semua buku dalam tabel |
| 2. Sewa Buku | Lihat alur sewa di bawah |
| 3. Buku yang Sedang Saya Sewa | Tabel sewa aktif milik sendiri beserta sisa waktu |
| 4. Cek Saldo E-money | Menampilkan saldo |
| 5. Top Up Saldo | Input nominal, cek batas, konfirmasi y/n, saldo bertambah |
| 6. Riwayat Transaksi Saya | Tabel transaksi milik sendiri |
| 7. Keluar | Kembali ke menu awal |

### 7. Alur sewa buku

1. Tampil daftar buku dan saldo pengguna, lalu pengguna memasukkan **ID buku**.
2. Program mengecek **ID ditemukan?** Jika tidak, tampil "ID buku tidak ditemukan".
3. Program mengecek **Stok > 0?** Jika tidak, tampil "stok buku habis".
4. Pengguna memasukkan **lama sewa** (1 sampai 365 hari), lalu program menghitung total = harga x durasi.
5. Program mengecek **Saldo cukup?** Jika tidak, tampil pesan saldo tidak cukup.
6. Jika cukup: data sewa dicatat, stok berkurang 1, saldo dipotong, transaksi dicatat, lalu **invoice** ditampilkan.
7. Program bertanya "masih ingin menyewa buku lagi?". Jika `y`, alur kembali ke langkah 1.

### 8. Masa sewa berakhir otomatis

Di setiap putaran program, fungsi `proses_sewa_berakhir()` dijalankan lebih dulu. Untuk setiap sewa berstatus `aktif` yang waktunya sudah habis, status diubah menjadi `selesai`, stok buku ditambah 1, dan transaksi jenis **Sewa Berakhir** dicatat.

### 9. Penyimpanan data

Setelah setiap putaran program (blok `finally`), seluruh isi `db` disimpan ke lima file CSV. Jadi data tetap aman walaupun terjadi error.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


---


## Penjelasan Code

### 1. Library yang Digunakan

```python
import csv
import os
import time
import pwinput
from datetime import datetime, timedelta
from prettytable import PrettyTable
```

| Library | Kegunaan di program |
|---|---|
| `csv` | Membaca (`DictReader`) dan menulis (`DictWriter`) file CSV |
| `os` | `os.system()` untuk membersihkan layar, dengan pengecekan OS (`cls` untuk Windows, `clear` untuk lainnya) |
| `time` | `time.sleep()` memberi jeda agar pesan sempat terbaca dan untuk hitung mundur blokir login |
| `pwinput` | Menyembunyikan ketikan sandi (tampil `*`) |
| `datetime`, `timedelta` | Mencatat waktu sewa dan menghitung kapan masa sewa berakhir serta sisa waktunya |
| `prettytable` | Menampilkan data dalam bentuk tabel yang rapi |

### 2. Konstanta dan Variabel Utama

```python
FILE_AKUN = 'akun.csv'
FILE_BUKU = 'buku.csv'
FILE_SEWA = 'sewa.csv'
FILE_TRANSAKSI = 'transaksi.csv'
FILE_SALDO = 'saldo.csv'

MIN_SALDO = 10000
MAX_SALDO = 500000
MAX_DURASI = 365

MAX_PERCOBAAN_LOGIN = 3
JEDA_BLOKIR_LOGIN = 5
MIN_NAMA = 4
MIN_SANDI = 6

ROLE_ADMIN = "admin"
ROLE_PENGGUNA = "pengguna"
```

| Variabel | Tipe | Fungsi |
|---|---|---|
| `FILE_...` | string | Nama kelima file CSV |
| `MIN_SALDO`, `MAX_SALDO` | integer | Batas minimal dan maksimal top up per transaksi |
| `MAX_DURASI` | integer | Lama sewa maksimal (hari) |
| `MAX_PERCOBAAN_LOGIN`, `JEDA_BLOKIR_LOGIN` | integer | Batas salah login dan lama blokir (detik) |
| `MIN_NAMA`, `MIN_SANDI` | integer | Panjang minimal nama pengguna dan sandi |
| `MENU_AWAL`, `MENU_ADMIN`, `MENU_PENGGUNA` | tuple | Daftar teks menu yang tidak berubah |
| `FORMAT` | dictionary | Memetakan tiap data ke nama file dan daftar kolom CSV-nya |
| `db` | dictionary berisi list | Penampung seluruh data selama program berjalan |

Menu disimpan sebagai **tuple** karena isinya tidak boleh berubah selama program berjalan.

### 3. Fungsi Umum dan Validasi Input

Fungsi input memakai `while True`, jadi pengguna terus diminta mengisi sampai inputnya benar.

| Fungsi | Aturan | Hasil |
|---|---|---|
| `input_teks(pesan)` | Tidak boleh kosong | String |
| `input_angka(pesan, minimal, maksimal)` | Harus angka dan berada dalam rentang | Integer |
| `konfirmasi(pesan)` | Harus `y` atau `n` | `True` atau `False` |
| `integer(nilai, default)` | Mengubah ke integer, jika gagal memakai nilai default (0) | Integer |
| `bersihkan_layar()` | Membersihkan layar sesuai OS | - |
| `jeda(detik)` | Menahan program beberapa detik | - |
| `sekarang_teks()` | Waktu saat ini dalam format `YYYY-MM-DD HH:MM:SS` | String |
| `tampilkan_menu(judul, daftar_menu)` | Mencetak menu bernomor dari tuple | - |

Contoh fungsi validasi:

```python
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
```

### 4. Fungsi File CSV

| Fungsi | Kegunaan |
|---|---|
| `baca_csv(nama_file)` | Membaca file menjadi list dictionary. Jika file belum ada, program memberi tahu dan file dibuat saat data disimpan. Jika gagal dibaca, program dihentikan |
| `tulis_csv(nama_file, kolom, data)` | Menulis list dictionary ke file CSV. Mengembalikan `False` jika gagal (misalnya file sedang dibuka di program lain) |
| `muat_semua()` | Memuat kelima file ke dalam `db`, dan membuat akun admin default bila belum ada akun |
| `simpan_semua(db)` | Menyimpan kelima data di `db` ke file masing-masing |

### 5. Fungsi Data Buku, Saldo, dan Transaksi

| Fungsi | Kegunaan |
|---|---|
| `cari_buku(buku, id_buku)` | Mencari buku berdasarkan ID, mengembalikan `None` jika tidak ada |
| `tampilkan_buku(buku)` | Menampilkan katalog buku dalam `PrettyTable` |
| `cari_saldo(db, nama)` | Mencari saldo pengguna. Jika belum ada, dibuat dengan saldo 0 |
| `id_berikutnya(data, kunci)` | Menghasilkan ID baru (ID terbesar + 1) |
| `catat_transaksi(...)` | Menambahkan satu catatan ke riwayat transaksi |
| `hitung_waktu_berakhir(data_sewa)` | Menghitung waktu sewa berakhir dengan `timedelta` |
| `format_sisa_waktu(...)` | Mengubah sisa waktu menjadi teks "x hari y jam z menit" |
| `proses_sewa_berakhir(db)` | Menutup sewa yang sudah habis dan mengembalikan stok buku |

### 6. Autentikasi: `registrasi()` dan `login()`

**`registrasi(db)`**

1. Meminta nama pengguna dan sandi (sandi tersembunyi).
2. `validasi_akun()` mengecek panjang nama (minimal 4), karakter nama (hanya huruf ASCII, angka, underscore), dan panjang sandi (minimal 6).
3. `username_terpakai()` mengecek apakah nama sudah dipakai (huruf besar kecil diabaikan).
4. Jika lolos, akun dibuat dengan role `pengguna` dan saldo awal `0`.

**`login(db)`**

1. Perulangan `for` sebanyak `MAX_PERCOBAAN_LOGIN` kali, tiap putaran meminta nama pengguna dan sandi.
2. Jika ada akun yang cocok, fungsi mengembalikan data akun tersebut.
3. Jika salah, sisa percobaan ditampilkan.
4. Jika gagal 3 kali, program menampilkan hitung mundur 5 detik lalu mengembalikan `None`, dan pengguna kembali ke menu awal.

### 7. Fitur Admin

**`tambah_buku(db)`**: meminta judul, penulis, harga sewa per hari, dan stok. ID dibuat otomatis, lalu data ditambahkan dengan `append`. Setelah itu program bertanya apakah ingin menambah lagi.

**`edit_buku(db)`**: admin memilih ID buku, lalu memilih bagian yang diubah (judul, penulis, harga, atau stok). Jika ID tidak ditemukan atau pilihan tidak valid, tampil pesan.

**`hapus_buku(db)`**: admin memilih ID buku. Jika buku sedang disewa, tampil peringatan. Penghapusan harus dikonfirmasi `y`/`n`. ID tidak diurutkan ulang karena ID buku juga dipakai oleh data sewa.

**`tampilkan_sewa_aktif(db, nama_pengguna)`**: menampilkan sewa berstatus `aktif` beserta sisa waktu. Jika `nama_pengguna` kosong (`None`), semua penyewa ditampilkan dengan kolom **Penyewa** (dipakai admin). Jika diisi, hanya sewa milik pengguna itu yang tampil.

**`tampilkan_transaksi(db, nama_pengguna)`**: memakai pola yang sama. Admin melihat semua transaksi dengan kolom **Pengguna**, pengguna disaring dengan list comprehension:

```python
riwayat = [t for t in db["transaksi"] if t["nama_pengguna"] == nama_pengguna]
```

**`laporan_ringkas(db)`** dan **`hitung_laporan(db)`**: menghitung total pendapatan dari transaksi jenis `Sewa`, jumlah seluruh transaksi, jumlah transaksi sewa, dan tiga buku terlaris. Buku terlaris dihitung dengan dictionary penghitung lalu diurutkan dengan `sorted()`.

### 8. Fitur Pengguna

**`sewa_buku(db, akun)`**: alur lengkapnya sebagai berikut.

1. Menampilkan daftar buku dan saldo, lalu meminta ID buku.
2. Mengecek ID ditemukan dan stok tersedia.
3. Meminta lama sewa (1 sampai 365 hari) dan menghitung total dengan `hitung_total()`.
4. Jika saldo cukup, `proses_sewa()` mencatat data sewa, mengurangi stok, memotong saldo, dan mencatat transaksi `Sewa`.
5. `cetak_invoice()` menampilkan invoice: nama, judul, lama sewa, total bayar, sisa saldo, dan tanggal sewa.

**`top_up(db, akun)`**: meminta nominal, mengecek batas minimal Rp10.000 dan maksimal Rp500.000, meminta konfirmasi, lalu menambah saldo dan mencatat transaksi `Top Up`.

```python
if tambah < MIN_SALDO:
    print(f"Minimal top-up adalah Rp{MIN_SALDO}.")
    return False
if tambah > MAX_SALDO:
    print(f"Maksimal top-up per transaksi adalah Rp{MAX_SALDO}.")
    return False
```

### 9. Menu: `menu_awal()`, `menu_admin()`, dan `menu_pengguna()`

- **`menu_awal(db)`** menampilkan menu Login, Daftar Akun Baru, dan Keluar. Fungsi mengembalikan dua nilai: akun yang login (atau `None`) dan penanda apakah program harus berhenti.
- **`menu_admin(db, akun)`** dan **`menu_pengguna(db, akun)`** menampilkan menu sesuai role, lalu memanggil fungsi dengan `if / elif`. Jika pengguna memilih Keluar, fungsi mengembalikan `None` sehingga program kembali ke menu awal. Selain itu fungsi mengembalikan `akun` agar sesi login tetap berlanjut.

Validasi role dilakukan lewat pemisahan fungsi menu: setelah login, program memilih `menu_admin` atau `menu_pengguna` berdasarkan role, sehingga pengguna biasa tidak punya jalur untuk membuka fitur admin.

### 10. Perulangan Utama Program

```python
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
```

Penjelasan:

1. Setiap putaran memproses sewa yang sudah habis terlebih dahulu.
2. Jika belum login (`akun_login is None`), tampil menu awal. Jika sudah, tampil menu sesuai role.
3. `try-except` menangkap `CTRL + C`, `CTRL + Z`, dan error tak terduga, sehingga program tidak langsung berhenti.
4. Blok `finally` selalu menyimpan data ke CSV di setiap putaran.
5. Program berhenti hanya saat pengguna memilih Keluar di menu awal (`keluar = True`).

### 11. Konsep Pemrograman yang Digunakan

| Konsep | Contoh di program |
|---|---|
| Variabel, tipe data, operator | `saldo_user`, `total`, `durasi`, `==`, `in`, `and`, `<`, `>` |
| Conditional statement | `if / elif / else` pada menu, login, dan validasi |
| Looping | `while True` pada menu dan validasi; `for` pada login dan pengisian tabel |
| List | `db["buku"]`, `db["sewa"]`, dan data lainnya |
| Tuple | `MENU_AWAL`, `MENU_ADMIN`, `MENU_PENGGUNA`, `DAFTAR_ROLE` |
| Dictionary | `db`, `FORMAT`, dan setiap data buku, akun, sewa, saldo, dan transaksi |
| Function (parameter dan return) | `login()`, `proses_sewa()`, `hitung_total()`, dan lainnya |
| File handling (CSV) | `baca_csv()`, `tulis_csv()` dengan `DictReader` dan `DictWriter` |
| Exception handling | `try-except` pada input angka, file CSV, dan perulangan utama |
| Library | `csv`, `os`, `time`, `datetime`, `pwinput`, `prettytable` |


<p align="right">(<a href="#readme-top">back to top</a>)</p>


---

## Screenshot Output

Berikut tampilan program saat dijalankan di terminal. Ganti `LINK_GAMBAR` dengan link screenshot kamu.

### 1. Menu Awal

<img width="468" height="249" alt="WhatsApp Image 2026-11-02 at 22 32 14" src="https://github.com/user-attachments/assets/e0df0ce6-d2d5-4403-a664-bb52d343f57a" />

Menu awal berisi pilihan Login, Daftar Akun Baru, dan Keluar.

### 2. Registrasi Akun

<img width="412" height="157" alt="WhatsApp Image 2026-11-02 at 22 37 18" src="https://github.com/user-attachments/assets/7f1f588a-f22a-4012-819d-f814b95aa203" />

Pengguna memasukkan nama pengguna dan sandi (tampil `*`). Input yang tidak memenuhi aturan (nama terlalu pendek, sandi kurang dari 6 karakter, atau nama sudah terdaftar) ditolak.

### 3. Login Berhasil

- Admin
<img width="424" height="345" alt="WhatsApp Image 2026-11-02 at 22 39 55" src="https://github.com/user-attachments/assets/dd32d8b8-25f9-41d1-bea8-e305db79d8d3" />

---

- Pengguna
<img width="384" height="346" alt="WhatsApp Image 2026-11-02 at 22 41 14" src="https://github.com/user-attachments/assets/dd92737a-2d8a-4bea-a5c8-4f9d9122b528" />

Program menampilkan pesan login berhasil beserta role dan nama pengguna.

### 4. Login Gagal

<img width="822" height="799" alt="WhatsApp Image 2026-11-02 at 22 45 24" src="https://github.com/user-attachments/assets/c79419f6-9cdd-43b4-a0c1-4cbbc33e8d7c" />

Jika nama pengguna atau sandi salah, program menampilkan sisa percobaan. Setelah gagal 3 kali, muncul hitung mundur 5 detik lalu pengguna kembali ke menu awal.

### 5. Menu Admin

<img width="369" height="279" alt="WhatsApp Image 2026-11-02 at 22 46 27" src="https://github.com/user-attachments/assets/2cdf6934-d656-49f4-b444-f9bd7e19c483" />

Admin mendapat 8 menu: *Lihat Buku, Tambah Buku, Edit Buku, Hapus Buku, Lihat Buku yang Sedang Disewa, Riwayat Transaksi Semua User, Laporan Ringkas, dan Keluar.*

### 6. Menu Pengguna

<img width="409" height="259" alt="WhatsApp Image 2026-11-02 at 22 47 23" src="https://github.com/user-attachments/assets/0c635a94-c7fe-4c43-ba8d-5586b7950bf2" />

Pengguna mendapat 7 menu: *Lihat Buku, Sewa Buku, Buku yang Sedang Saya Sewa, Cek Saldo, Top Up, Riwayat Transaksi Saya, dan Keluar.*

### 7. Tambah Buku (Admin)

<img width="636" height="340" alt="WhatsApp Image 2026-11-02 at 23 52 44" src="https://github.com/user-attachments/assets/95272411-c67b-4d23-a801-7fef600feafe" />

Admin mengisi judul, penulis, harga sewa per hari, dan stok. Setiap input divalidasi.

### 8. Edit Buku (Admin)

<img width="634" height="466" alt="WhatsApp Image 2026-11-02 at 23 53 57" src="https://github.com/user-attachments/assets/00604f9d-a4c5-41bc-b73c-6f95fc06ab19" />

Admin memilih ID buku, lalu memilih data yang ingin diubah.

### 9. Hapus Buku (Admin)

<img width="630" height="319" alt="WhatsApp Image 2026-11-02 at 23 55 05" src="https://github.com/user-attachments/assets/dbcbd810-4f50-4e68-9775-2d60e9265a05" />

Sebelum buku dihapus, program meminta konfirmasi `y` atau `n`. Jika buku sedang disewa, tampil peringatan.

### 10. Buku yang Sedang Disewa (Admin)

<img width="880" height="118" alt="WhatsApp Image 2026-11-02 at 23 56 34" src="https://github.com/user-attachments/assets/b8c60c74-5dd5-4846-a2f3-d10441b5c09d" />

Admin melihat semua sewa aktif dari semua pengguna, lengkap dengan kolom Penyewa dan Sisa Waktu.

### 11. Riwayat Transaksi dan Laporan Ringkas (Admin)

<img width="1189" height="396" alt="WhatsApp Image 2026-11-03 at 00 01 25" src="https://github.com/user-attachments/assets/86da3e4d-9707-4840-80e8-ab5216b01540" />
<img width="433" height="282" alt="WhatsApp Image 2026-11-03 at 00 02 29" src="https://github.com/user-attachments/assets/46a9ab63-bbf7-4b4f-81f9-401adc485125" />

Admin melihat seluruh transaksi, serta laporan berisi total pendapatan, jumlah transaksi, dan tiga buku terlaris.

### 12. Top Up Saldo (Pengguna)

<img width="429" height="292" alt="WhatsApp Image 2026-11-03 at 00 05 01" src="https://github.com/user-attachments/assets/c9ff4a45-08bb-439e-85cf-c1aab4abbeac" />

Pengguna memasukkan nominal top up (Rp10.000 sampai Rp500.000), lalu mengonfirmasi dengan `y` atau `n`.

### 13. Sewa Buku dan Invoice (Pengguna)

<img width="630" height="592" alt="WhatsApp Image 2026-11-03 at 00 06 54" src="https://github.com/user-attachments/assets/f10436a0-f1a8-4603-a1e5-1ac9b82c3c4d" />

Pengguna memilih ID buku dan lama sewa. Jika saldo dan stok mencukupi, sewa berhasil dan invoice ditampilkan.

### 14. Sewa Gagal (Saldo Tidak Cukup atau Stok Habis)

<img width="633" height="313" alt="WhatsApp Image 2026-11-03 at 00 08 40" src="https://github.com/user-attachments/assets/11f952d7-d47a-4e2a-9b04-784784314608" />

Jika saldo tidak cukup atau stok buku habis, program menampilkan pesan dan sewa tidak diproses.

### 15. Buku yang Sedang Saya Sewa (Pengguna)

<img width="760" height="109" alt="WhatsApp Image 2026-11-03 at 00 10 04" src="https://github.com/user-attachments/assets/b2e2d7fb-8c74-426a-ad67-13cad65cdece" />

Pengguna hanya melihat sewa miliknya sendiri beserta sisa waktu sewa.

### 16. Riwayat Transaksi Saya (Pengguna)

<img width="784" height="141" alt="WhatsApp Image 2026-11-03 at 00 10 44" src="https://github.com/user-attachments/assets/b95cd51c-c889-414b-b6e8-c914430d7864" />

Pengguna hanya melihat transaksi miliknya, tanpa kolom Pengguna.

### 17. Keluar dan Ganti Akun

<img width="411" height="354" alt="WhatsApp Image 2026-11-03 at 00 12 48" src="https://github.com/user-attachments/assets/3b5d2eff-08e7-4f66-b844-74bcee3d31c4" />
<img width="382" height="189" alt="WhatsApp Image 2026-11-03 at 00 12 48 (1)" src="https://github.com/user-attachments/assets/b7fd7fe8-6c45-48d4-9765-0980cad2ae36" />

Setelah memilih Keluar di menu admin atau pengguna, program kembali ke menu awal sehingga pengguna dapat login dengan akun lain.

### 18. Data Tersimpan di File CSV

<img width="406" height="202" alt="WhatsApp Image 2026-11-03 at 00 18 35" src="https://github.com/user-attachments/assets/8ea56615-b690-4624-a3ef-728d970f0a73" />
<img width="531" height="202" alt="WhatsApp Image 2026-11-03 at 00 18 35 (1)" src="https://github.com/user-attachments/assets/cb44492c-d0bb-4f60-9128-83de61dc816c" />
<img width="730" height="256" alt="WhatsApp Image 2026-11-03 at 00 18 35 (2)" src="https://github.com/user-attachments/assets/9d55fa72-9a13-4b2e-a496-990475fce4f8" />
<img width="1138" height="463" alt="WhatsApp Image 2026-11-03 at 00 18 35 (3)" src="https://github.com/user-attachments/assets/99c24edd-ae45-4f7b-a17e-a408b4cde912" />
<img width="301" height="148" alt="WhatsApp Image 2026-11-03 at 00 18 35 (4)" src="https://github.com/user-attachments/assets/06651fcd-3685-41f5-9e6f-13d6e51110a6" />

Data akun, buku, sewa, transaksi, dan saldo tersimpan di file CSV dan tetap ada saat program dijalankan kembali.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


---

