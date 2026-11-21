# Todo List - Ruang Rencana

Aplikasi todo list berbasis Flask untuk mencatat, mengubah, dan menghapus rencana harian. Tampilan menggunakan Jinja2, Tailwind CSS CDN, CSS kustom, dan JavaScript vanilla.

## Fitur

- Menambahkan tugas baru
- Menampilkan daftar tugas berdasarkan waktu dibuat terbaru
- Mengedit tugas melalui dialog
- Menghapus satu tugas dengan konfirmasi
- Memilih dan menghapus beberapa tugas sekaligus
- Menampilkan notifikasi sukses dan error
- Tampilan responsif

## Teknologi

- Python 3
- Flask 3.0.0
- MySQL
- mysql-connector-python
- Jinja2
- Tailwind CSS CDN
- HTML, CSS, dan JavaScript

## Struktur Proyek

```text
todo-list/
├── app.py
├── config.py
├── requirements.txt
├── models/
│   └── task.py
├── routes/
│   └── task_routes.py
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Persyaratan

- Python 3.10 atau lebih baru
- MySQL atau MariaDB
- XAMPP, Laragon, atau MySQL yang dapat dijalankan secara lokal

## Konfigurasi Database

Saat ini koneksi database dikonfigurasi di `config.py`:

```python
host = "localhost"
user = "root"
password = "root"
database = "db_todo"
```

Sesuaikan nilai tersebut dengan konfigurasi MySQL pada komputer Anda.

Buat database dan tabel melalui MySQL:

```sql
CREATE DATABASE IF NOT EXISTS db_todo;
USE db_todo;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Contoh instalasi MySQL bawaan Laragon/XAMPP biasanya menggunakan user `root` dengan password kosong. Jika demikian, ubah nilai `password` di `config.py` menjadi `""`.

## Instalasi

Buka PowerShell di folder proyek, lalu jalankan:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika PowerShell menolak menjalankan script aktivasi, jalankan:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

## Menjalankan Aplikasi

Pastikan layanan MySQL sudah aktif, lalu jalankan:

```powershell
python app.py
```

Buka aplikasi melalui browser:

```text
http://127.0.0.1:5000
```

## Environment Variable

Untuk mengganti secret key Flask, set environment variable berikut sebelum menjalankan aplikasi:

```powershell
$env:FLASK_SECRET_KEY="ganti-dengan-random-secret-key"
python app.py
```

Jika tidak diset, aplikasi membuat secret key acak saat aplikasi dimulai.

## Catatan

- Jalankan MySQL sebelum menjalankan aplikasi.
- Pastikan nama database, user, password, dan host di `config.py` sudah benar.
- Tailwind CSS dimuat dari CDN, sehingga koneksi internet diperlukan untuk memuat utility style Tailwind.
