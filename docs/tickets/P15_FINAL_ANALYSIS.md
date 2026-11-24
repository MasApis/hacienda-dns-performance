# P15 — Korelasi, Regresi, dan Finalisasi

| Field | Nilai |
|---|---|
| **Ticket ID** | P15 |
| **Judul** | Korelasi, Regresi, dan Finalisasi |
| **Pertemuan** | 15 |
| **Tujuan** | Menyelesaikan analisis hubungan, pembahasan, dan seluruh luaran akhir yang dapat direproduksi. |
| **Deskripsi pekerjaan** | Korelasi Pearson, regresi linear sederhana, interpretasi koefisien dan R², pembahasan dan kesimpulan, artikel ilmiah, laporan PDF, presentasi akhir, README reproduksi, serta pemeriksaan kelengkapan luaran. |
| **Input** | Seluruh luaran P12–P14, masukan dosen dari P14-10, panduan dosen bab E/H/I/J. |
| **Output yang diharapkan** | Notebook lengkap, artikel draft, laporan PDF, presentasi akhir, README reproduksi, struktur pengumpulan akhir. |
| **Status** | **TODO** |
| **Bukti** | belum tersedia |
| **Dependensi** | P14 |
| **Catatan kendala & keputusan** | Batas akhir sesuai panduan: **7–11 Desember 2026**. Korelasi/regresi RTT vs waktu respons wajib memakai unit agregat resolver×putaran (n=30), bukan 600 baris yang disalin RTT-nya. |

## P15-01 — Korelasi Pearson

- **Status:** TODO
- **Tujuan:** Mengukur arah dan kekuatan hubungan RTT dengan waktu respons DNS.
- **Deskripsi:** Agregasi RTT dan `waktu_ms` per resolver×putaran (n=30), hitung korelasi Pearson dan signifikansinya bila sesuai.
- **Input:** `data/processed/dataset_cleaned.csv`, `docs/METODOLOGI.md` bagian 7 butir 4.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Koefisien, arah, kekuatan, p-value (bila dihitung), n=30, dan interpretasi tercantum; tidak ada korelasi 600 baris sebagai temuan utama.
- **Dependensi:** P14-10
- **Catatan:** Korelasi awal pada level baris ≈ 0,006 dan pada level agregat ≈ 0,036 hanya sebagai pemeriksaan awal, bukan hasil final yang dihitung ulang di sini.

## P15-02 — Regresi linear sederhana

- **Status:** TODO
- **Tujuan:** Memodelkan waktu respons sebagai fungsi RTT pada unit pengamatan yang benar.
- **Deskripsi:** Bangun Y = a + bX dengan Y = rata-rata `waktu_ms` per resolver×putaran, X = `rtt_ms`; laporkan a, b, R², dan diagnostik residu.
- **Input:** P15-01.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** X, Y, a, b, R² didefinisikan; interpretasi b dalam ms per ms RTT; keterbatasan n=30 dan satu sesi dinyatakan.
- **Dependensi:** P15-01
- **Catatan:** Jangan menyimpulkan kausalitas dari regresi pada data observasional ini.

## P15-03 — Penyelesaian pembahasan

- **Status:** TODO
- **Tujuan:** Mengintegrasikan deskriptif, EDA, inferensi, dan hubungan antarvariabel.
- **Deskripsi:** Tulis pembahasan yang menjawab rumusan masalah dan menjelaskan perbedaan status respons serta dependensi data.
- **Input:** P12–P15-02.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Setiap klaim didukung angka dari notebook; tidak ada generalisasi lintas jaringan/waktu.
- **Dependensi:** P15-02
- **Catatan:** Sertakan penjelasan mengapa `acak` dan `ulang` tidak setara secara status.

## P15-04 — Kesimpulan dan saran

- **Status:** TODO
- **Tujuan:** Menutup penelitian dengan jawaban tujuan dan saran yang realistis.
- **Deskripsi:** Rumuskan kesimpulan berbasis bukti, keterbatasan, dan saran pengembangan.
- **Input:** P15-03.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Kesimpulan sesuai hasil uji (bila ada); saran tidak menjanjikan publikasi.
- **Dependensi:** P15-03
- **Catatan:** Panduan menyatakan publikasi adalah target pengembangan, bukan jaminan.

