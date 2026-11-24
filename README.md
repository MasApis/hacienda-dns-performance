# Hacienda Del Part — Analisis Waktu Resolusi DNS

**Judul:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Subtema:** Network Performance Analysis · **Mata kuliah:** Probabilitas dan Statistika (INF12107)  
**Status per 24 November 2026:** Pertemuan 12 selesai dan terverifikasi — 600 observasi terkumpul, cleaning diaudit, statistik deskriptif tersedia. P13–P15 belum dikerjakan.

Panduan kerja agent: [`AGENTS.md`](AGENTS.md) · Metodologi kanonik: [`docs/METODOLOGI.md`](docs/METODOLOGI.md) · Progres: [`docs/RINGKASAN_PROGRES_P12.md`](docs/RINGKASAN_PROGRES_P12.md) · Ticket: [`docs/tickets/`](docs/tickets/README.md)

## Gambaran penelitian

Penelitian kuantitatif komparatif dengan pengukuran berulang pada **satu laptop, satu jaringan Wi-Fi, satu sesi**. Objek: tiga resolver DNS, dua kondisi query, 10 putaran, 10 domain.

| Label CSV | Resolver | Alamat IP |
|---|---|---|
| `google` | Google Public DNS | `8.8.8.8` |
| `cloudflare` | Cloudflare DNS | `1.1.1.1` |
| `isp` | DNS bawaan jaringan | `103.29.106.17` |

Alamat ketiga terbaca pada konfigurasi DNS koneksi Wi-Fi. Identifikasi publik menunjukkan PT SOLNET INDONESIA (AS9422), sementara blok IP tercatat atas nama SOLONE PTE LTD. **Operator resolver ketiga belum terverifikasi**: label `isp` dipertahankan pada kode/CSV demi kompatibilitas, tetapi laporan memakai istilah **DNS bawaan jaringan**.

## Desain dan metadata pengukuran

- Satu sesi, **24 November 2026 `04:49:38`–`04:55:20` WIB**, `run_id=bfcc6beb3ee9`. Rancangan lama 3 hari/1.620 observasi **dibatalkan**.
- 10 putaran × 10 domain × 3 resolver × 2 kondisi = **600 observasi** (200 per resolver; 100 per resolver per kondisi).
- `acak` = query subdomain acak; `ulang` = query domain yang sama setelah query pemanasan. Keduanya **bukan bukti cache miss/hit**.
- Urutan domain dan resolver diacak tiap putaran.
- `waktu_ms` = durasi resolusi `dnspython` (termasuk overhead Python dan retry), **bukan** RTT jaringan murni.
- `rtt_ms` = RTT ICMP rata-rata, diukur **sekali per resolver per putaran** lalu dipakai pada 20 baris. Hanya ada 30 nilai unik; 600 baris **bukan** 600 sampel independen.
- Kolom `sesi` bernilai `malam` dari aturan otomatis jam mulai; warisan desain lama, bukan variabel analisis.

## Struktur repository

```text
hacienda-dns/
├── AGENTS.md
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── dns_collector.py            # pengumpul (dnspython + ping)
│   └── clean_dns.py                # validasi & cleaning
├── data/
│   ├── pilot/                      # 2 file uji alat, terpisah dari data utama
│   │   ├── dns_pilot.csv
│   │   └── dns_pilot_validasi.csv
│   ├── raw/dns_data.csv            # dataset utama, 600 baris — JANGAN diubah
│   └── processed/
│       ├── dataset_cleaned.csv                 # 600 baris valid
│       ├── dataset_analisis_utama.csv          # 300 baris `ulang` + `ok`
│       ├── statistik_query_ulang.csv
│       └── statistik_query_acak.csv
├── notebooks/analisis_probstat.ipynb
└── docs/
    ├── METODOLOGI.md
    ├── RINGKASAN_PROGRES_P12.md
    ├── audit_cleaning.txt
    ├── LOGBOOK_PENGUMPULAN_DATA_HACIENDA.xlsx
    ├── Revisi_Rancangan_Penelitian_dan_Metodologi_Hacienda_Del_Part.docx
    ├── references/                 # PDF panduan, lokal, diabaikan Git
    └── tickets/                    # P12–P15
```

## Instalasi dan validasi

