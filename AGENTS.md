# AGENTS.md — Panduan Kerja Agent Hacienda Del Part

Dokumen ini adalah **pedoman kerja** untuk AI coding agent yang melanjutkan repository ini. Baca sebelum mengubah apa pun. Ikuti [`docs/METODOLOGI.md`](docs/METODOLOGI.md) untuk detail metode dan [`docs/tickets/`](docs/tickets/) untuk status pelacakan.

## 1. Gambaran project

Repository penelitian Probabilitas dan Statistika (INF12107), semester V, subtema **Network Performance Analysis**. Penelitian kuantitatif komparatif dengan pengukuran berulang dari satu laptop dan satu jaringan Wi-Fi. Objek: tiga resolver DNS, dua kondisi query, satu sesi pengukuran.

Kelompok: **Hacienda Del Part**.

## 2. Tujuan penelitian

Membandingkan waktu resolusi DNS Google, Cloudflare, dan DNS bawaan jaringan memakai statistik deskriptif, EDA, simulasi/inferensi probabilitas, lalu korelasi dan regresi sederhana, dengan memperhatikan desain pengukuran berulang. Luaran akhir: dataset terdokumentasi, notebook yang bisa dijalankan ulang, laporan PDF, draft artikel, dan presentasi sesuai panduan dosen.

## 3. Struktur repository

```text
hacienda-dns/
├── AGENTS.md                         # panduan ini
├── README.md                         # ringkasan, struktur, cara menjalankan
├── requirements.txt                  # pip freeze lingkungan Python 3.12.3
├── .gitignore                        # .venv, cache, PDF referensi
├── src/
│   ├── dns_collector.py              # pengumpul data (dnspython + ping)
│   └── clean_dns.py                  # validasi & cleaning, menghasilkan 3 file
├── data/
│   ├── pilot/                        # 2 file uji alat, TIDAK untuk analisis utama
│   │   ├── dns_pilot.csv
│   │   └── dns_pilot_validasi.csv
│   ├── raw/dns_data.csv              # dataset utama, 600 baris, jangan diubah
│   └── processed/
│       ├── dataset_cleaned.csv                # salinan valid dari raw (600)
│       ├── dataset_analisis_utama.csv         # subset ulang+ok (300)
│       ├── statistik_query_ulang.csv
│       └── statistik_query_acak.csv
├── notebooks/analisis_probstat.ipynb  # notebook tahap pertama (P12)
└── docs/
    ├── METODOLOGI.md                 # metodologi kanonik Markdown
    ├── RINGKASAN_PROGRES_P12.md
    ├── audit_cleaning.txt
    ├── LOGBOOK_PENGUMPULAN_DATA_HACIENDA.xlsx
    ├── Revisi_Rancangan_Penelitian_dan_Metodologi_Hacienda_Del_Part.docx
    ├── references/                   # PDF panduan, diabaikan Git
    └── tickets/                      # P12–P15, indeks di README.md
```

## 4. Teknologi dan dependency

Linux Mint, Python **3.12.3**, virtual environment `.venv`. Dependency utama: `dnspython`, `pandas`, `numpy`, `matplotlib`, `scipy`, `jupyter` (ditambah `openpyxl` sebagai alat sekali pakai untuk mengisi logbook; tidak dimasukkan ke `requirements.txt`). `requirements.txt` adalah pip freeze penuh, bukan daftar minimal. Instal dengan `python -m pip install -r requirements.txt`.

## 5. Penjelasan dataset

Skema 12 kolom: `run_id`, `timestamp`, `sesi`, `putaran`, `resolver`, `ip_resolver`, `domain`, `jenis_cache`, `query_name`, `waktu_ms`, `status`, `rtt_ms`.

Fakta utama yang terverifikasi (24 November 2026, `04:49:38`–`04:55:20`, `run_id=bfcc6beb3ee9`): 600 baris, 10 putaran × 10 domain × 3 resolver × 2 kondisi; 200 baris per resolver; 100 per resolver per kondisi; status 300 `ok`, 270 `nxdomain`, 30 `noanswer`; 0 missing, 0 duplikasi kombinasi pengukuran; 0 nilai `waktu_ms`/`rtt_ms` non-positif.

| Resolver | Label CSV | Alamat |
|---|---|---|
| Google Public DNS | `google` | `8.8.8.8` |
| Cloudflare DNS | `cloudflare` | `1.1.1.1` |
| DNS bawaan jaringan | `isp` | `103.29.106.17` |

