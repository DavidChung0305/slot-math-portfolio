"""Theory vs simulation comparison table (Day 8).

Run from the python/ folder:  python -m sim.compare
Writes docs/compare.md (markdown tables for the README) and prints them.

Pass rule: |z| <= 1.96, where z = (simulated - theory) / SE.
With 6 metrics, P(at least one fails by luck) = 1 - 0.95^6 ~ 26%,
so a single failure means "rerun with other seeds", not "bug".
"""
from pathlib import Path

import numpy as np
import pandas as pd

from slotmath.exact import (all_board_awards, all_board_scatter_pays,
                            all_board_wins, load_config, moments,
                            total_moments)
from sim.simulate import simulate_detailed

ROOT = Path(__file__).resolve().parents[2]       # slot-math-portfolio/
CONFIG = ROOT / "config" / "game.json"
OUT = ROOT / "docs" / "compare.md"

N = 10_000_000
SEED = 2026
EDGES = [0, 1, 5, 20, 100]
Z95 = 1.96


def theory(config):
    """Exact values from exhaustive enumeration + first-step analysis."""
    bet = config["bet"]
    wins = all_board_wins(config)
    line = wins - all_board_scatter_pays(config)
    awards = all_board_awards(config)

    base_rtp, _, base_sd = moments(wins, bet)
    total_rtp, _, total_sd = total_moments(config)
    return {
        "total_rtp": total_rtp, "total_sd": total_sd,
        "base_rtp": base_rtp, "base_sd": base_sd,
        "fg_rtp": total_rtp - base_rtp,
        "hit": (line > 0).mean(),
        "trigger": (awards > 0).mean(),
        "base_wins": wins,
    }


def bin_probs(x):
    """P(win in each interval), x in multiples of bet. Labels '(lo,hi]'."""
    rows = [("0", (x == 0).mean())]
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        rows.append((f"({lo},{hi}]", ((x > lo) & (x <= hi)).mean()))
    rows.append((f">{EDGES[-1]}", (x > EDGES[-1]).mean()))
    return rows


def metric_table(th, sim, bet):
    t = sim["total"] / bet
    b = sim["base"] / bet
    fg = t - b                                  # free-game win per base spin
    n = t.size
    s = t.std(ddof=1)
    kurt = ((t - t.mean())**4).mean() / t.var()**2
    hit = (sim["line"] > 0).mean()
    trig = (sim["awards"] > 0).mean()

    def p_se(p):                                # SE of a simulated proportion
        return np.sqrt(p * (1 - p) / n)

    # (metric, unit, theory, simulated, SE, how SE is computed)
    rows = [
        ("總 RTP", "%", th["total_rtp"], t.mean(), th["total_sd"] / np.sqrt(n), "σ_total/√N"),
        ("主遊戲 RTP", "%", th["base_rtp"], b.mean(), th["base_sd"] / np.sqrt(n), "σ_base/√N"),
        ("免費遊戲 RTP", "%", th["fg_rtp"], fg.mean(), fg.std(ddof=1) / np.sqrt(n), "s_FG/√N"),
        ("命中頻率（連線贏分 > 0）", "%", th["hit"], hit, p_se(th["hit"]), "√(p(1−p)/N)"),
        ("觸發頻率", "%", th["trigger"], trig, p_se(th["trigger"]), "√(p(1−p)/N)"),
        ("σ_total（押注倍數）", "x", th["total_sd"], s,
         th["total_sd"] * np.sqrt((kurt - 1) / (4 * n)), f"σ·√((κ−1)/4N), κ={kurt:.0f}"),
    ]
    df = pd.DataFrame(rows, columns=["指標", "unit", "理論", "模擬", "SE", "SE 公式"])
    df["差距"] = df["模擬"] - df["理論"]
    df["z"] = df["差距"] / df["SE"]
    df["通過"] = np.where(df["z"].abs() <= Z95, "✓", "✗")
    return df


def dist_table(th, sim, bet):
    n = sim["base"].size
    base_th = bin_probs(th["base_wins"] / bet)
    base_sim = bin_probs(sim["base"] / bet)
    total_sim = bin_probs(sim["total"] / bet)
    rows = []
    for (label, p), (_, q), (_, r) in zip(base_th, base_sim, total_sim):
        se = np.sqrt(p * (1 - p) / n)
        z = (q - p) / se if se > 0 else 0.0
        rows.append((label, p, q, z, "✓" if abs(z) <= Z95 else "✗",
                     r, Z95 * np.sqrt(r * (1 - r) / n)))
    return pd.DataFrame(rows, columns=["區間（押注倍數）", "主遊戲理論", "主遊戲模擬", "z", "通過",
                                       "含免費遊戲模擬", "± 95%"])


def fmt(v, unit):
    return f"{v:.4%}" if unit == "%" else f"{v:.4f}"


def to_markdown(df_m, df_d):
    lines = [
        f"# 理論值 vs 模擬值（N = {N:,} 轉，seed = {SEED}）",
        "",
        "通過標準：|z| ≤ 1.96，z = (模擬 − 理論) / SE。",
        "",
        "| 指標 | 理論 | 模擬 | 差距 | SE | z | 通過 |",
        "|---|---:|---:|---:|---:|---:|:---:|",
    ]
    for _, r in df_m.iterrows():
        u = r["unit"]
        lines.append(f"| {r['指標']} | {fmt(r['理論'], u)} | {fmt(r['模擬'], u)} | "
                     f"{fmt(r['差距'], u)} | {fmt(r['SE'], u)}（{r['SE 公式']}） | "
                     f"{r['z']:+.2f} | {r['通過']} |")
    lines += [
        "",
        "## 派彩區間分佈",
        "",
        "主遊戲有窮舉理論值可對照；含免費遊戲的分佈沒有封閉解，只列模擬值 ± 95% 誤差。",
        "",
        "| 區間（押注倍數） | 主遊戲理論 | 主遊戲模擬 | z | 通過 | 含免費遊戲模擬 | ± 95% |",
        "|---|---:|---:|---:|:---:|---:|---:|",
    ]
    for _, r in df_d.iterrows():
        lines.append(f"| {r['區間（押注倍數）']} | {r['主遊戲理論']:.4%} | {r['主遊戲模擬']:.4%} | "
                     f"{r['z']:+.2f} | {r['通過']} | {r['含免費遊戲模擬']:.4%} | {r['± 95%']:.4%} |")
    lines += [
        "",
        "## 怎麼讀 ✗",
        "",
        "兩張表共 12 項檢定，每項即使程式完全正確也有 5% 機會 |z| > 1.96，"
        "至少一項 ✗ 的機率約 1 − 0.95¹² ≈ 46%。"
        "出現 ✗ 時先換種子重跑：每次都在同一項、同一方向失敗才是系統性錯誤。",
    ]
    return "\n".join(lines) + "\n"


def main():
    config = load_config(CONFIG)
    bet = config["bet"]
    th = theory(config)
    sim = simulate_detailed(config, N, SEED)

    md = to_markdown(metric_table(th, sim, bet), dist_table(th, sim, bet))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