## P15-05 — Draft artikel ilmiah

- **Status:** TODO
- **Tujuan:** Menyusun draft artikel sesuai format panduan bab H.
- **Deskripsi:** Susun judul, abstrak, pendahuluan, metode, hasil dan pembahasan, kesimpulan, daftar pustaka.
- **Input:** P15-04, seluruh notebook.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** File draft tersedia (format disepakati, mis. `.docx`); referensi dapat diverifikasi; angka konsisten dengan laporan.
- **Dependensi:** P15-04
- **Catatan:** Format akhir pengumpulan: `03_ARTIKEL/draft_artikel_ilmiah.docx`.

## P15-06 — Laporan akhir PDF

- **Status:** TODO
- **Tujuan:** Menghasilkan laporan lengkap sesuai panduan.
- **Deskripsi:** Susun laporan dengan bagian yang sama dengan artikel, ditambah detail teknis dan bukti.
- **Input:** P15-05.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** File PDF tersedia; seluruh luaran P12–P15 terlaporkan; grafik dan tabel mengikuti notebook.
- **Dependensi:** P15-05
- **Catatan:** Format akhir pengumpulan: `04_LAPORAN/laporan_project.pdf`.

## P15-07 — Presentasi akhir

- **Status:** TODO
- **Tujuan:** Memenuhi batas presentasi akhir 7–11 Desember 2026.
- **Deskripsi:** Siapkan file presentasi 10 menit + 5 menit tanya jawab, demonstrasikan notebook.
- **Input:** P15-04, P15-06, revisi P14-10.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** File presentasi tersedia; setiap anggota dapat menjelaskan bagiannya; notebook berjalan saat demonstrasi.
- **Dependensi:** P15-06
- **Catatan:** Format akhir pengumpulan: `05_PRESENTASI/presentasi_akhir.pdf`.

## P15-08 — README petunjuk reproduksi

- **Status:** TODO
- **Tujuan:** Memastikan orang lain dapat menjalankan ulang seluruh analisis.
- **Deskripsi:** Lengkapi README root dan siapkan `README.txt` sesuai panduan bab I: sumber data, library, cara menjalankan notebook, urutan langkah.
- **Input:** Seluruh luaran P12–P15.
- **Output/Bukti:** `README.md` sudah ada; `README.txt` belum tersedia.
- **Acceptance criteria:** Perintah dapat dijalankan; tidak ada jalur yang mengharuskan menjalankan collector; tidak ada perubahan pada data mentah.
- **Dependensi:** P15-06
- **Catatan:** Perbaikan portabilitas `ROOT` notebook (P12-10) sebaiknya selesai sebelum butir ini.

## P15-09 — Struktur pengumpulan akhir

- **Status:** TODO
- **Tujuan:** Menyesuaikan direktori penyerahan dengan bab I panduan dosen.
- **Deskripsi:** Siapkan `PROJECT_PROBSTAT_NAMA_KELOMPOK/` berisi `01_DATASET/`, `02_NOTEBOOK/`, `03_ARTIKEL/`, `04_LAPORAN/`, `05_PRESENTASI/`, `README.txt`.
- **Input:** P15-01–P15-08.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Struktur lengkap; `dataset_original.csv` dan `dataset_cleaned.csv` hadir; tidak ada data yang diubah.
- **Dependensi:** P15-05, P15-06, P15-07, P15-08
- **Catatan:** Gunakan salinan file, jangan memindahkan dataset asli keluar dari `data/raw/`.

## P15-10 — Pemeriksaan kelengkapan dan penyerahan

- **Status:** TODO
- **Tujuan:** Memastikan tidak ada luaran yang terlewat sebelum batas 7–11 Desember 2026.
- **Deskripsi:** Cocokkan seluruh luaran dengan bab E dan J panduan, periksa konsistensi angka di notebook/laporan/artikel/presentasi.
- **Input:** P15-01–P15-09.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Semua ticket P12–P15 berstatus DONE atau BLOCKED dengan alasan; tidak ada angka yang bertentangan antarfile.
- **Dependensi:** P15-09
- **Catatan:** Rekomendasi pesan commit akhir: `docs: complete P15 research deliverables and reproducibility guide`. Commit/push tetap menunggu persetujuan.