Label `isp` dipertahankan demi kompatibilitas kode/CSV. Identitas operator resolver ketiga belum terverifikasi; dalam laporan gunakan **DNS bawaan jaringan**.

Definisi subset:
- `dataset_cleaned.csv` = seluruh 600 baris valid, tidak ada baris dihapus.
- `dataset_analisis_utama.csv` = 300 baris `jenis_cache == "ulang"` **dan** `status == "ok"`; seluruh kondisi `acak` tidak termasuk. Jangan menyebutnya "semua data".

## 6. Aturan metodologi penelitian

1. Desain final: **satu sesi**, 10 putaran, 10 domain, 3 resolver, 2 kondisi query, target 600 observasi. Rancangan lama 3 hari × 3 sesi × 3 putaran (1.620 observasi) **dibatalkan**; jangan dikembalikan ke dokumentasi.
2. `acak` = query ke subdomain acak; `ulang` = query domain yang sama setelah query pemanasan. Keduanya **bukan bukti terverifikasi** cache miss/cache hit.
3. Status respons berbeda tidak setara: `ok`, `nxdomain`, `noanswer`, `timeout`, `no_nameservers` harus dianalisis sesuai maknanya. NXDOMAIN/NoAnswer adalah respons DNS yang sah, bukan otomatis dibuang.
4. **Seluruh 300 baris `acak` berstatus non-OK** (270 NXDOMAIN, 30 NoAnswer); **seluruh 300 baris `ulang` berstatus `ok`**. Perbandingan kedua kondisi juga membandingkan jenis respons — nyatakan ini pada setiap interpretasi.
5. 600 baris **bukan** 600 sampel independen. Pengukuran berulang per putaran dan domain; gunakan unit analisis yang sesuai.
6. `rtt_ms` adalah RTT ICMP rata-rata yang diukur **sekali per resolver per putaran**, lalu dipakai ulang pada 20 baris. Hanya ada 30 nilai RTT unik. Untuk korelasi/regresi, agregasi ke unit resolver×putaran (n=30) atau gunakan metode yang memperhitungkan dependensi; jangan menghitung korelasi Pseudo-replikasi sebagai temuan utama.
7. `waktu_ms` adalah durasi resolusi yang dicatat oleh `dnspython` (termasuk overhead Python dan retry), **bukan** RTT jaringan murni.
8. Kolom `sesi` bernilai `malam` karena aturan otomatis berdasarkan jam mulai; ini warisan desain lama dan tidak dipakai sebagai variabel analisis.
9. Satu jaringan, satu sesi, satu perangkat: hasil tidak digeneralisasikan ke semua jaringan/waktu. Belum ada uji hipotesis yang membuktikan perbedaan signifikan; jangan menyatakan resolver tertentu "paling cepat secara umum".

## 7. Workflow Plan → Approval → Build

1. **Plan:** audit read-only, laporkan temuan, sebutkan file yang akan dibuat/diperbarui/dipertahankan, minta persetujuan.
2. **Approval:** tunggu persetujuan eksplisit sebelum menulis file, mengubah kode, atau menjalankan analisis baru.
3. **Build:** implementasi bertahap sesuai cakupan yang disetujui.
4. **Validation:** jalankan pengecekan yang relevan, tampilkan `git diff`, laporkan bukti.
5. Berhenti dan laporkan bila menemukan error atau ketidaksesuaian penting.
6. Jangan commit/push tanpa persetujuan terpisah.

## 8. Aturan perubahan kode

- Perubahan kecil dan lokal; ikuti pola yang sudah ada. Tanpa abstraksi, opsi, atau fitur yang tidak diminta.
- Sebelum mengubah fungsi, cari semua pemanggilnya. Perbaiki akar masalah sekali di kode bersama.
- `clean_dns.py` bersifat spesifik untuk studi ini (assert 600 baris, 1 run_id, keseimbangan penuh). Jangan melonggarkan guard tanpa alasan dan persetujuan.
- Jika notebook diubah, jalankan ulang dan pastikan CSV hasil tidak berubah secara tidak sengaja.
- Jangan menambah dependency untuk beberapa baris kode.

## 9. Aturan keamanan dataset asli

