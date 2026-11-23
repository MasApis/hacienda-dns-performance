# Hacienda Del Part — DNS Resolution Performance Research

**Judul:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Subtema:** Network Performance Analysis  
**Mata kuliah:** Probabilitas dan Statistika (INF12107)  
**Status:** Pertemuan 12 — persiapan dan pilot test selesai; pengumpulan data utama terjadwal.

## Orang-orang hebat
**Al Adhlu Sodri Niwrad**
--------------------------------------------
**Azizul Rizki Mahadi**
**Dzaky Ribal Faiz**
--------------------------------------------
**Farhan Dwi Saputra**
**Muhammad Al Fikry Akbar**
**Akbar Rizki Lingga**
**Bayu Adhandika**
**Abdul Hafidz**

## Ringkasan
Penelitian kuantitatif berbasis pengukuran langsung yang membandingkan waktu penyelesaian kueri DNS record A dari satu laptop dan jaringan Wi-Fi yang sama. Resolver yang dibandingkan: **Google Public DNS (`8.8.8.8`)**, **Cloudflare (`1.1.1.1`)**, dan **DNS bawaan jaringan (`103.29.106.17`)**. Alamat ketiga terkonfigurasi pada koneksi yang digunakan, tetapi status sebagai resolver yang dioperasikan langsung oleh ISP **belum terverifikasi**. Koneksi internet publik teridentifikasi sebagai PT SOLNET INDONESIA (AS9422); registrasi blok IP DNS ketiga tercatat atas nama SOLONE PTE LTD.

Setiap pengukuran mencatat waktu kueri (ms), RTT ICMP (ms), status DNS, resolver, domain, kondisi pengujian, timestamp, putaran, sesi dan `run_id`. Kondisi `acak` menggunakan subdomain acak; `ulang` adalah kueri kedua terhadap domain yang telah dipanaskan. **Kedua label tersebut bukan bukti pasti cache miss/cache hit.** RTT ICMP dan waktu kueri DNS merupakan dua metrik berbeda.

## Rancangan pengumpulan data
- Periode: **24–26 November 2026**, waktu Indonesia Barat (WIB).
- Tiga sesi per hari: **08.00 (pagi), 13.00 (siang), 20.00 (malam)**; tiga putaran tiap sesi.
- Setiap putaran: 10 domain × 3 resolver × 2 kondisi = **60 observasi**.
- Target: **180 observasi/sesi**, **540 observasi/hari**, **1.620 observasi/3 hari**. Ini jumlah baris, **bukan** jaminan semua respons `ok`.
- Gunakan satu laptop, satu koneksi Wi-Fi yang sama, dan pengaturan pengujian yang tidak berubah selama penelitian.
- Detail jadwal, aturan wajib, dan format catatan: [`docs/LOGBOOK_PENGUMPULAN_DATA.md`](docs/LOGBOOK_PENGUMPULAN_DATA.md).

## Struktur project
```text
hacienda-dns/
├── src/dns_collector.py        # kode pengumpul data
├── data/pilot/dns_pilot.csv    # dataset percobaan (60 observasi)
├── data/raw/dns_data.csv      # dataset utama, dibuat saat pengukuran
├── data/processed/            # dataset hasil cleaning (tahap berikutnya)
├── notebooks/                 # notebook statistik (tahap berikutnya)
├── docs/
│   ├── LOGBOOK_PENGUMPULAN_DATA.md
│   └── RINGKASAN_PROGRES_P12.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Persiapan dan cara menjalankan
Python 3.12 digunakan saat persiapan. Pastikan terminal ada di akar repository.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m py_compile src/dns_collector.py
```

Jalankan pada jam yang **benar-benar sesuai**, bukan dengan mengganti label sesi pada waktu lain:

```bash
# 08.00 WIB
python src/dns_collector.py --isp 103.29.106.17 --rounds 3 --sesi pagi
# 13.00 WIB
python src/dns_collector.py --isp 103.29.106.17 --rounds 3 --sesi siang
# 20.00 WIB
python src/dns_collector.py --isp 103.29.106.17 --rounds 3 --sesi malam
```

Program **menambahkan** baris ke `data/raw/dns_data.csv` (append), tidak menimpa file sebelumnya. Jangan menjalankan ulang sesi yang sudah berhasil tanpa menulis alasan dan identitas `run_id` pada logbook. Simpan file mentah apa adanya dan buat salinan untuk cleaning.

## Ringkasan pilot test (24 November 2026, 00.48 WIB)
- `run_id`: `9e5e799b056e`, sesi `malam`, 1 putaran.
- 60 observasi, 12 kolom, 20 observasi per resolver; masing-masing 10 `acak` + 10 `ulang`.
- Tidak ditemukan missing value dan baris identik berdasarkan pemeriksaan awal.
- Per resolver: 10 `ok`, 9 `nxdomain`, 1 `noanswer`; ketiga kasus `noanswer` terjadi pada subdomain acak `github.com`.
- File pilot telah diarsipkan sebagai `data/pilot/dns_pilot.csv` (61 baris termasuk header) dan dipisahkan dari data utama.
- Angka pilot **bukan** kesimpulan tentang DNS tercepat. Detail ada di [`docs/RINGKASAN_PROGRES_P12.md`](docs/RINGKASAN_PROGRES_P12.md).

## Rencana analisis
1. **Pertemuan 12:** audit, cleaning, mean, median, min–max, varians, standar deviasi, kuartil.
2. **Pertemuan 13:** EDA, histogram, boxplot, scatter plot, interpretasi.
3. **Pertemuan 14:** simulasi probabilitas, estimasi, uji hipotesis.
4. **Pertemuan 15:** korelasi Pearson, regresi linear sederhana, laporan dan presentasi akhir.

**Catatan:** Hasil berdasarkan `acak` dan `ulang` dianalisis terpisah; respons `ok`, `nxdomain`, dan `noanswer` tidak digabung tanpa menjelaskan perbedaannya. Pengukuran gagal juga tetap dilacak sebagai outcome, bukan dihapus diam-diam.

## Reproduksibilitas
Jangan mengubah data mentah, parameter collector, daftar domain, resolver, atau koneksi secara diam-diam selama pengumpulan. Catat setiap penyimpangan nyata, termasuk keterlambatan jadwal, kehilangan koneksi, restart, atau eksekusi tambahan. Dokumentasi ini merupakan ringkasan keputusan penting, bukan transkrip percakapan lengkap.