Linux Mint, Python 3.12.3. Dari akar repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m py_compile src/dns_collector.py src/clean_dns.py
python src/dns_collector.py --help
wc -l data/raw/dns_data.csv        # harus 601 termasuk header
```

> **Jangan jalankan `dns_collector.py` untuk pengukuran.** Skrip membuka `data/raw/dns_data.csv` dalam mode **append**; eksekusi ulang akan menambah baris dan merusak dataset 600 observasi. `--help` aman dan tidak mengukur apa pun.

Untuk menjalankan ulang cleaning (menulis ulang file di `data/processed/`, bukan raw):

```bash
python src/clean_dns.py
git diff -- data/processed/
```

Notebook P12 ditulis untuk dijalankan dari direktori `notebooks/`:

```bash
cd notebooks && jupyter notebook analisis_probstat.ipynb
```

Penentuan `ROOT` toleran terhadap direktori eksekusi (P12-10 selesai): notebook dapat dijalankan dari root repository maupun dari folder `notebooks/`.

## Hasil P12 — dataset utama (terverifikasi)

`data/raw/dns_data.csv`: 600 baris, 12 kolom, 0 missing, 0 duplikasi kunci, 0 nilai `waktu_ms`/`rtt_ms` non-positif. Status: **300 `ok`, 270 `nxdomain`, 30 `noanswer`**. Seluruh 30 `noanswer` berasal dari subdomain acak `github.com` (respons NODATA yang sah).

`data/processed/dataset_cleaned.csv` = 600 baris tanpa penghapusan. `dataset_analisis_utama.csv` = **300 baris `jenis_cache == "ulang"` dan `status == "ok"`**; seluruh kondisi `acak` tidak termasuk, sehingga jangan menyebutnya "semua data".

Rata-rata waktu resolusi (ms):

| Kondisi / status | Google | DNS bawaan jaringan | Cloudflare |
|---|---:|---:|---:|
| `ulang`, `ok` (n=100/resolver) | 15,266 | 15,291 | 15,323 |
| `acak`, non-OK (n=100/resolver) | 26,959 | 27,374 | 28,764 |

Median pada `ulang`: 10,566 / 10,648 / 10,685 ms. Statistik lengkap (jumlah, minimum, maksimum, varians, standar deviasi, Q1/Q2/Q3): [`data/processed/statistik_query_ulang.csv`](data/processed/statistik_query_ulang.csv) dan [`statistik_query_acak.csv`](data/processed/statistik_query_acak.csv).

**Batasan interpretasi:** seluruh 300 baris `acak` berstatus non-OK (270 NXDOMAIN, 30 NoAnswer), sedangkan seluruh 300 baris `ulang` `ok`. Perbandingan dua kondisi juga membandingkan **jenis respons**, bukan hanya prosedur cache. Distribusi berekor panjang (maksimum 289,9 ms pada `acak`), sehingga mean mudah dipengaruhi outlier. Belum ada uji hipotesis; Google memiliki mean terendah **pada dataset ini**, bukan bukti keunggulan umum.

## Pilot test — bukan hasil utama

`data/pilot/dns_pilot.csv`, 24 November 2026 ≈00.48 WIB, `run_id=9e5e799b056e`: 60 observasi, 1 putaran, status 30 `ok` / 27 `nxdomain` / 3 `noanswer`. `dns_pilot_validasi.csv` (`run_id=dc54ebc8b8c7`) berisi 60 observasi dengan komposisi sama. Keduanya tidak digabung ke dataset utama dan tidak dipakai untuk kesimpulan.

## Rencana dan ticket

| Pertemuan | Fokus | Status tiket |
|---|---|---|
| P12 | Pengumpulan, cleaning, statistik deskriptif | DONE |
| P13 | EDA, ≥3 visualisasi, outlier, notebook tahap 2 | TODO |
| P14 | Distribusi, simulasi, uji hipotesis α=0,05, presentasi kemajuan (30 Nov–4 Des 2026) | TODO |
| P15 | Korelasi/regresi pada unit agregat n=30, artikel, laporan PDF, presentasi akhir (7–11 Des 2026), reproduksi | TODO |

Detail 40 sub-ticket ada di [`docs/tickets/README.md`](docs/tickets/README.md). Pekerjaan P13 baru dimulai setelah persetujuan terpisah.

## Etika dan reproduksibilitas

Dataset asli dan pilot tidak diubah; cleaning menghasilkan file baru. NXDOMAIN/NoAnswer dipertahankan. Korelasi dan regresi harus memakai agregat resolver×putaran (n=30) atau metode yang memperhitungkan dependensi. Satu perangkat, satu jaringan, satu sesi: hasil tidak digeneralisasikan ke waktu/jaringan lain. Jangan mengarang angka, status, atau bukti file yang belum ada.
