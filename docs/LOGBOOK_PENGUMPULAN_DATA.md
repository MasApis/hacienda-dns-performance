# Logbook Pengumpulan Data DNS — Hacienda Del Part

**Penelitian:** Analisis Perbandingan Waktu Resolusi DNS pada Resolver Google, Cloudflare, dan ISP Berdasarkan Pendekatan Probabilitas dan Statistika  
**Tahap:** Pertemuan 12 — Data Collection  
**Periode:** 24–26 November 2026 (WIB)  
**Perangkat dan OS:** laptop penelitian yang sama; Linux Mint  
**Koneksi jaringan yang disepakati:** Wi-Fi `BESI HIJAU`  
**Resolver:** Google `8.8.8.8`; Cloudflare `1.1.1.1`; DNS bawaan jaringan `103.29.106.17` (kepemilikan operasional ISP belum dikonfirmasi).

## A. Jadwal tetap (rencana)

| Hari/tanggal | Pagi 08.00 WIB | Siang 13.00 WIB | Malam 20.00 WIB | Target harian |
|---|---|---|---|---:|
| Selasa, 24 Nov 2026 | ☐ 180 | ☐ 180 | ☐ 180 | 540 |
| Rabu, 25 Nov 2026 | ☐ 180 | ☐ 180 | ☐ 180 | 540 |
| Kamis, 26 Nov 2026 | ☐ 180 | ☐ 180 | ☐ 180 | 540 |
| **Total** | **540** | **540** | **540** | **1.620** |

Satu sesi: 3 putaran × 10 domain × 3 resolver × 2 kondisi (`acak`/`ulang`) = **180 baris**. Waktu pada tabel merupakan **rencana**; waktu aktual harus dicatat setelah selesai. Selisih dari jadwal tidak boleh disembunyikan.

## B. Aturan wajib / protokol tetap

1. **Tempat:** Jalankan seluruh pengukuran dari **lokasi fisik yang sama** dan Wi-Fi `BESI HIJAU` dengan laptop yang sama. Jangan berpindah ke hotspot, VPN, jaringan kampus, atau koneksi lain. Jika terjadi perubahan tak terhindarkan, **hentikan, catat, dan tandai data terdampak** untuk ditinjau, bukan digabung seolah setara.
2. **Waktu:** Jalankan pada **08.00, 13.00, dan 20.00 WIB**, masing-masing pada 24, 25, dan 26 November 2026. Label `--sesi` harus cocok dengan jam aktual; jangan memalsukan label waktu jika terlambat. Jika terlewat, catat sebagai `TERLEWAT`, bukan mengisi hasil perkiraan.
3. **Alat dan parameter:** Gunakan `src/dns_collector.py` versi yang sama, `--isp 103.29.106.17`, `--rounds 3`, 10 domain tetap, serta `TIMEOUT=3.0` dan `JEDA=0.3`. Jangan mengubah daftar domain, konfigurasi perangkat, atau kode di tengah periode pengamatan tanpa pencatatan versi dan alasan.
4. **Kondisi perangkat:** Pastikan jam komputer sesuai WIB; matikan VPN/proxy DNS yang dapat mengubah jalur pengukuran dan hindari unduhan besar, speed test, atau aktivitas berat lain selama satu sesi. Catat gangguan yang tidak dapat dihindari.
5. **Cara eksekusi:** Jalankan **satu proses collector per sesi**, tunggu sampai selesai, catat `run_id`, jam mulai dan selesai, jumlah baris, serta status. Jangan menjalankan dua proses collector secara paralel.
6. **Data asli tidak boleh diubah:** File utama `data/raw/dns_data.csv` bersifat **append-only**. Jangan mengedit nilai, menghapus outlier, menimpa file, atau menghapus status `nxdomain`/`noanswer`/`timeout`. Cleaning dilakukan belakangan pada file lain di `data/processed/`.
7. **Gagal/terputus:** Jika script error atau koneksi terputus, jangan langsung menjalankan ulang dengan asumsi data belum tertulis. Periksa `run_id` dan jumlah baris dahulu; dokumentasikan kegagalan dan keputusan pemulihan. Data parsial harus ditandai.
8. **Audit selesai sesi:** Pastikan ada 180 baris tambahan **jika sesi lengkap**, serta periksa jumlah baris keseluruhan dan `run_id`. Jumlah yang tepat tidak menjamin semua respons sukses: hitung dan laporkan status DNS secara terpisah.
9. **Kejujuran metodologis:** Kondisi `acak` dan `ulang` **bukan** cache miss/hit terverifikasi. DNS `103.29.106.17` disebut **DNS bawaan jaringan** hingga operator resolver terbukti. RTT `ping` tidak disamakan dengan latency kueri DNS.
10. **Bukti:** Isi logbook segera setelah sesi, tanpa mengarang hasil. Simpan output ringkas terminal, bila perlu screenshot, dan catat hash/commit kode jika ada perubahan. Jangan mengunggah data identifikasi pribadi atau rahasia jaringan.

