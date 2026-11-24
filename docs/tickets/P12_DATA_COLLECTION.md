# P12 — Pengumpulan Data, Cleaning, dan Statistik Deskriptif

| Field | Nilai |
|---|---|
| **Ticket ID** | P12 |
| **Judul** | Pengumpulan Data, Cleaning, dan Statistik Deskriptif |
| **Pertemuan** | 12 |
| **Tujuan** | Memiliki dataset empiris yang terdokumentasi, hasil cleaning yang dapat diaudit, dan statistik deskriptif yang dapat direproduksi. |
| **Deskripsi pekerjaan** | Menentukan topik, rumusan masalah, tujuan, dan variabel; menyiapkan lingkungan dan collector; menjalankan pilot; mengumpulkan 600 observasi; memvalidasi dan membersihkan data; menghitung statistik deskriptif pada notebook tahap pertama. |
| **Input** | Panduan dosen, rancangan revisi satu sesi, 10 domain, 3 alamat resolver, Python 3.12.3. |
| **Output yang diharapkan** | Dataset asli & cleaned, logbook terisi, tabel statistik deskriptif, notebook tahap pertama, catatan audit. |
| **Status** | **DONE** (10/10 sub-ticket DONE) |
| **Bukti** | `data/raw/dns_data.csv`, `data/processed/`, `docs/audit_cleaning.txt`, `notebooks/analisis_probstat.ipynb`, `docs/LOGBOOK_PENGUMPULAN_DATA_HACIENDA.xlsx` |
| **Dependensi** | Tidak ada |
| **Catatan kendala & keputusan** | Rancangan 1.620 observasi (3 hari × 3 sesi) dibatalkan; final satu sesi 600 observasi. Data pilot tidak digabung. P12-10 (uji keterulangan notebook) selesai dan terverifikasi. |

## P12-01 — Penentuan topik, rumusan masalah, tujuan, dan variabel

- **Status:** DONE
- **Tujuan:** Menetapkan fokus penelitian dan variabel yang diukur.
- **Deskripsi:** Merumuskan masalah, tujuan, dan daftar variabel sebelum pengumpulan.
- **Input:** Panduan dosen bab C–D, revisi metodologi.
- **Output/Bukti:** `docs/METODOLOGI.md` bagian 1–2 dan 4; `docs/Revisi_Rancangan_Penelitian_dan_Metodologi_Hacienda_Del_Part.docx` bagian 1–4.5.
- **Acceptance criteria:** Topik, rumusan masalah, tujuan, dan variabel numerik/kategorikal tertulis; ada batasan generalisasi.
- **Dependensi:** —
- **Catatan:** Variabel numerik yang dipakai untuk hubungan/regresi: `waktu_ms` dan `rtt_ms`.

## P12-02 — Lingkungan Python dan repository

- **Status:** DONE
- **Tujuan:** Menyiapkan lingkungan yang dapat direproduksi.
- **Deskripsi:** Membuat venv, menginstal library, menyiapkan Git dan `.gitignore`.
- **Input:** Linux Mint, Python 3.12.3.
- **Output/Bukti:** `requirements.txt`, `.gitignore`, riwayat Git `548eaab..c94cd49`.
- **Acceptance criteria:** `python -m pip install -r requirements.txt` berhasil; `.venv` tidak terlacak.
- **Dependensi:** —
- **Catatan:** `openpyxl` dipasang terpisah sebagai alat sekali pakai untuk P12-08.

## P12-03 — Pengembangan collector

- **Status:** DONE
- **Tujuan:** Memiliki skrip pengumpul yang menghasilkan skema data yang disepakati.
- **Deskripsi:** Implementasi 10 domain, pengacakan urutan, dua kondisi query, RTT, status, timestamp, run ID, dan penulisan CSV.
- **Input:** Rancangan revisi satu sesi.
- **Output/Bukti:** `src/dns_collector.py` (di-rename dari `dns-collector.py` pada Build ini).
- **Acceptance criteria:** Sintaks valid; 12 kolom sesuai kontrak; `--rounds` dan `--isp` tersedia; pengacakan domain/resolver aktif.
- **Dependensi:** P12-02
- **Catatan:** Skrip membuka output dengan mode append — eksekusi ulang dilarang setelah data lengkap.

## P12-04 — Pilot test dan arsip terpisah

- **Status:** DONE
- **Tujuan:** Menguji alat sebelum pengukuran utama.
- **Deskripsi:** Menjalankan dua pilot 1 putaran (60 observasi) dan mengarsipkannya terpisah.
- **Input:** Collector, koneksi Wi-Fi yang sama.
- **Output/Bukti:** `data/pilot/dns_pilot.csv` (`run_id=9e5e799b056e`), `data/pilot/dns_pilot_validasi.csv` (`run_id=dc54ebc8b8c7`).
- **Acceptance criteria:** Masing-masing 60 baris; status 30 `ok` / 27 `nxdomain` / 3 `noanswer`; tidak masuk dataset utama.
- **Dependensi:** P12-03
- **Catatan:** Angka mean pilot di README sesuai `dns_pilot.csv`; bukan hasil utama.

## P12-05 — Pengumpulan dataset utama 600 observasi

- **Status:** DONE
- **Tujuan:** Memperoleh dataset empiris sesuai target final.
- **Deskripsi:** Menjalankan satu sesi 10 putaran pada 24 November 2026.
- **Input:** Collector, `--isp 103.29.106.17 --rounds 10`.
- **Output/Bukti:** `data/raw/dns_data.csv` (601 baris termasuk header), `run_id=bfcc6beb3ee9`, timestamp `04:49:38`–`04:55:20`.
- **Acceptance criteria:** 600 baris; 200 per resolver; 100 per resolver per kondisi; 1 run_id; 0 missing/duplikasi kunci; status 300 `ok`, 270 `nxdomain`, 30 `noanswer`.
- **Dependensi:** P12-04
- **Catatan:** Tidak ada pengambilan data tambahan selama audit maupun Build ini.

