# Hacienda Del Part — DNS Resolution Performance Research

**Judul penelitian:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Subtema:** Network Performance Analysis  
**Mata kuliah:** Probabilitas dan Statistika (INF12107)  
**Status per 24 November 2026:** Persiapan, verifikasi konektivitas resolver, pilot test, dan revisi rancangan selesai. **Pengumpulan dataset utama belum dilaksanakan.**

## Gambaran penelitian
Penelitian kuantitatif komparatif ini membandingkan waktu respons kueri DNS record **A** menggunakan satu laptop dan satu jaringan Wi-Fi pada **satu sesi pengukuran**. Tiga resolver yang diuji:

| Label dalam CSV | Resolver | Alamat IP |
|---|---|---|
| `google` | Google Public DNS | `8.8.8.8` |
| `cloudflare` | Cloudflare DNS | `1.1.1.1` |
| `isp` | DNS bawaan jaringan (identitas operator belum terverifikasi) | `103.29.106.17` |

Alamat ketiga muncul pada konfigurasi DNS koneksi Wi-Fi penelitian. Hasil identifikasi koneksi publik menunjukkan PT SOLNET INDONESIA (AS9422), sedangkan registrasi blok IP `103.29.106.17` menunjukkan SOLONE PTE LTD. **Belum terbukti resolver ketiga dioperasikan langsung oleh ISP.** Label `isp` di CSV dipertahankan demi kompatibilitas dengan collector, sementara laporan menggunakan istilah **DNS bawaan jaringan**.

## Desain pengumpulan data — revisi satu sesi
- **Durasi:** satu sesi pada tanggal dan jam aktual yang dicatat di logbook; **tidak ada perbandingan pagi, siang, dan malam**.
- **Putaran:** `10` dalam satu kali eksekusi collector.
- **Per putaran:** 10 domain × 3 resolver × 2 kondisi kueri = **60 catatan**.
- **Target satu sesi:** **600 baris observasi** (200 per resolver; 100 `acak` dan 100 `ulang` per resolver), termasuk status respons negatif atau gagal.
- **Kondisi `acak`:** kueri ke subdomain acak dari domain pengujian.
- **Kondisi `ulang`:** kueri kedua ke domain yang sama setelah kueri pemanasan.
- Kedua kondisi **bukan bukti terverifikasi** bahwa terjadi cache miss atau cache hit.
- Urutan domain dan resolver diacak; `run_id` membedakan tiap eksekusi.
- `rtt_ms` adalah RTT ICMP dari `ping`, **bukan** waktu kueri DNS. Satu nilai RTT diukur per putaran per resolver dan digunakan pada beberapa observasi DNS; akibatnya 600 baris tidak sepenuhnya independen.

Baca dokumen metode [`docs/REVISI_RANCANGAN_METODOLOGI.docx`](docs/REVISI_RANCANGAN_METODOLOGI.docx) dan catat pelaksanaan dalam [`docs/LOGBOOK_PENGUMPULAN_DATA_HACIENDA_REVISI_1_SESI.xlsx`](docs/LOGBOOK_PENGUMPULAN_DATA_HACIENDA_REVISI_1_SESI.xlsx).

## Struktur repository
```text
hacienda-dns/
├── src/
│   └── dns_collector.py
├── data/
│   ├── pilot/
│   │   └── dns_pilot.csv           # pilot test, 60 observasi
│   ├── raw/
│   │   └── dns_data.csv            # dibuat ketika pengumpulan utama dimulai
│   └── processed/                  # hasil cleaning, belum dibuat
├── notebooks/                     # notebook analisis, belum dibuat
├── docs/
│   ├── REVISI_RANCANGAN_METODOLOGI.docx
│   ├── LOGBOOK_PENGUMPULAN_DATA_HACIENDA_REVISI_1_SESI.xlsx
│   └── RINGKASAN_PROGRES_P12.md
├── .gitignore
├── requirements.txt
└── README.md
```

