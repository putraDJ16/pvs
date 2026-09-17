# PV Solution — HTML + CSS statis

Hasil konversi file Figma **PV Solution** (`9cIWRPoUBfx76ALGx6c0GO`, versi 10 Sep 2026)
ke HTML + CSS statis. Tidak ada framework, tidak ada build step — buka `index.html`
langsung di browser.

## Cara pakai

Buka **`index.html`** — halaman Login, dengan dua tombol tambahan di bawah form
("Atau lihat langsung") untuk langsung masuk ke Customer UI atau PAE UI tanpa
login sungguhan. Footer di paling bawah punya link **"Lihat semua layar &
komponen"** ke `screens.html`, katalog semua 11 halaman + 4 modal untuk
navigasi cepat.

## Struktur

```
index.html              Login (+ 2 tombol quick access + footer link katalog)
screens.html             katalog semua layar (bukan bagian desain Figma — bantuan navigasi)
login.html               Login — versi murni sesuai Figma, tanpa quick access
register.html           Create an Account
register-invalid.html   Create an Account — state validasi error
customer/
  dashboard.html        Home
  application.html      Installation Application
  history.html          Application History (+ modal detail)
pae/
  dashboard.html        Dashboard (+ modal Sync Data to P4B)
  application.html      Installation Application
  history.html          Application History (+ modal detail)
  update-status.html    Update Application Status (+ modal update)
  activity.html         Activity History
assets/
  styles.css            design token + seluruh komponen
  app.js                modal, toggle password (± 60 baris, tanpa dependensi)
```

17 frame di Figma dipetakan jadi **11 halaman + 4 modal**, karena beberapa frame
adalah state dari layar yang sama (misal daftar + daftar dengan modal terbuka) dan
beberapa lainnya duplikat identik.

## Modal

Di Figma modal adalah frame terpisah. Di sini modal jadi bagian dari halaman
induknya dan **tertutup saat load** — klik pemicunya untuk membuka:

| Halaman | Pemicu |
|---|---|
| `customer/history.html` | tombol **View Detail** di tabel |
| `pae/history.html` | tombol **View Detail** di tabel |
| `pae/update-status.html` | tombol **Update** di tabel |
| `pae/dashboard.html` | tombol **Sync Data to P4B** |

Tutup dengan tombol ✕, klik area gelap, atau tekan `Esc`.

## Design token

Semua nilai di `assets/styles.css` diambil dari node tree Figma, bukan perkiraan
dari gambar. Yang utama:

| Token | Nilai | Dipakai untuk |
|---|---|---|
| `--brand` | `#1B4D8E` | sidebar, tombol primary, link |
| `--accent` | `#F59E0B` | logo mark, CTA "Apply for Installation" |
| `--page-bg` | `#F8FAFC` | latar halaman |
| `--font-head` | DM Sans | heading |
| `--font-body` | Inter | body |
| radius | 4 / 8 / 12 / 16 px | |

Skala abu-abu dan biru mengikuti palet Tailwind default (`#6A7282` = gray-500,
`#EFF6FF` = blue-50, dst.), jadi kalau nanti dibangun ulang pakai Tailwind,
nilainya sudah langsung cocok.

Badge status: `badge--submitted` `badge--verification` `badge--survey`
`badge--quotation` `badge--progress` `badge--completed` — warnanya persis
seperti di Figma.

## Catatan implementasi

- **Font** di-load dari Google Fonts lewat `<link>`. Kalau jaringanmu memblokir
  `fonts.googleapis.com`, halaman jatuh ke Segoe UI dan spacing bergeser sedikit
  (heading bisa jadi 3 baris, bukan 2). Kalau perlu offline penuh, unduh woff2
  Inter + DM Sans dan ganti `<link>` dengan `@font-face` lokal.
- **Layout pakai flex/grid**, bukan absolute positioning. Jadi lebih mudah
  diterjemahkan ke komponen Angular/React nanti, tapi konsekuensinya lebar kolom
  tabel ditentukan browser, tidak dipatok px seperti di Figma. Selisihnya beberapa
  piksel per kolom.
- **Ikon** adalah inline SVG bergaya Lucide, bukan hasil export dari Figma —
  vektor ikon di Figma tidak punya nama semantik, jadi dipilih yang paling dekat
  secara visual.
- **Layer yang di-hide di Figma tetap ditulis** dengan atribut `hidden` dan diberi
  komentar, supaya kontennya tidak hilang. Ada di: kotak "Demo Accounts" di
  `login.html`, serta state konfirmasi dan kotak statistik di modal Sync P4B.
- **Desain hanya punya breakpoint desktop 1280px.** CSS-nya tidak dibuat
  responsive karena tidak ada acuan mobile di Figma. Di layar sempit, tabel
  bisa di-scroll horizontal.
- **Tidak ada logika bisnis.** Form tidak memvalidasi dan tidak mengirim apa pun;
  `action` hanya mengarah ke halaman berikutnya supaya alurnya bisa dicoba.

## Kalau desainnya berubah

Halaman-halaman di `customer/`, `pae/`, `register*.html`, dan `screens.html`
di-generate dari `gen.py` (disertakan) supaya sidebar dan topbar tidak pernah
beda antar halaman. Kalau perlu ubah navigasi, topbar, atau data tabel: edit
`gen.py` lalu jalankan `python gen.py` — halaman-halaman itu ditulis ulang.
`index.html`, `login.html`, dan `assets/` ditulis manual, tidak tersentuh
script — kalau desain login berubah, edit keduanya secara terpisah (index.html
punya blok `.quick-access` tambahan yang tidak ada di login.html).
