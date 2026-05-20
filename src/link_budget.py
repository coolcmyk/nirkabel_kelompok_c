"""
Bagian 2 — Simulasi Link Budget
Pr = Pt + Gt + Gr - Lpath - Lmisc  (dBm / dB)
N  = -174 + 10*log10(B_Hz) + NF    (dBm)
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from fspl import fspl_db, FREQUENCIES, COLORS


# ── System parameters ────────────────────────────────────────────────────────
PT_DBM   = 30   # Transmit power (dBm)
GT_DBI   = 5    # Tx antenna gain (dBi)
GR_DBI   = 5    # Rx antenna gain (dBi)
LMISC_DB = 3    # Miscellaneous losses (dB)
NF_DB    = 5    # Noise figure (dB)

BANDWIDTHS = {
    "1 MHz":   1e6,
    "10 MHz":  10e6,
    "100 MHz": 100e6,
}

BW_COLORS = ["#9C27B0", "#FF9800", "#009688"]

# Minimum SNR requirements per modulation for BER ≈ 1e-3
SNR_MIN = {
    "BPSK":   6.8,
    "QPSK":   9.8,
    "16-QAM": 16.5,
    "64-QAM": 22.3,
}


def noise_floor_dbm(bw_hz: float, nf_db: float = NF_DB) -> float:
    """Thermal noise floor in dBm."""
    return -174 + 10 * np.log10(bw_hz) + nf_db


def received_power_dbm(f_mhz: float, d_km: np.ndarray) -> np.ndarray:
    lpath = fspl_db(f_mhz, d_km)
    return PT_DBM + GT_DBI + GR_DBI - lpath - LMISC_DB


def receiver_sensitivity_dbm(bw_hz: float, snr_min_db: float = SNR_MIN["BPSK"]) -> float:
    return noise_floor_dbm(bw_hz) + snr_min_db


def link_margin_db(pr_dbm: np.ndarray, rx_sens_dbm: float) -> np.ndarray:
    return pr_dbm - rx_sens_dbm


def print_link_budget_table(f_mhz: float = 2400, d_km: float = 1.0) -> None:
    pr = received_power_dbm(f_mhz, np.array([d_km]))[0]
    print(f"\n=== Link Budget @ {f_mhz} MHz, d = {d_km} km ===")
    print(f"  Pt                : {PT_DBM:>8.2f} dBm")
    print(f"  Gt                : {GT_DBI:>8.2f} dBi")
    print(f"  Gr                : {GR_DBI:>8.2f} dBi")
    print(f"  FSPL              : {fspl_db(f_mhz, d_km):>8.2f} dB")
    print(f"  Lmisc             : {LMISC_DB:>8.2f} dB")
    print(f"  Pr (received)     : {pr:>8.2f} dBm")
    print()
    print(f"  {'Bandwidth':>10}  {'N floor':>10}  {'Rx Sens (BPSK)':>16}  {'Link Margin':>12}")
    print("  " + "-" * 55)
    for bw_label, bw_hz in BANDWIDTHS.items():
        nf = noise_floor_dbm(bw_hz)
        rs = receiver_sensitivity_dbm(bw_hz)
        lm = link_margin_db(np.array([pr]), rs)[0]
        print(f"  {bw_label:>10}  {nf:>9.2f}dBm  {rs:>15.2f}dBm  {lm:>11.2f} dB")


def plot_link_budget(save_dir: str = "../plots") -> None:
    distances = np.linspace(0.1, 10, 1000)
    os.makedirs(save_dir, exist_ok=True)

    # ── Plot 1: Received power for each frequency + noise floors ─────────────
    fig, ax = plt.subplots(figsize=(11, 7))
    for (label, f_mhz), color in zip(FREQUENCIES.items(), COLORS):
        pr = received_power_dbm(f_mhz, distances)
        ax.plot(distances, pr, label=f"Pr — {label}", color=color, linewidth=2)

    for (bw_label, bw_hz), ls in zip(BANDWIDTHS.items(), ["--", "-.", ":"]):
        nf = noise_floor_dbm(bw_hz)
        ax.axhline(
            nf,
            linestyle=ls,
            color="gray",
            linewidth=1.5,
            label=f"N floor {bw_label} ({nf:.0f} dBm)",
        )

    ax.set_xlabel("Jarak (km)", fontsize=12)
    ax.set_ylabel("Daya (dBm)", fontsize=12)
    ax.set_title(
        "Received Power vs Jarak & Noise Floor per Bandwidth",
        fontsize=13,
        fontweight="bold",
    )
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.1, 10)
    out1 = os.path.join(save_dir, "link_budget_received_power.png")
    plt.tight_layout()
    plt.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out1}")

    # ── Plot 2: Link Margin for 2.4 GHz across bandwidths ────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    pr_2400 = received_power_dbm(2400, distances)

    for (bw_label, bw_hz), color, ls in zip(BANDWIDTHS.items(), BW_COLORS, ["-", "--", "-."]):
        rs = receiver_sensitivity_dbm(bw_hz)
        lm = link_margin_db(pr_2400, rs)
        ax.plot(distances, lm, label=f"BW = {bw_label}", color=color, linewidth=2, linestyle=ls)

    ax.axhline(0, color="red", linewidth=1.5, linestyle=":", label="Link Margin = 0 dB")
    ax.fill_between(distances, 0, -80, alpha=0.08, color="red", label="Link Gagal")
    ax.set_xlabel("Jarak (km)", fontsize=12)
    ax.set_ylabel("Link Margin (dB)", fontsize=12)
    ax.set_title(
        "Link Margin vs Jarak @ 2.4 GHz — Variasi Bandwidth",
        fontsize=13,
        fontweight="bold",
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.1, 10)
    out2 = os.path.join(save_dir, "link_margin_vs_distance.png")
    plt.tight_layout()
    plt.savefig(out2, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out2}")

    # ── Plot 3: Noise floor vs bandwidth (bar chart) ──────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    bw_labels = list(BANDWIDTHS.keys())
    nf_values = [noise_floor_dbm(bw) for bw in BANDWIDTHS.values()]
    bars = ax.bar(bw_labels, nf_values, color=BW_COLORS, width=0.5, edgecolor="black", linewidth=0.8)
    for bar, val in zip(bars, nf_values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.0f} dBm",
                ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_xlabel("Bandwidth", fontsize=12)
    ax.set_ylabel("Noise Floor (dBm)", fontsize=12)
    ax.set_title("Noise Floor vs Bandwidth (NF = 5 dB)", fontsize=13, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(min(nf_values) - 5, max(nf_values) + 5)
    out3 = os.path.join(save_dir, "noise_floor_vs_bandwidth.png")
    plt.tight_layout()
    plt.savefig(out3, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out3}")

    # ── Plot 4: Link Margin comparison all freqs + all BWs at d=1km ──────────
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(FREQUENCIES))
    width = 0.25
    for i, (bw_label, bw_hz) in enumerate(BANDWIDTHS.items()):
        rs = receiver_sensitivity_dbm(bw_hz)
        lm_vals = []
        for f_mhz in FREQUENCIES.values():
            pr = received_power_dbm(f_mhz, np.array([1.0]))[0]
            lm_vals.append(link_margin_db(np.array([pr]), rs)[0])
        bars = ax.bar(x + i * width, lm_vals, width, label=f"BW = {bw_label}",
                      color=BW_COLORS[i], edgecolor="black", linewidth=0.8)
        for bar, val in zip(bars, lm_vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"{val:.0f}", ha="center", va="bottom", fontsize=9)

    ax.axhline(0, color="red", linewidth=1.5, linestyle="--", label="Batas Link Margin = 0 dB")
    ax.set_xlabel("Frekuensi", fontsize=12)
    ax.set_ylabel("Link Margin (dB)", fontsize=12)
    ax.set_title("Perbandingan Link Margin @ d = 1 km\n(BPSK, Pt = 30 dBm)", fontsize=13, fontweight="bold")
    ax.set_xticks(x + width)
    ax.set_xticklabels(list(FREQUENCIES.keys()), fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis="y")
    out4 = os.path.join(save_dir, "link_margin_comparison.png")
    plt.tight_layout()
    plt.savefig(out4, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out4}")
