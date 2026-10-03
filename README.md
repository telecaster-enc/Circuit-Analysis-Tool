# Circuit Analysis Tool

Python CLI untuk menyelesaikan rangkaian resistor DC menggunakan **nodal analysis** (KVL/KCL solver), menghasilkan tegangan tiap node/resistor dan arus tiap cabang.

## Latar Belakang

Proyek ini adalah bagian dari rangkaian proyek belajar mandiri selama semester 1 perkuliahan, terinspirasi dari mata kuliah **Rangkaian Listrik I** dan **Matematika Terapan**. Tujuannya bukan cuma membuat tool yang jalan, tapi memahami materi rangkaian listrik lewat implementasi, tiap kali bingung soal teori, debug kodenya jadi cara paling efektif untuk memperkuat pemahaman.

## Metode

Rangkaian direpresentasikan sebagai graf (node = titik sambungan, edge = komponen). Penyelesaiannya menggunakan **nodal analysis / modified nodal analysis**: KCL di tiap node diterjemahkan jadi bentuk konduktansi dari hukum Ohm,

```
G · V = I
```

di mana `G` adalah matriks konduktansi, `V` vektor tegangan node yang dicari, dan `I` vektor arus/sumber yang diketahui. Sistem persamaan ini diselesaikan dengan `numpy.linalg.solve()`.

## Fitur / Command

| Command | Keterangan |
|---|---|
| `<nama> <node_a> <node_b> <nilai>` | Tambah/ubah komponen, contoh: `R1 1 2 100` |
| `seek` | Tampilkan semua komponen yang sudah dimasukkan |
| `seeker on` / `seeker off` | Aktif/nonaktifkan tampilan komponen otomatis setelah tiap input |
| `solve` | Selesaikan rangkaian, tampilkan tegangan node, tegangan resistor, dan arus cabang |
| `visualize` | Tampilkan grafik batang tegangan vs node (matplotlib) |
| `clear` | Hapus semua komponen |
| `-h` / `help` | Tampilkan bantuan |

Format nama komponen: `R` untuk resistor, `V` untuk sumber tegangan. Node `0` selalu dianggap ground (0V).

## Instalasi

```bash
pip install numpy matplotlib
```

## Cara Pakai

```bash
python main.py
```

## Contoh Pemakaian

```
> V1 1 0 9
> R1 1 2 100
> R2 2 0 220
> R3 2 0 330
> solve

=== Tegangan Node ===
Node 0: 0.000 V
Node 1: 9.000 V
Node 2: 5.121 V

=== Tegangan Resistor ===
R1: 3.879 V
R2: 5.121 V
R3: 5.121 V

=== Arus Cabang ===
R1: 38.79 mA
R2: 23.28 mA
R3: 15.52 mA
```

## Keterbatasan

Proyek ini masih jauh dari kata sempurna. Sejauh ini hanya bisa menyelesaikan rangkaian dengan sumber tegangan dalam posisi dan konfigurasi yang spesifik (salah satu terminal sumber harus terhubung ke ground, node B sumber harus terletak di 0), belum ada dukungan **supernode** untuk sumber tegangan mengambang (floating voltage source).

## Rencana Pengembangan

- Dukungan supernode untuk sumber tegangan mengambang
- Dukungan sumber arus
- Validasi rangkaian (deteksi node terisolasi, rangkaian terbuka)

Proyek ini akan terus dikembangkan. Stay tuned!