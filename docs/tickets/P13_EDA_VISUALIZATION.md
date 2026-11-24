# P13 — Exploratory Data Analysis dan Visualisasi

| Field | Nilai |
|---|---|
| **Ticket ID** | P13 |
| **Judul** | Exploratory Data Analysis dan Visualisasi |
| **Pertemuan** | 13 |
| **Tujuan** | Memahami bentuk distribusi, pola, dan outlier waktu respons DNS, lalu menyajikannya dalam minimal tiga visualisasi yang diinterpretasi. |
| **Deskripsi pekerjaan** | EDA lanjutan pada dataset hasil cleaning; identifikasi distribusi dan outlier; histogram, boxplot, scatter plot; interpretasi tiap grafik; notebook tahap kedua; draft awal bagian hasil. |
| **Input** | `data/processed/dataset_cleaned.csv`, `data/processed/statistik_query_*.csv`, `docs/METODOLOGI.md`. |
| **Output yang diharapkan** | Notebook tahap kedua, minimal 3 grafik berserta interpretasi, catatan distribusi dan outlier, draft bagian hasil. |
| **Status** | **TODO** |
| **Bukti** | belum tersedia |
| **Dependensi** | P12 (khususnya P12-06 dan P12-07) |
| **Catatan kendala & keputusan** | Sebelum membuat grafik, dapat persetujuan eksplisit. Jangan menggabungkan kondisi `acak` dan `ulang` dalam satu ringkasan tanpa keterangan status respons. Scatter plot RTT memakai unit agregat resolver×putaran (n=30), bukan 600 baris. |

## P13-01 — Verifikasi input dan definisi subset

- **Status:** TODO
- **Tujuan:** Memastikan EDA memakai dataset dan definisi yang benar.
- **Deskripsi:** Muat `dataset_cleaned.csv`, verifikasi 600 baris, dan pisahkan `acak` vs `ulang` serta status respons.
- **Input:** `data/processed/dataset_cleaned.csv`.
- **Output/Bukti:** belum tersedia (sel notebook tahap kedua).
- **Acceptance criteria:** Tercantum 300 `acak` non-OK dan 300 `ulang` `ok`; tidak ada klaim keduanya setara.
- **Dependensi:** P12-06
- **Catatan:** Gunakan `dataset_analisis_utama.csv` hanya bila yang dimaksud adalah subset `ulang`+`ok`.

## P13-02 — Pemeriksaan bentuk distribusi

- **Status:** TODO
- **Tujuan:** Mengidentifikasi pola distribusi waktu respons.
- **Deskripsi:** Hitung skewness, kurtosis, kuartil, dan ringkasan ekor per resolver per kondisi.
- **Input:** P13-01.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Ada pernyataan apakah data simetris/condong dan justifikasi kandidat distribusi untuk P14; tidak langsung menyatakan normal.
- **Dependensi:** P13-01
- **Catatan:** Ekor panjang sudah terlihat pada statistik P12 (maks 289,9 ms pada `acak`).

## P13-03 — Identifikasi outlier

- **Status:** TODO
- **Tujuan:** Menandai pengukuran ekstrem tanpa merusak data.
- **Deskripsi:** Terapkan aturan IQR atau persentil, hitung jumlah dan posisi outlier per kelompok.
- **Input:** P13-02.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Metode dan ambang batas dinyatakan; outlier **ditandai, tidak dihapus**; alasan tertulis.
- **Dependensi:** P13-02
- **Catatan:** Dataset asli dan cleaned tidak boleh diubah.

## P13-04 — Histogram

- **Status:** TODO
- **Tujuan:** Menampilkan bentuk distribusi `waktu_ms`.
- **Deskripsi:** Buat histogram per resolver, dibedakan menurut kondisi query.
- **Input:** P13-01–P13-03.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Sumbu, satuan ms, legenda, dan judul jelas; kondisi tidak dicampur tanpa penjelasan.
- **Dependensi:** P13-02
- **Catatan:** Visualisasi ke-1 dari minimal 3.

## P13-05 — Boxplot

- **Status:** TODO
- **Tujuan:** Menampilkan penyebaran dan outliers antarresolver.
- **Deskripsi:** Boxplot `waktu_ms` oleh resolver dan `jenis_cache`, dengan penanda outlier.
- **Input:** P13-03.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Median, IQR, dan outlier terbaca; selisih skala `acak`/`ulang` dijelaskan.
- **Dependensi:** P13-03
- **Catatan:** Visualisasi ke-2.

## P13-06 — Scatter plot RTT terhadap waktu DNS

- **Status:** TODO
- **Tujuan:** Mengamati pola hubungan dua variabel numerik pada unit pengamatan yang benar.
- **Deskripsi:** Plot `rtt_ms` vs rata-rata `waktu_ms` per resolver×putaran (n=30).
- **Input:** P13-01, `docs/METODOLOGI.md` bagian 7 butir 4.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Jumlah titik 30 dan tercantum di narasi; ada catatan bahwa RTT tidak independen pada level 600 baris.
- **Dependensi:** P13-01
- **Catatan:** Visualisasi ke-3. Scatter pada 600 baris hanya boleh sebagai ilustrasi berlabel "pseudo-replikasi", bukan dasar kesimpulan.

## P13-07 — Interpretasi setiap visualisasi

- **Status:** TODO
- **Tujuan:** Mengubah grafik menjadi narasi ilmiah.
- **Deskripsi:** Tulis interpretasi histogram, boxplot, dan scatter plot secara terpisah.
- **Input:** P13-04–P13-06.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Tiap grafik memiliki paragraf interpretasi; tidak ada klaim signifikansi statistik; disebut keterbatasan satu sesi.
- **Dependensi:** P13-04, P13-05, P13-06
- **Catatan:** Pemisahan status respons wajib diingatkan kembali di sini.

## P13-08 — Notebook tahap kedua

- **Status:** TODO
- **Tujuan:** Menyajikan EDA dan visualisasi secara dapat dijalankan ulang.
- **Deskripsi:** Tambahkan bagian EDA ke notebook atau buat notebook tahap kedua dengan sel berurutan dan output tersimpan.
- **Input:** P13-01–P13-07.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Notebook berjalan dari awal tanpa error; execution count berurutan; output grafik tampil.
- **Dependensi:** P13-07
- **Catatan:** Perlu keputusan: notebook terpisah atau lanjutan `analisis_probstat.ipynb`.

## P13-09 — Draft awal bagian hasil

- **Status:** TODO
- **Tujuan:** Menyiapkan teks untuk laporan/artikel.
- **Deskripsi:** Susun draft bagian "Hasil" berisi statistik deskriptif P12 dan EDA P13.
- **Input:** P13-07, tabel statistik P12.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Angka bersumber dari file; tidak ada hasil uji hipotesis yang ditulis seolah sudah dilakukan.
- **Dependensi:** P13-07
- **Catatan:** Format akhir mengikuti bab H panduan dosen.

## P13-10 — Pemeriksaan kelengkapan P13

- **Status:** TODO
- **Tujuan:** Memastikan luaran P13 memenuhi panduan.
- **Deskripsi:** Cocokkan luaran dengan bab E pertemuan 13 panduan dosen.
- **Input:** P13-01–P13-09.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Minimal 3 visualisasi, interpretasi tiap grafik, hasil identifikasi distribusi dan outlier, notebook tahap kedua, draft hasil — semuanya ada.
- **Dependensi:** P13-08, P13-09
- **Catatan:** Status ticket diubah menjadi DONE hanya setelah bukti diperiksa, bukan saat file dibuat.
