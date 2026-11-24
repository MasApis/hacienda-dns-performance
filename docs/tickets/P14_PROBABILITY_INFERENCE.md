# P14 — Simulasi Probabilitas dan Inferensi Statistik

| Field | Nilai |
|---|---|
| **Ticket ID** | P14 |
| **Judul** | Simulasi Probabilitas dan Inferensi Statistik |
| **Pertemuan** | 14 |
| **Tujuan** | Memilih distribusi yang sesuai, melakukan simulasi dan estimasi, serta menguji perbedaan antarresolver dengan taraf signifikansi 0,05. |
| **Deskripsi pekerjaan** | Identifikasi distribusi, simulasi NumPy, pemakaian SciPy, estimasi parameter, perumusan H0/H1, pengujian hipotesis yang sesuai desain berulang, interpretasi statistik uji dan p-value, notebook tahap ketiga, draft laporan, dan presentasi kemajuan. |
| **Input** | `data/processed/dataset_cleaned.csv`, hasil EDA P13, `docs/METODOLOGI.md`. |
| **Output yang diharapkan** | Notebook tahap ketiga, hasil simulasi & estimasi, hasil uji hipotesis, draft awal laporan/artikel, file presentasi kemajuan, catatan masukan dosen. |
| **Status** | **TODO** |
| **Bukti** | belum tersedia |
| **Dependensi** | P13 |
| **Catatan kendala & keputusan** | Batas presentasi kemajuan sesuai panduan: **30 November–4 Desember 2026**. Uji harus memperhitungkan pengukuran berulang dan perbedaan status respons `acak`/`ulang`. Jangan memakai uji independen sederhana pada 600 baris tanpa justifikasi. |

## P14-01 — Identifikasi distribusi yang sesuai

- **Status:** TODO
- **Tujuan:** Memilih keluarga distribusi yang masuk akal bagi `waktu_ms`.
- **Deskripsi:** Bandingkan kandidat (mis. lognormal, gamma, eksponensial, normal) dengan bentuk distribusi dari P13.
- **Input:** P13-02, P13-04, P13-05.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Ada justifikasi berdasarkan bentuk data dan sifat waktu respons, bukan sekadar pilihan default; normal tidak dipakai tanpa pemeriksaan.
- **Dependensi:** P13-02
- **Catatan:** Pisahkan kondisi `acak` dan `ulang`.

## P14-02 — Peluang empiris di bawah ambang

- **Status:** TODO
- **Tujuan:** Menjawab rumusan masalah tentang peluang respons memenuhi ambang waktu.
- **Deskripsi:** Tentukan ambang secara transparan, lalu hitung peluang empiris per resolver dan kondisi.
- **Input:** P14-01, dataset cleaned.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Nilai ambang dan alasannya tertulis; peluang dihitung dari data nyata; tidak disamakan dengan probabilitas model tanpa verifikasi.
- **Dependensi:** P14-01
- **Catatan:** Ambang harus ditetapkan sebelum melihat hasil uji agar tidak terlihat dipilih setelah fakta.

## P14-03 — Simulasi probabilitas dengan NumPy

- **Status:** TODO
- **Tujuan:** Mendemonstrasikan perilaku distribusi terpilih.
- **Deskripsi:** Simulasikan data dengan parameter hasil estimasi, tetapkan seed, bandingkan ringkasan simulasi dengan data empiris.
- **Input:** P14-01, P14-02.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Seed tercatat; hasil simulasi dibandingkan secara kuantitatif; dinyatakan sebagai demonstrasi, bukan pengganti data empiris.
- **Dependensi:** P14-01
- **Catatan:** Panduan bab D butir 8: data simulasi tidak menggantikan dataset empiris sebagai dasar temuan utama.

## P14-04 — Estimasi parameter dengan SciPy

- **Status:** TODO
- **Tujuan:** Mengestimasi parameter distribusi terpilih dari data.
- **Deskripsi:** Gunakan `scipy.stats` untuk fitting dan sajikan estimated parameter beserta interval bila memungkinkan.
- **Input:** P14-01.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Nama distribusi, metode fitting, parameter, dan ukuran kesesuaian tercantum; unit ms konsisten.
- **Dependensi:** P14-01
- **Catatan:** Estimasi per resolver per kondisi, bukan menggabungkan status respons yang berbeda.

