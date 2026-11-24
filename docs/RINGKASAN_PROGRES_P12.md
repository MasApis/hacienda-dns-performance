# Ringkasan Progres Pertemuan 12 — Hacienda Del Part

**Penelitian:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Tanggal ringkasan:** 24 November 2026  
**Posisi aktual:** Seluruh pekerjaan teknis P12 selesai dan diverifikasi terhadap file: 600 observasi utama terkumpul, cleaning diaudit tanpa penghapusan baris, statistik deskriptif dan notebook tahap pertama tersedia. Logbook hasil pengukuran telah diisi. Yang tersisa: uji keterulangan notebook (P12-10) dan seluruh luaran P13–P15.

Sumber kebenaran metode: [`METODOLOGI.md`](METODOLOGI.md). Status pekerjaan: [`tickets/README.md`](tickets/README.md).

## 1. Pekerjaan yang sudah selesai

- Folder proyek `~/Projects/hacienda-dns`, Git, `.gitignore`, `requirements.txt`, dan `.venv` tersedia; Python **3.12.3**.
- Library `dnspython`, `pandas`, `numpy`, `matplotlib`, `scipy`, `jupyter` terpasang (`openpyxl` ditambahkan terpisah sebagai alat sekali pakai untuk logbook).
- Ketiga resolver menjawab kueri `dig` A `google.com`: Google `8.8.8.8` (10 ms), Cloudflare `1.1.1.1` (9 ms), DNS bawaan jaringan `103.29.106.17` (8 ms). Ini **hanya pemeriksaan konektivitas**, bukan peringkat performa.
- Koneksi publik teridentifikasi PT SOLNET INDONESIA (AS9422); blok IP `103.29.106.17` tercatat atas nama SOLONE PTE LTD. Operator resolver ketiga belum terverifikasi.
- Collector `src/dns_collector.py` lolos `py_compile` dan menghasilkan skema 12 kolom. Tak ada perubahan logika untuk 10 putaran.
- Revisi metodologi satu sesi menggantikan rancangan 3 hari/9 sesi/1.620 observasi yang **dibatalkan**.

## 2. Pilot test — uji alat, bukan hasil utama

| File | `run_id` | Baris | Status |
|---|---|---:|---|
| `data/pilot/dns_pilot.csv` | `9e5e799b056e` | 60 | 30 `ok`, 27 `nxdomain`, 3 `noanswer` |
| `data/pilot/dns_pilot_validasi.csv` | `dc54ebc8b8c7` | 60 | 30 `ok`, 27 `nxdomain`, 3 `noanswer` |

Pilot pertama ≈00.48 WIB, 1 putaran, 20 observasi per resolver (10 `acak`, 10 `ulang`), 0 missing, 0 duplikasi identik. Rata-rata pilot (ms): Cloudflare 36,131 `acak` / 19,745 `ulang`; Google 33,120 / 26,218; DNS bawaan jaringan 41,272 / 15,713. Seluruh `noanswer` pada subdomain acak `github.com`. Data pilot tetap terpisah dari data utama.

## 3. Dataset utama — terverifikasi

`data/raw/dns_data.csv`, 24 November 2026 `04:49:38`–`04:55:20`, `run_id=bfcc6beb3ee9`:

| Pemeriksaan | Hasil |
|---|---|
| Baris × kolom | 600 × 12 |
| Putaran | 10, masing-masing 60 baris |
| Resolver | 200 per resolver |
| Kondisi | 100 per resolver per `acak`/`ulang` |
| Status | 300 `ok`, 270 `nxdomain`, 30 `noanswer` |
| Missing / duplikasi kunci | 0 / 0 |
| `waktu_ms`, `rtt_ms` ≤ 0 | 0 |
| `rtt_ms` unik | 30 (3 resolver × 10 putaran) |

Seluruh 300 baris `acak` berstatus non-OK; seluruh 300 baris `ulang` `ok`. Seluruh 30 `noanswer` berasal dari subdomain acak `github.com` — respons NODATA yang sah. Kolom `sesi` = `malam` dari aturan jam otomatis, bukan variabel analisis.

