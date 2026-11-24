# Metodologi Penelitian — Hacienda Del Part

Dokumen ini adalah **sumber kebenaran Markdown** untuk desain dan definisi variabel. Rancangan asli dalam bentuk Word ada di [`Revisi_Rancangan_Penelitian_dan_Metodologi_Hacienda_Del_Part.docx`](Revisi_Rancangan_Penelitian_dan_Metodologi_Hacienda_Del_Part.docx). Bila keduanya berbeda, angka yang terverifikasi di repository ini yang dipakai dan perbedaan dicatat.

## 1. Identitas dan desain

| Komponen | Keterangan |
|---|---|
| Judul | Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika |
| Subtema | Network Performance Analysis |
| Mata kuliah | Probabilitas dan Statistika (INF12107) |
| Desain | Kuantitatif komparatif, pengukuran berulang, **satu sesi** |
| Lingkungan | Satu laptop Linux Mint, satu koneksi Wi-Fi, Python 3.12.3 |
| Sumber data | Pengukuran langsung dengan `dnspython` dan `ping` |
| Waktu pelaksanaan | 24 November 2026, `04:49:38`–`04:55:20` WIB, `run_id=bfcc6beb3ee9` |

Rancangan awal 3 hari × 3 sesi (pagi/siang/malam) × 3 putaran = **1.620 observasi dibatalkan**. Rancangan berlaku: satu sesi × 10 putaran × 10 domain × 3 resolver × 2 kondisi = **600 observasi**. Dokumentasi tidak boleh memulihkan rancangan lama sebagai rencana aktif.

## 2. Objek pengukuran

| Label CSV | Objek | Alamat IPv4 | Catatan |
|---|---|---|---|
| `google` | Google Public DNS | `8.8.8.8` | DNS publik |
| `cloudflare` | Cloudflare DNS | `1.1.1.1` | DNS publik |
| `isp` | DNS bawaan jaringan | `103.29.106.17` | Terdaftar pada koneksi; operator belum terverifikasi. Label `isp` dipertahankan pada kode/CSV; laporan memakai istilah **DNS bawaan jaringan** |

Sepuluh domain pengujian: `google.com`, `youtube.com`, `facebook.com`, `instagram.com`, `wikipedia.org`, `tokopedia.com`, `shopee.co.id`, `detik.com`, `kompas.com`, `github.com`.

## 3. Prosedur pengumpulan

1. `src/dns_collector.py` membuat 10 putaran. Urutan domain dan resolver diacak pada setiap putaran.
2. Untuk setiap pasangan domain–resolver, dua kondisi dicatat:
   - **`acak`**: query ke subdomain acak 16 karakter, lalu durasi dan statusnya dicatat.
   - **`ulang`**: query pemanasan ke domain asli (tidak dicatat), jeda, lalu query ulang ke domain yang sama yang dicatat.
3. `rtt_ms` diukur sekali per resolver per putaran dengan `ping` (rata-rata ICMP), lalu disalin ke seluruh baris resolver–putaran itu.
4. `waktu_ms` diukur dengan `time.perf_counter()` di sekitar pemanggilan `resolver.resolve(..., "A")`.
5. `TIMEOUT = 3.0` detik, `JEDA = 0.3` detik. `status` mencatat `ok`, `nxdomain`, `noanswer`, `timeout`, `no_nameservers`, atau `error_*`.
6. Hasil ditulis ke `data/raw/dns_data.csv` dengan mode **append**. Dataset utama sudah lengkap;Collector tidak boleh dijalankan ulang.

## 4. Variabel

| Variabel | Jenis | Definisi operasional / peran |
|---|---|---|
| `waktu_ms` | Numerik | Durasi resolusi DNS yang dicatat, dalam milidetik; termasuk overhead Python/dnspython dan retry hingga batas `lifetime`. Bukan RTT jaringan murni. |
| `rtt_ms` | Numerik | Rata-rata RTT ICMP per resolver per putaran. 30 nilai unik, masing-masing dipakai pada 20 baris. |
| `resolver` | Kategorikal | `google` / `cloudflare` / `isp` |
| `jenis_cache` | Kategorikal | `acak` / `ulang` — label prosedur, **bukan** bukti cache miss/hit |
| `status` | Kategorikal | `ok` / `nxdomain` / `noanswer` / `timeout` / `no_nameservers` / `error_*` |
| `domain`, `putaran`, `run_id`, `timestamp` | Konteks | Pengelompokan pengukuran dan audit |
| `sesi` | Konteks | Label otomatis dari jam mulai (`malam` untuk 04.49); warisan desain lama, bukan variabel analisis |

