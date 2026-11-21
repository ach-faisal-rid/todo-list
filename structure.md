# Struktur proyek

```text
todo-list/
├── app.py                  # Membuat aplikasi Flask dan mendaftarkan blueprint
├── config.py               # Konfigurasi dan koneksi database
├── requirements.txt        # Dependency Python aplikasi
├── models/
│   ├── __init__.py
│   └── task.py             # Operasi database untuk tugas (CRUD)
├── routes/
│   ├── __init__.py
│   └── task_routes.py      # Endpoint dan validasi request tugas
├── templates/
│   ├── base.html           # Layout bersama, Tailwind CDN, CSS dan JS
│   └── index.html          # Halaman daftar tugas
├── static/
│   ├── css/
│   │   └── style.css       # Komponen dan detail visual khusus aplikasi
│   └── js/
│       └── script.js       # Interaksi pilihan, dialog edit, dan notifikasi
└── structure.md            # Dokumentasi struktur proyek
```

## Pembagian tanggung jawab

- `app.py` menjadi entry point Flask dan mendaftarkan blueprint dari `routes/`.
- `routes/` menangani URL, input form, pesan, dan pemanggilan fungsi model.
- `models/` berisi query database; template tidak mengakses database langsung.
- `templates/base.html` menyimpan kerangka halaman yang dapat digunakan ulang.
  `templates/index.html` hanya berisi konten halaman daftar tugas.
- `static/` menyimpan aset frontend. Tailwind dipakai untuk utility styling,
  sedangkan `static/css/style.css` untuk komponen visual khusus seperti dialog
  dan ilustrasi.
- `requirements.txt` hanya berisi package Python; perintah setup dijalankan di
  terminal dan tidak ditulis sebagai isi file dependency.

Tailwind CSS dimuat melalui CDN di `templates/base.html`. CDN cocok untuk
prototipe atau belajar; untuk deployment produksi, gunakan proses build Tailwind
agar CSS yang dikirim lebih kecil dan tidak bergantung pada CDN.

## Menjalankan aplikasi

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
