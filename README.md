# Mini Project — Simulasi Link Budget dan Trade-off Modulasi

> **Kelompok C**
> - Muhammad Jibril Adrian (2206059660)
> - Falah Andhesryo (2306161990)
> - Muhammad Riyan Satrio Wibowo (2306229323)
> - Ryan Adidaru Excel Barnabi (2306266994)

Simulasi sistem komunikasi nirkabel untuk drone video monitoring.

## Struktur Proyek

```
MiniProject_Wireless/
├── src/
│   ├── fspl.py          # Bagian 1: FSPL simulation
│   ├── link_budget.py   # Bagian 2: Link budget analysis
│   ├── modulation.py    # Bagian 3: BER vs Eb/N0 analysis
│   └── main.py          # Runner: generates all plots + tables
├── report/
│   └── laporan.ipynb    # Laporan lengkap (Jupyter Notebook)
├── plots/               # Output grafik (auto-generated)
└── README.md
```

## Cara Menjalankan

### Menjalankan seluruh simulasi (generate semua plot)

```bash
cd MiniProject_Wireless
python3 src/main.py
```

### Membuka laporan Jupyter

```bash
cd MiniProject_Wireless
jupyter notebook report/laporan.ipynb
```

### Google Colab

Upload folder `src/` dan `report/laporan.ipynb` ke Google Drive, lalu buka `laporan.ipynb` di Colab. Ubah path import menjadi:

```python
import sys; sys.path.insert(0, '/content/src')
```

## Dependensi

```
python >= 3.8
numpy
matplotlib
scipy
jupyter  (untuk notebook)
```

Install:

```bash
pip install numpy matplotlib scipy jupyter
```

## Output Grafik

| File | Deskripsi |
|------|-----------|
| `fspl_vs_distance.png` | FSPL vs jarak, 3 frekuensi (linear & log scale) |
| `link_budget_received_power.png` | Daya terima + noise floor semua BW |
| `link_margin_vs_distance.png` | Link margin vs jarak @ 2.4 GHz |
| `noise_floor_vs_bandwidth.png` | Noise floor per bandwidth (bar chart) |
| `link_margin_comparison.png` | Perbandingan link margin semua frekuensi @ 1 km |
| `ber_vs_ebn0.png` | BER vs Eb/N₀ untuk BPSK/QPSK/16-QAM/64-QAM |
| `ber_vs_snr.png` | BER vs SNR |
| `spectral_efficiency_tradeoff.png` | Trade-off: efficiency vs Eb/N₀ required |
| `throughput_vs_snr.png` | Throughput achievable @ 10 MHz |

## Parameter Sistem

| Parameter | Nilai |
|-----------|-------|
| Pt | 30 dBm |
| Gt / Gr | 5 dBi |
| Lmisc | 3 dB |
| NF | 5 dB |
| Frekuensi | 700 MHz, 2.4 GHz, 28 GHz |
| Bandwidth | 1 MHz, 10 MHz, 100 MHz |
| Modulasi | BPSK, QPSK, 16-QAM, 64-QAM |