## 4. Cleaning dan statistik deskriptif

`src/clean_dns.py` memvalidasi dataset dan menghasilkan:

- `data/processed/dataset_cleaned.csv` — 600 baris, **0 dihapus**; NXDOMAIN dan NoAnswer dipertahankan; `timestamp` dinormalisasi dari `T` menjadi spasi (raw tidak berubah).
- `data/processed/dataset_analisis_utama.csv` — **300 baris `ulang` + `ok`**; seluruh kondisi `acak` tidak termasuk.
- `docs/audit_cleaning.txt` — audit 600/300/0 dan keputusan pemertahanan status.

`notebooks/analisis_probstat.ipynb` (cell 1–5 tereksekusi) menghasilkan:

| Kondisi | Google | DNS bawaan jaringan | Cloudflare |
|---|---|---|---|
| `ulang` mean (ms) | 15,266 | 15,291 | 15,323 |
| `ulang` median (ms) | 10,566 | 10,648 | 10,685 |
| `acak` mean (ms) | 26,959 | 27,374 | 28,764 |
| `acak` median (ms) | 14,550 | 14,154 | 14,112 |

Tabel lengkap including jumlah, minimum, maksimum, varians, standar deviasi, Q1–Q3: `data/processed/statistik_query_{ulang,acak}.csv`.

**Interpretasi batas:** perbandingan `acak` vs `ulang` mencampur prosedur dan jenis respons (non-OK vs `ok`). Distribusi ekor panjang (maks 289,9 ms pada `acak`). Belum ada uji hipotesis; mean terendah Google berlaku pada dataset ini saja. 600 baris bukan sampel independen, dan RTT tidak boleh dikorelasikan pada level baris.

## 5. Status dan tindak lanjut

| Pekerjaan | Status | Bukti |
|---|---|---|
| Lingkungan Python, Git, library | Selesai | `requirements.txt`, `.gitignore` |
| Verifikasi tiga resolver | Selesai | catatan konektivitas di bagian 1 |
| Collector dan dua pilot | Selesai | `src/dns_collector.py`, `data/pilot/` |
| Revisi metodologi satu sesi | Selesai | `docs/METODOLOGI.md`, `.docx` |
| Pengukuran utama 600 observasi | Selesai | `data/raw/dns_data.csv` |
| Audit & cleaning | Selesai | `docs/audit_cleaning.txt`, `data/processed/` |
| Statistik deskriptif & notebook P12 | Selesai | `notebooks/analisis_probstat.ipynb`, 2 CSV statistik |
| Logbook hasil pengukuran | Selesai | `docs/LOGBOOK_PENGUMPULAN_DATA_HACIENDA.xlsx` |
| Dokumentasi README/RINGKASAN/ticket | Selesai | `README.md`, file ini, `docs/tickets/` |
| Uji keterulangan notebook (P12-10) | **Belum disetujui** | — |
| P13 EDA & visualisasi | **Belum dimulai** | — |
| P14 probabilitas & inferensi | **Belum dimulai** | — |
| P15 korelasi, regresi, finalisasi | **Belum dimulai** | — |

Collector **tidak boleh dijalankan ulang**: output mode append akan menambah baris ke `data/raw/dns_data.csv`. Perbaikan `ROOT` notebook dan penghapusan cell kosong masuk P12-10, menunggu persetujuan terpisah.

## 6. Kebijakan kualitas penelitian

1. Dataset asli dan pilot tidak diubah; cleaning hanya pada salinan.
2. `NXDOMAIN`, `NoAnswer`, dan status lain tidak dihapus otomatis atau disamakan dengan `ok`.
3. `acak` dan `ulang` dianalisis terpisah; tidak menyimpulkan isi cache resolver.
4. Uji hipotesis dan regresi memperhitungkan domain, putaran, dan pengukuran berulang; korelasi RTT memakai agregat resolver×putaran (n=30).
5. Angka dalam dokumentasi diambil dari file, bukan ingatan. Jika belum dihitung, ditulis **belum dihitung**; jika berkas belum ada, ditulis **belum tersedia**.
