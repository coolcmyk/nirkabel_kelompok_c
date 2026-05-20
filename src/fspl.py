"""
Bagian 1 — Simulasi Free Space Path Loss (FSPL)
FSPL(dB) = 32.44 + 20*log10(f_MHz) + 20*log10(d_km)
"""

import numpy as np
import matplotlib.pyplot as plt
import os


FREQUENCIES = {
    "700 MHz": 700,
    "2.4 GHz": 2400,
    "28 GHz (mmWave)": 28000,
}

COLORS = ["#2196F3", "#FF5722", "#4CAF50"]


def fspl_db(f_mhz: float, d_km: np.ndarray) -> np.ndarray:
    """Return FSPL in dB for frequency f_mhz and distance array d_km."""
    return 32.44 + 20 * np.log10(f_mhz) + 20 * np.log10(d_km)


def print_fspl_table():
    distances_km = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    print("\n=== FSPL (dB) ===")
    header = f"{'Jarak':>10}" + "".join(f"{k:>20}" for k in FREQUENCIES)
    print(header)
    print("-" * len(header))
    for d in distances_km:
        row = f"{d:>9.1f}km"
        for f_mhz in FREQUENCIES.values():
            row += f"{fspl_db(f_mhz, d):>20.2f}"
        print(row)


def plot_fspl(save_dir: str = "../plots") -> None:
    distances = np.linspace(0.1, 10, 1000)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Linear distance
    ax = axes[0]
    for (label, f_mhz), color in zip(FREQUENCIES.items(), COLORS):
        loss = fspl_db(f_mhz, distances)
        ax.plot(distances, loss, label=label, color=color, linewidth=2)
    ax.set_xlabel("Jarak (km)", fontsize=12)
    ax.set_ylabel("FSPL (dB)", fontsize=12)
    ax.set_title("FSPL vs Jarak (Skala Linear)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.1, 10)

    # Log distance
    ax = axes[1]
    for (label, f_mhz), color in zip(FREQUENCIES.items(), COLORS):
        loss = fspl_db(f_mhz, distances)
        ax.semilogx(distances, loss, label=label, color=color, linewidth=2)
    ax.set_xlabel("Jarak (km) — Skala Log", fontsize=12)
    ax.set_ylabel("FSPL (dB)", fontsize=12)
    ax.set_title("FSPL vs Jarak (Skala Log)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which="both")
    ax.set_xlim(0.1, 10)

    # Annotate difference at 1 km
    for ax in axes:
        fspl_700 = fspl_db(700, 1.0)
        fspl_28k = fspl_db(28000, 1.0)
        ax.annotate(
            f"Δ = {fspl_28k - fspl_700:.1f} dB\n@1 km",
            xy=(1.0, (fspl_700 + fspl_28k) / 2),
            xytext=(2.5, (fspl_700 + fspl_28k) / 2 - 5),
            arrowprops=dict(arrowstyle="->", color="gray"),
            fontsize=9,
            color="gray",
        )

    fig.suptitle(
        "Free Space Path Loss (FSPL) — Perbandingan Frekuensi",
        fontsize=15,
        fontweight="bold",
    )
    plt.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    out = os.path.join(save_dir, "fspl_vs_distance.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out}")