- `data/raw/dns_data.csv`, `data/pilot/*.csv` **tidak boleh** diubah, ditimpa, dihapus, atau digabung.
- `dns_collector.py` membuka file raw dengan mode **append**. Menjalankan ulang collector akan menambah baris dan merusak dataset 600 observasi. **Jangan jalankan collector** kecuali ada permintaan eksplisit dan prosedur pengumpulan baru yang disetujui.
- Cleaning selalu menghasilkan file baru di `data/processed/`; raw tidak pernah ditulis ulang.
- Data pilot tetap terpisah dari data utama.

## 10. Konvensi penamaan file

- Modul Python: `snake_case.py` (`dns_collector.py`, `clean_dns.py`).
- Dokumentasi Markdown: `UPPER_SNAKE_CASE.md` di `docs/`; `README.md` dan `AGENTS.md` di root.
- Ticket: `P<pertemuan>_<TOPIK>.md` di `docs/tickets/`, sub-ticket `P<pertemuan>-<nomor>`.
- Hasil olahan: `statistik_<kondisi>.csv`, `dataset_<jenis>.csv`.
- Jangan mengganti nama file yang sudah dirujuk dokumentasi tanpa memperbarui semua referensi.

## 11. Pengujian dan validasi

```bash
python -m py_compile src/dns_collector.py src/clean_dns.py
python src/dns_collector.py --help        # hanya help; TIDAK menjalankan pengukuran
wc -l data/raw/dns_data.csv               # harus 601
python src/clean_dns.py                    # menulis ulang file turunan; cek git diff
```

Pemeriksaan data minimum: jumlah baris 600, 1 run_id, 10 putaran × 60, crosstab resolver×kondisi = 100, status 300/270/30, 0 missing, 0 duplikasi kunci. Untuk notebook, cek execution count berurutan dan output tidak kosong. Selalu tampilkan bukti sebelum menyatakan selesai.

## 12. Dokumentasi dan standar commit

- Dokumentasi harus menyebut angka yang diverifikasi dari file, bukan ingatan. Hindari dokumentasi ganda yang bertentangan; arahkan ke satu sumber kanonik.
- Perubahan status ticket disertai path bukti. **Jangan menandai DONE hanya karena file ada** — periksa isinya.
- Pesan commit: Conventional Commits (`docs:`, `feat:`, `fix:`, `refactor:`, `chore:`). Contoh: `docs: add AGENTS.md and meeting 12–15 ticket system`.
- Jangan commit/push otomatis. Ajukan rekomendasi pesan commit dan tunggu persetujuan.

## 13. Cara menjalankan notebook

Notebook `notebooks/analisis_probstat.ipynb` belum diubah dan menentukan root dengan `Path.cwd().resolve().parent`. Jalankan dari direktori `notebooks/`:

```bash
source .venv/bin/activate
cd notebooks
jupyter notebook analisis_probstat.ipynb
```

Atau dari root repo dengan nbconvert (cwd otomatis mengikuti direktori notebook):

```bash
jupyter nbconvert --to notebook --execute notebooks/analisis_probstat.ipynb --output /tmp/opencode/analisis_probstat_executed.ipynb
```

Jalankan sel berurutan. Notebook menulis `data/processed/statistik_query_{ulang,acak}.csv`; periksa `git diff` setelahnya. Perbaikan portabilitas `ROOT` masih menjadi pekerjaan P12-10 dan belum disetujui.

## 14. Status pekerjaan

**Selesai (P12, terverifikasi):** lingkungan & Git, verifikasi resolver, collector, dua pilot test, revisi metodologi satu sesi, pengumpulan 600 observasi, cleaning + audit, statistik deskriptif, notebook tahap pertama.

**Belum selesai:** pengisian narasi hasil di README/RINGKASAN (dilakukan pada Build ini), uji keterulangan notebook (P12-10), seluruh luaran P13 (EDA/visualisasi), P14 (probabilitas/inferensi + presentasi kemajuan), P15 (korelasi/regresi, artikel, laporan PDF, presentasi akhir, petunjuk reproduksi final). Lihat [`docs/tickets/README.md`](docs/tickets/README.md).

## 15. Larangan mengarang

Dilarang mengarang data, angka statistik, status pengerjaan, bukti file, tanggal, `run_id`, atau hasil uji. Jika suatu angka belum dihitung, tulis **belum dihitung**. Jika berkas belum ada, tulis **belum tersedia**. Pisahkan fakta yang terverifikasi dari rencana dan asumsi.
