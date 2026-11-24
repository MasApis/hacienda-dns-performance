# Indeks Ticket Project — Hacienda Del Part

Sistem pelacakan P12–P15. Setiap ticket memuat sub-ticket bernomor agar seluruh pekerjaan dapat dilacak dari awal sampai final. **Status ditentukan dari bukti, bukan dari keberadaan file.**

## Status ticket

| ID | Judul | Pertemuan | Status | Bukti utama | Dependensi |
|---|---|---|---|---|---|
| [P12](P12_DATA_COLLECTION.md) | Pengumpulan Data, Cleaning, dan Statistik Deskriptif | 12 | **DONE** | `data/raw/dns_data.csv`, `docs/audit_cleaning.txt`, `notebooks/analisis_probstat.ipynb` | — |
| [P13](P13_EDA_VISUALIZATION.md) | Exploratory Data Analysis dan Visualisasi | 13 | **TODO** | belum tersedia | P12 |
| [P14](P14_PROBABILITY_INFERENCE.md) | Simulasi Probabilitas dan Inferensi Statistik | 14 | **TODO** | belum tersedia | P13 |
| [P15](P15_FINAL_ANALYSIS.md) | Korelasi, Regresi, dan Finalisasi | 15 | **TODO** | belum tersedia | P14 |

**Arti status:**
- `TODO` — belum dikerjakan.
- `IN PROGRESS` — sedang dikerjakan, bukti sebagian.
- `DONE` — bukti diperiksa dan acceptance criteria terpenuhi.
- `BLOCKED` — ada ketergantungan/keputusan yang belum terselesaikan.

P12 dinyatakan **DONE**: 10 dari 10 sub-ticket selesai, termasuk logbook dan uji keterulangan notebook. Lihat detail di ticket.

## Aturan pembaruan

1. Update status hanya setelah memeriksa isi bukti: jumlah baris, angka, execution count, atau output aktual.
2. Cantumkan path file relatif terhadap root repository pada kolom bukti.
3. Jika terjadi penyimpangan metode atau kendala, tulis di catatan sub-ticket pada hari itu juga; jangan menyesuaikan angka.
4. Tidak ada commit/push otomatis. Rekomendasi pesan commit dicantumkan di bagian akhir ticket P15.
5. Validasi terhadap panduan sumber: `docs/references/INF12107 - Panduan Project Probabilitas dan Statistika.pdf` (tersedia lokal, diabaikan Git). Untuk file yang belum dibuat, tulis **belum tersedia**.

## Pemetaan luaran panduan dosen

| Pertemuan | Luaran wajib panduan | Bukti di repository |
|---|---|---|
| P12 | Topik, rumusan masalah, tujuan, variabel, dataset asli + cleaned, statistik deskriptif, notebook tahap 1 | `docs/METODOLOGI.md`, `docs/Revisi_Rancangan_Penelitian_dan_Metodologi_Hacienda_Del_Part.docx`, `data/raw/dns_data.csv`, `data/processed/`, `notebooks/analisis_probstat.ipynb` |
| P13 | ≥3 visualisasi, interpretasi tiap grafik, identifikasi distribusi & outlier, notebook tahap 2, draft hasil | belum tersedia |
| P14 | Distribusi & simulasi, estimasi, uji hipotesis α=0,05, notebook tahap 3, presentasi kemajuan (30 Nov–4 Des 2026) | belum tersedia |
| P15 | Korelasi Pearson, regresi, artikel, laporan PDF, presentasi akhir (7–11 Des 2026), README reproduksi, kelengkapan luaran | belum tersedia |

Struktur pengumpulan akhir menurut panduan (bab I): `PROJECT_PROBSTAT_NAMA_KELOMPOK/` berisi `01_DATASET/`, `02_NOTEBOOK/`, `03_ARTIKEL/`, `04_LAPORAN/`, `05_PRESENTASI/`, dan `README.txt`. Belum dibuat; masuk P15-09.
