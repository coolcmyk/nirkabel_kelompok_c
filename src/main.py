"""
Main script — menjalankan seluruh simulasi dan menghasilkan semua plot.
Jalankan dari direktori src/:  python main.py
atau dari root:                python src/main.py
"""

import sys
import os

# Allow imports from src/ regardless of working directory
sys.path.insert(0, os.path.dirname(__file__))

PLOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "plots")


def run_part1():
    print("\n" + "=" * 60)
    print("BAGIAN 1 — Free Space Path Loss (FSPL)")
    print("=" * 60)
    from fspl import print_fspl_table, plot_fspl
    print_fspl_table()
    plot_fspl(save_dir=PLOTS_DIR)


def run_part2():
    print("\n" + "=" * 60)
    print("BAGIAN 2 — Link Budget")
    print("=" * 60)
    from link_budget import print_link_budget_table, plot_link_budget

    for f_mhz, label in [(700, "700 MHz"), (2400, "2.4 GHz"), (28000, "28 GHz")]:
        for d in [1.0, 5.0]:
            print_link_budget_table(f_mhz=f_mhz, d_km=d)

    plot_link_budget(save_dir=PLOTS_DIR)


def run_part3():
    print("\n" + "=" * 60)
    print("BAGIAN 3 — Analisis Modulasi & BER vs Eb/N₀")
    print("=" * 60)
    from modulation import print_modulation_summary, plot_ber, plot_snr_vs_throughput
    print_modulation_summary()
    plot_ber(save_dir=PLOTS_DIR)
    plot_snr_vs_throughput(save_dir=PLOTS_DIR, bandwidth_hz=10e6)


def run_part4():
    print("\n" + "=" * 60)
    print("BAGIAN 4 — Engineering Decision Summary")
    print("=" * 60)

    scenarios = {
        "Skenario A — Pedesaan": {
            "karakteristik": ["Coverage luas", "Infrastruktur terbatas", "User sedikit"],
            "rekomendasi": {
                "Frekuensi": "700 MHz",
                "Modulasi":  "BPSK / QPSK",
                "Bandwidth": "1 MHz",
            },
            "alasan": (
                "700 MHz memiliki FSPL lebih kecil sehingga jangkauan lebih luas. "
                "BPSK/QPSK lebih robust di SNR rendah. "
                "Bandwidth sempit menekan noise floor sehingga link margin terjaga."
            ),
        },
        "Skenario B — Perkotaan": {
            "karakteristik": ["User padat", "Throughput tinggi", "Interferensi tinggi"],
            "rekomendasi": {
                "Frekuensi": "2.4 GHz",
                "Modulasi":  "16-QAM / 64-QAM",
                "Bandwidth": "10–100 MHz",
            },
            "alasan": (
                "2.4 GHz menyeimbangkan coverage dan kapasitas. "
                "16/64-QAM memaksimalkan spectral efficiency untuk throughput tinggi. "
                "Bandwidth lebar membutuhkan SNR tinggi yang tersedia di sel kecil perkotaan."
            ),
        },
        "Skenario C — Drone Pegunungan": {
            "karakteristik": ["Fading berat", "Reliabilitas tinggi", "SNR fluktuatif"],
            "rekomendasi": {
                "Frekuensi": "700 MHz",
                "Modulasi":  "BPSK",
                "Bandwidth": "1 MHz",
            },
            "alasan": (
                "700 MHz lebih penetratif terhadap obstacle. "
                "BPSK adalah modulasi paling robust — butuh Eb/N0 ~6.8 dB untuk BER 10⁻³. "
                "Bandwidth sempit memaksimalkan link margin saat SNR fluktuatif."
            ),
        },
    }

    for scenario, data in scenarios.items():
        print(f"\n  {scenario}")
        print(f"  Karakteristik: {', '.join(data['karakteristik'])}")
        print("  Rekomendasi:")
        for k, v in data["rekomendasi"].items():
            print(f"    {k:12s}: {v}")
        print(f"  Justifikasi: {data['alasan']}")


if __name__ == "__main__":
    os.makedirs(PLOTS_DIR, exist_ok=True)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Simulasi Link Budget — Sistem Komunikasi Nirkabel       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    run_part1()
    run_part2()
    run_part3()
    run_part4()

    print(f"\n[SELESAI] Semua plot tersimpan di: {os.path.abspath(PLOTS_DIR)}")
