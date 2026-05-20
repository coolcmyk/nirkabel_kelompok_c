"""
Bagian 3 — Analisis BER vs Eb/N0 dan Trade-off Modulasi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
import os


MODULATIONS = {
    "BPSK":   {"M": 2,  "color": "#1565C0", "ls": "-"},
    "QPSK":   {"M": 4,  "color": "#2E7D32", "ls": "--"},
    "16-QAM": {"M": 16, "color": "#E65100", "ls": "-."},
    "64-QAM": {"M": 64, "color": "#6A1B9A", "ls": ":"},
}


def qfunc(x: np.ndarray) -> np.ndarray:
    """Q-function via erfc."""
    return 0.5 * erfc(x / np.sqrt(2))


def ber_psk(M: int, ebn0_lin: np.ndarray) -> np.ndarray:
    """BER for M-PSK (exact for BPSK/QPSK, approximate for higher orders)."""
    if M == 2:
        # BPSK: BER = Q(sqrt(2*Eb/N0))
        return qfunc(np.sqrt(2 * ebn0_lin))
    elif M == 4:
        # QPSK: same bit-error probability as BPSK
        return qfunc(np.sqrt(2 * ebn0_lin))
    else:
        # M-PSK approximation (not used here, kept for completeness)
        k = np.log2(M)
        return (2 / k) * qfunc(np.sqrt(2 * k * ebn0_lin) * np.sin(np.pi / M))


def ber_mqam(M: int, ebn0_lin: np.ndarray) -> np.ndarray:
    """
    Approximate BER for square M-QAM with Gray coding.
    Formula: BER ≈ (4/log2(M))*(1-1/sqrt(M)) * Q(sqrt(3*log2(M)*Eb/N0/(M-1)))
    """
    k = np.log2(M)
    coeff = (4 / k) * (1 - 1 / np.sqrt(M))
    arg = np.sqrt(3 * k * ebn0_lin / (M - 1))
    return coeff * qfunc(arg)


def ber(mod_name: str, ebn0_lin: np.ndarray) -> np.ndarray:
    M = MODULATIONS[mod_name]["M"]
    if mod_name in ("BPSK", "QPSK"):
        return ber_psk(M, ebn0_lin)
    return ber_mqam(M, ebn0_lin)


def spectral_efficiency(mod_name: str) -> float:
    return np.log2(MODULATIONS[mod_name]["M"])


def ebn0_for_ber_target(mod_name: str, target_ber: float = 1e-3) -> float:
    """Binary-search Eb/N0 (dB) to achieve target_ber."""
    ebn0_db_vals = np.linspace(-5, 35, 10000)
    ebn0_lin = 10 ** (ebn0_db_vals / 10)
    ber_vals = ber(mod_name, ebn0_lin)
    idx = np.argmin(np.abs(ber_vals - target_ber))
    return ebn0_db_vals[idx]


def print_modulation_summary() -> None:
    print("\n=== Trade-off Modulasi ===")
    print(f"{'Modulasi':>10}  {'η (bps/Hz)':>12}  {'Eb/N0 @BER=1e-3':>18}  {'SNR_min @BER=1e-3':>20}")
    print("-" * 66)
    for name in MODULATIONS:
        eta = spectral_efficiency(name)
        ebn0 = ebn0_for_ber_target(name, 1e-3)
        snr_min = ebn0 + 10 * np.log10(eta)
        print(f"{name:>10}  {eta:>12.1f}  {ebn0:>17.2f} dB  {snr_min:>19.2f} dB")


def plot_ber(save_dir: str = "../plots") -> None:
    os.makedirs(save_dir, exist_ok=True)
    ebn0_db = np.linspace(0, 30, 1000)
    ebn0_lin = 10 ** (ebn0_db / 10)

    # ── Plot 1: BER vs Eb/N0 ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 7))
    for name, props in MODULATIONS.items():
        ber_vals = ber(name, ebn0_lin)
        ax.semilogy(ebn0_db, ber_vals, label=name, color=props["color"],
                    linestyle=props["ls"], linewidth=2.5)

    ax.axhline(1e-3, color="gray", linewidth=1, linestyle="--", alpha=0.7, label="BER = 10⁻³")
    ax.axhline(1e-6, color="gray", linewidth=1, linestyle=":",  alpha=0.7, label="BER = 10⁻⁶")
    ax.set_xlabel("Eb/N₀ (dB)", fontsize=13)
    ax.set_ylabel("BER (Bit Error Rate)", fontsize=13)
    ax.set_title("BER vs Eb/N₀ — Perbandingan Modulasi Digital", fontsize=14, fontweight="bold")
    ax.legend(fontsize=12)
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlim(0, 30)
    ax.set_ylim(1e-8, 1)

    # Annotate Eb/N0 at BER=1e-3 for each modulation
    for name, props in MODULATIONS.items():
        req = ebn0_for_ber_target(name, 1e-3)
        ax.axvline(req, color=props["color"], linewidth=0.8, linestyle=":", alpha=0.5)
        ax.annotate(f"{req:.1f} dB", xy=(req, 1e-3),
                    xytext=(req + 0.3, 2e-3),
                    fontsize=8, color=props["color"])

    out1 = os.path.join(save_dir, "ber_vs_ebn0.png")
    plt.tight_layout()
    plt.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out1}")

    # ── Plot 2: Spectral efficiency vs Eb/N0 required ────────────────────────
    fig, ax = plt.subplots(figsize=(8, 6))
    for name, props in MODULATIONS.items():
        eta = spectral_efficiency(name)
        req = ebn0_for_ber_target(name, 1e-3)
        ax.scatter(req, eta, color=props["color"], s=200, zorder=5)
        ax.annotate(name, xy=(req, eta),
                    xytext=(req + 0.4, eta + 0.05),
                    fontsize=12, color=props["color"], fontweight="bold")

    ax.plot(
        [ebn0_for_ber_target(n, 1e-3) for n in MODULATIONS],
        [spectral_efficiency(n) for n in MODULATIONS],
        color="black", linewidth=1.5, linestyle="--", alpha=0.4,
    )
    ax.set_xlabel("Eb/N₀ Minimum @ BER = 10⁻³ (dB)", fontsize=12)
    ax.set_ylabel("Spectral Efficiency η (bps/Hz)", fontsize=12)
    ax.set_title(
        "Trade-off: Spectral Efficiency vs Eb/N₀ Required",
        fontsize=13, fontweight="bold",
    )
    ax.grid(True, alpha=0.3)
    ax.set_xlim(4, 22)
    ax.set_ylim(0, 7.5)
    out2 = os.path.join(save_dir, "spectral_efficiency_tradeoff.png")
    plt.tight_layout()
    plt.savefig(out2, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out2}")

    # ── Plot 3: BER vs SNR (not Eb/N0) ───────────────────────────────────────
    snr_db = np.linspace(0, 30, 1000)
    fig, ax = plt.subplots(figsize=(10, 7))
    for name, props in MODULATIONS.items():
        eta = spectral_efficiency(name)
        # SNR = Eb/N0 * eta  →  Eb/N0 = SNR / eta
        ebn0_lin_from_snr = (10 ** (snr_db / 10)) / eta
        ber_vals = ber(name, ebn0_lin_from_snr)
        ax.semilogy(snr_db, ber_vals, label=name, color=props["color"],
                    linestyle=props["ls"], linewidth=2.5)

    ax.axhline(1e-3, color="gray", linewidth=1, linestyle="--", alpha=0.7, label="BER = 10⁻³")
    ax.set_xlabel("SNR (dB)", fontsize=13)
    ax.set_ylabel("BER (Bit Error Rate)", fontsize=13)
    ax.set_title("BER vs SNR — Perbandingan Modulasi Digital", fontsize=14, fontweight="bold")
    ax.legend(fontsize=12)
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlim(0, 30)
    ax.set_ylim(1e-8, 1)
    out3 = os.path.join(save_dir, "ber_vs_snr.png")
    plt.tight_layout()
    plt.savefig(out3, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out3}")


def plot_snr_vs_throughput(save_dir: str = "../plots", bandwidth_hz: float = 10e6) -> None:
    """Show throughput (bps) achievable per modulation as function of SNR."""
    os.makedirs(save_dir, exist_ok=True)
    snr_db = np.linspace(0, 35, 500)

    fig, ax = plt.subplots(figsize=(10, 6))
    for name, props in MODULATIONS.items():
        eta = spectral_efficiency(name)
        ebn0_lin = (10 ** (snr_db / 10)) / eta
        ber_vals = ber(name, ebn0_lin)
        # Throughput available only when BER < 1e-2
        throughput = np.where(ber_vals < 1e-2, eta * bandwidth_hz / 1e6, np.nan)
        ax.plot(snr_db, throughput, label=name, color=props["color"],
                linestyle=props["ls"], linewidth=2.5)

    ax.set_xlabel("SNR (dB)", fontsize=12)
    ax.set_ylabel("Throughput (Mbps)", fontsize=12)
    ax.set_title(
        f"Throughput vs SNR @ BW = {bandwidth_hz/1e6:.0f} MHz (BER < 10⁻²)",
        fontsize=13, fontweight="bold",
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 35)
    out = os.path.join(save_dir, "throughput_vs_snr.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out}")