## P12-06 — Cleaning dan audit data

- **Status:** DONE
- **Tujuan:** Menghasilkan salinan bersih tanpa mengubah data mentah.
- **Deskripsi:** Validasi skema, tipe, missing, duplikasi, kategori, dan rentang nilai; ekspor subset analisis.
- **Input:** `data/raw/dns_data.csv`.
- **Output/Bukti:** `src/clean_dns.py`, `data/processed/dataset_cleaned.csv` (600), `data/processed/dataset_analisis_utama.csv` (300), `docs/audit_cleaning.txt`.
- **Acceptance criteria:** 0 baris dihapus; NXDOMAIN/NoAnswer dipertahankan; subset = `ulang` + `ok`; audit menyebut 600/300/0.
- **Dependensi:** P12-05
- **Catatan:** `dataset_analisis_utama.csv` tidak memuat kondisi `acak`; definisi ini wajib disebut pada setiap pemakaian.

## P12-07 — Statistik deskriptif dan notebook tahap pertama

- **Status:** DONE
- **Tujuan:** Menghasilkan ringkasan deskriptif yang dapat dijalankan ulang.
- **Deskripsi:** Menghitung jumlah, mean, median, min, maks, varians, standar deviasi, Q1/Q2/Q3 per resolver untuk dua kondisi.
- **Input:** `data/processed/dataset_cleaned.csv`.
- **Output/Bukti:** `notebooks/analisis_probstat.ipynb` (cell 1–5 tereksekusi), `data/processed/statistik_query_ulang.csv`, `data/processed/statistik_query_acak.csv`.
- **Acceptance criteria:** Angka sesuai file: `ulang` mean 15,266 / 15,291 / 15,323 ms (Google / ISP / Cloudflare); `acak` mean 26,959 / 27,374 / 28,764 ms. Notebook menyatakan belum ada uji signifikansi.
- **Dependensi:** P12-06
- **Catatan:** Seluruh 300 baris `acak` non-OK dan seluruh 300 `ulang` `ok`, jadi perbandingan kondisi mencampur jenis respons.

## P12-08 — Pengisian logbook hasil pengukuran

- **Status:** DONE
- **Tujuan:** Merekam bukti administratif pengukuran yang sebenarnya terjadi.
- **Deskripsi:** Mengisi sheet "Logbook 1 Sesi" dan memperbarui ringkasan pada file Excel.
- **Input:** Timestamp dan ringkasan dari `data/raw/dns_data.csv`, `docs/audit_cleaning.txt`.
- **Output/Bukti:** `docs/LOGBOOK_PENGUMPULAN_DATA_HACIENDA.xlsx`.
- **Acceptance criteria:** Baris 1 berisi tanggal 24-11-2026, sesi `malam`, mulai `04:49:38`, selesai `04:55:20`, `run_id=bfcc6beb3ee9`, lokasi BESI HIJAU, 10 putaran, 600 baris, status SELESAI, OK 300 / NXDOMAIN 270 / NoAnswer 30; ringkasan tidak lagi menyebut "belum dikumpulkan".
- **Dependensi:** P12-05, P12-06
- **Catatan:** Diisi dengan `openpyxl` pada Build ini; workbook diatur agar menghitung ulang saat dibuka.

## P12-09 — Dokumentasi dan bukti P12

- **Status:** DONE
- **Tujuan:** Menghilangkan dokumentasi yang bertentangan dengan data aktual.
- **Deskripsi:** Menyelaraskan README, ringkasan progres, metodologi Markdown, dan sistem ticket.
- **Input:** Hasil audit read-only tanggal 24 November 2026.
- **Output/Bukti:** `README.md`, `docs/RINGKASAN_PROGRES_P12.md`, `docs/METODOLOGI.md`, `AGENTS.md`, `docs/tickets/`.
- **Acceptance criteria:** Tidak ada klaim "data utama belum dikumpulkan"; semua path dan perintah terminal merujuk ke file yang ada; rancangan 1.620 tidak muncul sebagai rencana aktif.
- **Dependensi:** P12-01…P12-08
- **Catatan:** PDF panduan dosen disimpan lokal dan diabaikan Git.

## P12-10 — Uji keterulangan notebook

- **Status:** DONE
- **Tujuan:** Memastikan notebook dapat dijalankan dari root repository tanpa kegagalan path.
- **Deskripsi:** Perbaiki penentuan `ROOT` agar naik satu level bila dataset tidak ditemukan di `cwd`, hapus cell kosong, lalu jalankan ulang dan bandingkan CSV hasil.
- **Input:** `notebooks/analisis_probstat.ipynb`.
- **Output/Bukti:** `notebooks/analisis_probstat.ipynb` (6 cell, 0 kosong, execution count 1–5); `data/processed/statistik_query_ulang.csv` dan `statistik_query_acak.csv` (hash SHA-256 identik sebelum/sesudah).
- **Acceptance criteria:** Notebook berhasil dijalankan dari root; `statistik_query_*.csv` tidak berubah selain format yang disengaja; tidak ada cell kosong.
- **Dependensi:** P12-07
- **Catatan:** Diverifikasi dari root repository **dan** dari folder `notebooks/`; `data/` tidak berubah. Path lama (`Path.cwd().resolve().parent`) dari root menunjuk ke `/home/masapis/Projects/data/processed/...` yang tidak ada.