## 5. Komposisi data terverifikasi

| Dimensi | Jumlah |
|---|---:|
| Total baris | 600 |
| Putaran | 10 × 60 baris |
| Resolver | 200 per resolver |
| Kondisi | 100 per resolver per kondisi |
| Status `ok` | 300 |
| Status `nxdomain` | 270 |
| Status `noanswer` | 30 |
| Missing value | 0 |
| Duplikasi kombinasi `run_id`+`putaran`+`resolver`+`domain`+`jenis_cache` | 0 |
| Nilai `waktu_ms` / `rtt_ms` ≤ 0 | 0 |

Distribusi status menurut kondisi:

| `jenis_cache` | `ok` | `nxdomain` | `noanswer` |
|---|---:|---:|---:|
| `acak` | 0 | 270 | 30 |
| `ulang` | 300 | 0 | 0 |

Seluruh 30 baris `noanswer` berasal dari subdomain acak `github.com` (NODATA wildcard), tiga per resolver per putaran totalnya 10 per resolver. Ini respons DNS yang sah.

## 6. Cleaning

`src/clean_dns.py` memvalidasi skema, tipe data, missing value, duplikasi kunci, rentang nilai, komposisi resolver/kondisi/putaran, dan status yang diizinkan. Tidak ada baris yang dibuang dari `dataset_cleaned.csv`. Filter `ulang` + `ok` menghasilkan `dataset_analisis_utama.csv` (300 baris) dan **meniadakan seluruh kondisi `acak`**. Efek samping: `timestamp` pada salinan cleaned dinormalisasi dari format `T` menjadi spasi; file raw tidak berubah. Audit tertulis di `docs/audit_cleaning.txt`.

## 7. Batasan interpretasi yang wajib dipatuhi

1. `acak` dan `ulang` hanya menyatakan prosedur, bukan bukti cache miss/hit.
2. Karena seluruh `acak` non-OK dan seluruh `ulang` `ok`, perbandingan dua kondisi **mencampur efek prosedur dan jenis respons**. Statistik deskriptif harus dinyatakan per kondisi dan per status; jangan menyimpulkan efek cache dari perbedaan mean saja.
3. 600 baris bukan 600 sampel independen. Struktur pengulangan: putaran, domain, resolver, dan pasangan `acak`–`ulang`.
4. RTT digunakan ulang dalam satu putaran. Korelasi/regresi pada level baris adalah pseudo-replikasi; pakai agregat resolver×putaran (n=30) atau metode yang memperhitungkan dependensi, dan nyatakan n yang dipakai.
5. Distribusi `waktu_ms` berekor panjang (median ~10,6 ms, maksimum 127,4 ms pada `ulang`; maksimum 289,9 ms pada `acak`). Mean mudah dipengaruhi outlier; sertakan median, kuartil, dan identifikasi outlier.
6. Satu perangkat, satu jaringan, satu sesi. Generalisasi lintas waktu/jaringan tidak didukung.
7. Belum ada uji hipotesis. Pernyataan "Google rata-rata terendah pada dataset ini" adalah temuan deskriptif, bukan bukti keunggulan umum.

## 8. Rencana analisis lanjutan

- **P13:** histogram, boxplot, scatter plot; pola distribusi dan outlier; tiga visualisasi minimum; interpretasi tiap grafik. Scatter plot memakai unit agregat RTT.
- **P14:** pilih distribusi yang sesuai (misalnya lognormal/gamma, diuji, bukan diasumsikan), simulasi NumPy, estimasi parameter SciPy, H0/H1, uji dengan α = 0,05 yang sesuai dengan desain berulang, interpretasi statistik uji dan p-value.
- **P15:** korelasi Pearson dan regresi linear sederhana pada unit yang tepat, interpretasi arah/kekuatan, koefisien, R², pembahasan, kesimpulan, artikel, laporan PDF, presentasi, README reproduksi.

Detail dan status ada di [`tickets/README.md`](tickets/README.md).
