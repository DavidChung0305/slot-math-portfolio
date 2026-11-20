"""Compute PAR Sheet statistics and write them as CSV files for Excel (Power Query).

Run from the python/ folder:  python -m sim.export_par
"""
from pathlib import Path

import numpy as np
import pandas as pd

from slotmath.exact import (all_board_wins, load_config, moments,
                            payout_distribution, total_moments)
from sim.simulate import simulate_spins

ROOT = Path(__file__).resolve().parents[2]       # slot-math-portfolio/
CONFIG = ROOT / "config" / "game.json"
OUT = ROOT / "excel" / "data"

N = 1_000_000
SEED = 2026
EDGES = [0, 1, 5, 20, 100]
Z95 = 1.96


def main():
    config = load_config(CONFIG)
    bet = config["bet"]

    # Theory: exhaustive base game + first-step analysis for free games
    base_wins = all_board_wins(config)
    base_mean, base_var, base_sd = moments(base_wins, bet)
    total_mean, total_var, total_sd = total_moments(config)

    # Simulation: base game + free games with retriggers
    sim = simulate_spins(config, N, SEED)
    x = sim / bet
    sim_mean = x.mean()
    sim_sd = x.std(ddof=1)
    half = Z95 * sim_sd / np.sqrt(N)

    stats = pd.DataFrame([
        ("RTP_Base", base_mean),
        ("Var_Base", base_var),
        ("SD_Base", base_sd),
        ("RTP_Total", total_mean),
        ("Var_Total", total_var),
        ("SD_Total", total_sd),
        ("VI", Z95 * total_sd),
        ("Sim_N", N),
        ("Sim_Seed", SEED),
        ("Sim_RTP", sim_mean),
        ("Sim_CI_Low", sim_mean - half),
        ("Sim_CI_High", sim_mean + half),
        ("Sim_SD", sim_sd),
        ("Sim_Max", x.max()),
    ], columns=["Metric", "Value"])

    base_dist = payout_distribution(base_wins, bet, EDGES)
    sim_dist = payout_distribution(sim, bet, EDGES)
    # "(lo,hi]" labels: Excel would read "1-5" as a date (Jan 5)
    labels = ["0"] + [f"({lo},{hi}]" for lo, hi in zip(EDGES[:-1], EDGES[1:])] + [f">{EDGES[-1]}"]
    dist = pd.DataFrame({
        "Interval": labels,
        "P_Base": [p for _, p in base_dist],
        "P_Total": [p for _, p in sim_dist],
    })
    dist["P_Total_Err"] = Z95 * np.sqrt(dist["P_Total"] * (1 - dist["P_Total"]) / N)

    OUT.mkdir(parents=True, exist_ok=True)
    stats.to_csv(OUT / "par_stats.csv", index=False)
    dist.to_csv(OUT / "par_dist.csv", index=False)
    print(stats.to_string(index=False))
    print()
    print(dist.to_string(index=False))


if __name__ == "__main__":
    main()