## P14-05 — Perumusan H0 dan H1

- **Status:** TODO
- **Tujuan:** Menyatakan hipotesis yang dapat diuji dengan desain ini.
- **Deskripsi:** Rumuskan hipotesis perbandingan resolver untuk kondisi `ulang`+`ok` dan, terpisah, untuk kondisi `acak` sesuai statusnya.
- **Input:** P14-04, `docs/METODOLOGI.md` bagian 7.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** H0/H1 eksplisit, arah uji (dua sisi/satu sisi) dinyatakan, unit analisis disebut.
- **Dependensi:** P14-04
- **Catatan:** Hindari pernyataan "resolver tercepat secara umum" — satu sesi dan satu jaringan.

## P14-06 — Pemilihan metode uji dan pemeriksaan asumsi

- **Status:** TODO
- **Tujuan:** Memilih uji yang sesuai dengan data berulang dan ekor panjang.
- **Deskripsi:** Evaluasi normalitas/homoskedastisitas dan pertimbangkan pendekatan berpasangan per domain–putaran atau uji nonparametrik.
- **Input:** P14-05, P13-02.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Metode dipilih berdasarkan tujuan, jenis data, desain pengamatan, dan asumsi; alternatif yang ditolak disebut alasannya.
- **Dependensi:** P14-05
- **Catatan:** Friedman atau ANOVA pengukuran berulang pada agregat putaran adalah kandidat; keputusan final diambil setelah asumsi diperiksa.

## P14-07 — Statistik uji, p-value, dan interpretasi

- **Status:** TODO
- **Tujuan:** Mengambil keputusan statistik pada α = 0,05.
- **Deskripsi:** Hitung statistik uji dan p-value, nyatakan keputusan tolak/gagal tolak H0, artikan dalam konteks DNS.
- **Input:** P14-06.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Statistik uji, p-value, α, keputusan, dan interpretasi lengkap; tidak ada klaim signifikansi tanpa p-value.
- **Dependensi:** P14-06
- **Catatan:** Jika p ≥ 0,05, tulis "gagal menolak H0", bukan "membuktikan tidak ada perbedaan".

## P14-08 — Notebook tahap ketiga

- **Status:** TODO
- **Tujuan:** Menggabungkan simulasi, estimasi, dan uji dalam notebook yang dapat dijalankan ulang.
- **Deskripsi:** Tambahkan bagian P14 ke notebook analisis dengan sel berurutan dan output tersimpan.
- **Input:** P14-02–P14-07.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Notebook berjalan dari awal; angka di laporan sama dengan output notebook; seed tercatat.
- **Dependensi:** P14-07
- **Catatan:** Perlu sinkronisasi dengan keputusan P13-08 tentang satu atau beberapa notebook.

## P14-09 — Presentasi kemajuan

- **Status:** TODO
- **Tujuan:** Menyampaikan progres sesuai batas panduan 30 November–4 Desember 2026.
- **Deskripsi:** Siapkan file presentasi berisi judul, latar belakang, rumusan masalah, dataset, variabel, metode, statistik deskriptif, EDA, hasil simulasi/estimasi/uji sementara, kendala, dan rencana.
- **Input:** P12–P14.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** File presentasi tersedia; alokasi 7–10 menit + 5 menit tanya jawab; notebook dapat didemonstrasikan.
- **Dependensi:** P14-08
- **Catatan:** Sesuai bab E dan J panduan dosen.

## P14-10 — Catatan evaluasi dan revisi dosen

- **Status:** TODO
- **Tujuan:** Menampung masukan dosen untuk diperbaiki di P15.
- **Deskripsi:** Rekam pertanyaan, koreksi, dan tindak lanjut dari presentasi kemajuan.
- **Input:** P14-09.
- **Output/Bukti:** belum tersedia.
- **Acceptance criteria:** Ada daftar masukan bertanggal dan penetapan tindak lanjut pada ticket P15.
- **Dependensi:** P14-09
- **Catatan:** Panduan mewajibkan revisi hasil presentasi kemajuan diintegrasikan ke luaran akhir.