## C. Perintah per sesi

```bash
cd ~/Projects/hacienda-dns
source .venv/bin/activate

# Jalankan perintah yang sesuai dengan jam aktual:
python src/dns_collector.py --isp 103.29.106.17 --rounds 3 --sesi pagi
python src/dns_collector.py --isp 103.29.106.17 --rounds 3 --sesi siang
python src/dns_collector.py --isp 103.29.106.17 --rounds 3 --sesi malam
```

**Pilih satu perintah**, bukan menjalankan ketiganya sekaligus. Setelah selesai:

```bash
wc -l data/raw/dns_data.csv
python - <<'PY'
import pandas as pd
from pathlib import Path
p = Path('data/raw/dns_data.csv')
if not p.exists():
    print('Dataset utama belum dibuat.')
else:
    df = pd.read_csv(p)
    print('Total baris data:', len(df))
    print('Run ID dan jumlah baris:')
    print(df.groupby(['run_id','sesi']).size().to_string())
    print('Status DNS per resolver:')
    print(pd.crosstab(df['resolver'], df['status']).to_string())
PY
```

Perkiraan kumulatif **jika seluruh sesi berurutan dan lengkap**: sesi 1 = 181 baris CSV, sesi 2 = 361, sesi 3 = 541, ... sesi 9 = 1.621 (termasuk header). Bila berbeda, jangan langsung mengubah data; audit penyebabnya.

## D. Tabel logbook pelaksanaan (diisi setelah setiap sesi)

| No. | Tanggal | Sesi (rencana) | Mulai–selesai aktual (WIB) | Run ID | Baris tambahan | Status pelaksanaan | Catatan kondisi/gangguan |
|---:|---|---|---|---|---:|---|---|
| 1 | 24-11-2026 | Pagi 08.00 | — | — | — | BELUM | — |
| 2 | 24-11-2026 | Siang 13.00 | — | — | — | BELUM | — |
| 3 | 24-11-2026 | Malam 20.00 | — | — | — | BELUM | — |
| 4 | 25-11-2026 | Pagi 08.00 | — | — | — | BELUM | — |
| 5 | 25-11-2026 | Siang 13.00 | — | — | — | BELUM | — |
| 6 | 25-11-2026 | Malam 20.00 | — | — | — | BELUM | — |
| 7 | 26-11-2026 | Pagi 08.00 | — | — | — | BELUM | — |
| 8 | 26-11-2026 | Siang 13.00 | — | — | — | BELUM | — |
| 9 | 26-11-2026 | Malam 20.00 | — | — | — | BELUM | — |

Status yang boleh digunakan: `BELUM`, `SELESAI`, `PARSIAL`, `GAGAL`, `TERLEWAT`. Jangan menandai `SELESAI` sebelum cek jumlah data dan status eksekusi.

## E. Form detail tiap sesi (salin dan isi 9 kali)

```text
IDENTITAS SESI
Hari/tanggal            :
Sesi yang direncanakan  : pagi / siang / malam
Waktu rencana (WIB)     :
Waktu mulai aktual      :
Waktu selesai aktual    :
Lokasi (deskripsi umum) :
Wi-Fi                   : BESI HIJAU / berubah (jelaskan)
Laptop / OS             : laptop penelitian / Linux Mint
VPN / jaringan lain     : tidak / ya (jelaskan)

EKSEKUSI
Perintah dijalankan     :
Run ID                  :
Putaran selesai         : ... / 3
Jumlah baris sebelum    :
Jumlah baris sesudah    :
Baris tambahan          :
Status sesi             : SELESAI / PARSIAL / GAGAL / TERLEWAT

KUALITAS DAN KONDISI
Status DNS (ok/nxdomain/noanswer/timeout/error) :
RTT kosong / kegagalan ping                    :
Gangguan atau penyimpangan                     :
Tindakan yang diambil                          :
Bukti (nama screenshot atau path log)          :
Catatan pengamat                               :
```

## F. Ketentuan penyerahan setelah 3 hari

Saat sembilan sesi sudah selesai, siapkan **dataset utama asli** `data/raw/dns_data.csv` dan **logbook terisi** ini. Sertakan ringkasan jumlah `run_id`, 180 baris per sesi atau penjelasan jika berbeda, catatan gangguan, serta versi kode yang digunakan. **Jangan melakukan cleaning sebelum raw dataset diamankan dan diaudit.**
