# Ringkasan Progres Pertemuan 12 — Hacienda Del Part

**Penelitian:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Tanggal ringkasan:** 24 November 2026  
**Posisi aktual:** Persiapan, pilot test, audit pilot, pengarsipan, dan **revisi rancangan satu sesi** telah dilakukan. **Belum ada dataset utama 600 observasi dan belum ada hasil statistik deskriptif dataset utama.**

## 1. Pekerjaan yang sudah selesai
- Folder proyek Linux Mint: `~/Projects/hacienda-dns`; Git, `.gitignore`, `requirements.txt`, dan lingkungan `.venv` tersedia.
- Python **3.12.3** dan library `dnspython`, `pandas`, `numpy`, `matplotlib`, `scipy`, `jupyter` berhasil diperiksa.
- Collector pada `src/dns_collector.py` lolos pemeriksaan sintaks dan berhasil dijalankan pada pilot test. **Tidak diperlukan perubahan kode** hanya untuk mengganti jumlah putaran dari 3 menjadi 10.
- Ketiga resolver dapat menjawab kueri `dig` record A `google.com`: Google `8.8.8.8` (10 ms), Cloudflare `1.1.1.1` (9 ms), DNS bawaan jaringan `103.29.106.17` (8 ms). Ini **masing-masing hanya satu pemeriksaan konektivitas**, bukan peringkat performa.
- Koneksi internet publik teridentifikasi sebagai PT SOLNET INDONESIA (AS9422); IP DNS ketiga tercatat atas nama SOLONE PTE LTD. Pengelola operasional resolver ketiga belum terverifikasi.

## 2. Pilot test dan audit awal
- **Tanggal:** 24 November 2026 sekitar **00.48 WIB**.
- **Run ID:** `9e5e799b056e`; sesi otomatis `malam`; **1 putaran = 60 observasi**.
- **Struktur:** 12 kolom; 20 observasi/resolver, masing-masing 10 `acak` dan 10 `ulang`.
- **Pemeriksaan:** missing value 0; duplikasi baris identik 0; RTT kosong 0.
- **Status per resolver:** 10 `ok`, 9 `nxdomain`, 1 `noanswer`. `noanswer` ditemukan pada subdomain acak `github.com` di ketiga resolver. Penyebab spesifiknya belum diverifikasi.
- **Arsip:** `data/pilot/dns_pilot.csv` berisi 61 baris termasuk header. Setelah dipindahkan, `data/raw/` telah dicek kosong.

| Resolver | Mean `acak` (ms) | Mean `ulang` (ms) |
|---|---:|---:|
| Cloudflare | 36,131 | 19,745 |
| Google | 33,120 | 26,218 |
| DNS bawaan jaringan | 41,272 | 15,713 |

**Interpretasi:** Ini adalah data uji alat, bukan hasil penelitian utama. Sampel kecil, kondisi query berbeda, dan kemungkinan ketergantungan antarobservasi membatasi interpretasi statistik.

## 3. Keputusan revisi metodologi
**Rancangan sebelumnya (dibatalkan):** 3 hari × 3 sesi/hari × 3 putaran/sesi = **1.620 observasi**.

**Rancangan terbaru (berlaku):**
- **Satu sesi pengukuran** pada tanggal dan jam aktual yang akan dicatat (tidak ada analisis perbedaan pagi/siang/malam).
- **10 putaran dalam satu eksekusi collector**.
- 10 domain × 3 resolver × 2 kondisi × 10 putaran = **600 observasi target** (200 per resolver).
- Dua kondisi tetap disebut **`acak`** (subdomain acak) dan **`ulang`** (kueri kedua setelah pemanasan), bukan cache hit/miss yang terbukti.
- `103.29.106.17` disebut **DNS bawaan jaringan**; label kode `isp` tetap dipertahankan agar data konsisten.
- Data pilot tetap **terpisah** dari dataset utama; data utama tidak boleh diisi dengan data pilot.
- Satu sesi membatasi generalisasi lintas waktu dan jaringan. **600 baris bukan berarti 600 sampel independen.** RTT diukur per resolver dan putaran sehingga diperlukan penanganan yang tepat dalam analisis hubungan.

Rancangan tertulis: `docs/REVISI_RANCANGAN_METODOLOGI.docx`. Logbook terbaru: `docs/LOGBOOK_PENGUMPULAN_DATA_HACIENDA_REVISI_1_SESI.xlsx`.

## 4. Status dan tindak lanjut
| Pekerjaan | Status |
|---|---|
| Lingkungan Python dan Git | Selesai |
| Verifikasi respons ketiga resolver | Selesai |
| Collector dan pilot test 60 observasi | Selesai |
| Audit dan arsip pilot | Selesai |
| Revisi rancangan/metodologi satu sesi | Selesai |
| Perubahan kode collector untuk 10 putaran | Tidak diperlukan |
| Revisi logbook Excel satu sesi | Selesai disiapkan; harus disimpan dalam repository |
| Perbarui README dan ringkasan ini | Disiapkan; harus disalin ke repository |
| Pengukuran utama 600 observasi | **Belum dilaksanakan** |
| Audit/cleaning dataset utama | **Belum dilaksanakan** |
| Statistik deskriptif dan notebook P12 | **Belum dilaksanakan** |

**Ketika siap mengumpulkan data utama:**

```bash
python src/dns_collector.py --isp 103.29.106.17 --rounds 10
```

Pastikan `data/raw/dns_data.csv` belum berisi hasil percobaan; untuk file baru, target setelah eksekusi adalah **601 baris termasuk header**. Catat `run_id`, waktu aktual, kondisi jaringan, jumlah baris, status, dan gangguan pada Excel. Hindari eksekusi ulang tanpa alasan karena collector menggunakan mode **append**.

## 5. Kebijakan kualitas penelitian
1. Dataset asli tidak diubah; cleaning dikerjakan pada salinan dan keputusan dicatat.
2. `NXDOMAIN`, `NoAnswer`, dan timeout tidak dihapus otomatis atau disamakan dengan query sukses.
3. Perbandingan `acak` dan `ulang` dilakukan terpisah; jangan menyimpulkan isi cache resolver secara pasti.
4. Uji hipotesis mempertimbangkan domain, putaran, dan pengukuran berulang, bukan memperlakukan semua 600 baris sebagai independen.
5. Hasil penelitian belum boleh dinyatakan sampai data utama terkumpul dan dianalisis.