> Struktur ini mencakup file yang **direncanakan**. Folder atau file yang belum dibuat tidak berarti prosesnya sudah selesai. Bila nama dokumen berbeda di repository, sesuaikan tautan di atas dengan nama akhirnya.

## Instalasi dan pengujian
Persiapan dilakukan di Linux Mint menggunakan Python 3.12.3. Dari akar repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m py_compile src/dns_collector.py
python src/dns_collector.py --help
```

**Perintah pengukuran utama (jalankan hanya satu kali sesuai rencana ketika siap):**

```bash
python src/dns_collector.py --isp 103.29.106.17 --rounds 10
```

Program menulis ke `data/raw/dns_data.csv` dalam mode **append**, sehingga pelaksanaan ulang akan menambah baris, bukan mengganti data lama. Pastikan file dataset utama belum terisi pengukuran yang tidak sengaja. Setelah selesai:

```bash
wc -l data/raw/dns_data.csv
```

Untuk file baru dengan 600 observasi, jumlahnya **601 baris termasuk header**. Periksa `run_id`, status, dan jumlah data, lalu isi logbook. Jangan mengubah dataset mentah, menghapus respons yang tidak diharapkan, atau mengganti label sesi secara fiktif.

## Hasil pilot test — bukan hasil utama
Pilot test dilakukan pada **24 November 2026 sekitar 00.48 WIB** dengan `run_id=9e5e799b056e` (1 putaran):
- 60 observasi, 12 kolom; 20 observasi per resolver (10 `acak`, 10 `ulang`).
- Tidak ditemukan nilai kosong atau baris duplikat identik pada audit awal; RTT tersedia untuk seluruh baris.
- Per resolver: 10 respons `ok`, 9 `nxdomain`, 1 `noanswer`.
- Seluruh `noanswer` terjadi pada subdomain acak `github.com`.
- File pilot diarsipkan terpisah sebagai `data/pilot/dns_pilot.csv` (61 baris termasuk header).

Rata-rata pilot (ms, 10 observasi per sel):

| Resolver | `acak` | `ulang` |
|---|---:|---:|
| Cloudflare | 36,131 | 19,745 |
| Google | 33,120 | 26,218 |
| DNS bawaan jaringan | 41,272 | 15,713 |

Angka pilot **tidak** digunakan untuk menentukan resolver tercepat secara umum. Informasi lengkap ada pada [`docs/RINGKASAN_PROGRES_P12.md`](docs/RINGKASAN_PROGRES_P12.md).

## Rencana analisis sesuai panduan dosen
1. **Pertemuan 12:** kumpulkan data utama, audit/cleaning terpisah, statistik deskriptif (mean, median, minimum, maksimum, varians, standar deviasi, kuartil, dan modus jika relevan).
2. **Pertemuan 13:** eksplorasi distribusi dan outlier; histogram, boxplot, scatter plot.
3. **Pertemuan 14:** simulasi probabilitas, estimasi parameter, serta uji hipotesis sesuai asumsi dan desain pengukuran.
4. **Pertemuan 15:** korelasi Pearson dan regresi linear sederhana, dengan perhatian khusus pada dependensi data RTT; finalisasi laporan dan presentasi.

Perbandingan waktu kueri `acak` dan `ulang` dianalisis terpisah; respons `ok`, `nxdomain`, `noanswer`, dan `timeout` **tidak diperlakukan sebagai kategori yang setara tanpa penjelasan**. Karena pengukuran dilakukan pada satu jaringan dan satu sesi, hasil penelitian tidak dapat digeneralisasikan ke seluruh waktu dan jaringan. Untuk inferensi statistik, pengukuran berulang dan struktur pasangan/domain/putaran harus diperhitungkan.

## Etika dan reproduksibilitas
Pertahankan data mentah, arsipkan pilot secara terpisah, dokumentasikan tanggal serta waktu mulai/selesai aktual, jaringan, perubahan konfigurasi, kendala, dan `run_id`. Semua perubahan metode ditulis secara eksplisit. **Jangan mengklaim pengumpulan data utama, cleaning, atau hasil analisis yang belum dikerjakan.**
