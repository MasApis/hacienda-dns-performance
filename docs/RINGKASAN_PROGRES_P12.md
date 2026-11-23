# Ringkasan Progres Pertemuan 12

**Kelompok:** Hacienda Del Part  
**Penelitian:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Posisi pekerjaan per 24 November 2026:** pilot test dan audit awal selesai; pengumpulan data utama belum dimulai.

## 1. Persiapan
- Pengembangan dilakukan pada Linux Mint di `~/Projects/hacienda-dns`; Python 3.12.3 dan pip tersedia.
- Proyek telah memiliki repo Git, virtual environment `.venv`, `.gitignore`, `requirements.txt`, dan `src/dns_collector.py`.
- Library yang diverifikasi dapat diimpor: dnspython, Pandas, NumPy, Matplotlib, SciPy, Jupyter.

## 2. Identifikasi resolver
- Google DNS: `8.8.8.8`.
- Cloudflare DNS: `1.1.1.1`.
- DNS bawaan jaringan: `103.29.106.17` (muncul di `resolvectl`/`nmcli` untuk Wi-Fi `BESI HIJAU`).
- Koneksi internet publik teridentifikasi sebagai PT SOLNET INDONESIA, AS9422 (`ipinfo.io/org`), sementara data WHOIS untuk `103.29.106.17` menunjukkan SOLONE PTE LTD / SOLONE-SG. **Belum ada bukti operasional bahwa IP ketiga dikelola langsung oleh ISP koneksi**.
- Pengujian langsung `dig` untuk record A `google.com` berhasil (`NOERROR`) pada ketiganya. Waktu satu kali pengujian: Google 10 ms, Cloudflare 9 ms, DNS bawaan jaringan 8 ms; **bukan basis pemeringkatan statistik**.

## 3. Collector dan pilot test
- Pengumpul Python merekam `run_id`, timestamp, sesi, putaran, resolver, alamat IP, domain, label kondisi (`acak`/`ulang`), nama query, waktu DNS, status, RTT.
- `acak`: query subdomain acak; `ulang`: query domain kedua setelah pemanasan. Keduanya bukan kepastian status cache.
- Pilot test pada **24 Nov 2026 sekitar 00.48 WIB**: `run_id=9e5e799b056e`, sesi `malam`, 1 putaran, **60 observasi (61 baris termasuk header)**.
- Tiap resolver memiliki 20 observasi: 10 `acak`, 10 `ulang`.
- Tidak ada missing value dalam 12 kolom, tidak ada duplikasi baris identik, dan seluruh 60 observasi memiliki RTT.
- Untuk **masing-masing** resolver: 10 `ok`, 9 `nxdomain`, 1 `noanswer`.
- Seluruh `noanswer` terjadi pada subdomain acak `github.com`; tidak dianggap otomatis gagal jaringan dan belum dipastikan penyebab teknisnya.
- Hasil waktu rata-rata pilot (ms; masing-masing n=10 per sel):

| Resolver | `acak` | `ulang` |
|---|---:|---:|
| Cloudflare | 36.131 | 19.745 |
| Google | 33.120 | 26.218 |
| DNS bawaan jaringan | 41.272 | 15.713 |

Data tersebut bersifat indikatif dari sampel kecil, **tidak membuktikan resolver paling cepat**.

## 4. Pengarsipan dan tindak lanjut
- Dataset percobaan dipindahkan ke `data/pilot/dns_pilot.csv` (61 baris) tanpa dihapus.
- `data/raw/` telah dikonfirmasi kosong setelah pemindahan; siap untuk dataset utama.
- Data utama direncanakan **24–26 November 2026** pada 08.00, 13.00, dan 20.00 WIB, masing-masing 3 putaran. Target total 1.620 observasi.
- Setelah semua sesi: audit data mentah, cleaning terpisah, lalu statistik deskriptif (mean, median, modus jika relevan, min–max, varians, standar deviasi, kuartil).

## 5. Keputusan metodologis yang harus dipertahankan
1. Gunakan label `acak` dan `ulang`, jangan menyebutnya cache hit/miss pasti.
2. `103.29.106.17` disebut **DNS bawaan jaringan** sampai status sebagai DNS ISP dibuktikan.
3. Jangan menghapus `NXDOMAIN` dan `NoAnswer` otomatis; kategorikan status dengan benar.
4. Jangan mengubah dataset mentah dan jangan menggabungkan data pilot ke dataset utama.
5. Catat kondisi jaringan, waktu aktual, kendala, dan run ID di logbook.
