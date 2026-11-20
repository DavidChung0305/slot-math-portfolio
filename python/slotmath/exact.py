import json
import numpy as np


def load_config(path):
    """Read game.json and return it as a dict."""
    with open(path, encoding="utf-8") as f:
        config = json.load(f)
    return config


def window_counts(reel, symbols, rows=3, wild=None):
    """Count each symbol (plus wilds) visible in the window at every stop position."""
    L = len(reel)
    counts = np.zeros((L, len(symbols)), dtype=int)
    for p in range(L):
        window = [reel[(p + k) % L] for k in range(rows)]
        for j, sym in enumerate(symbols):
            counts[p, j] = window.count(sym)
            if wild is not None:
                counts[p, j] += window.count(wild)
    return counts


def symbol_win(c, pays):
    """Ways win (in points) for one symbol on one board.

    c:    counts on reels 1-5, e.g. [1, 2, 1, 0, 3]
    pays: paytable for this symbol, e.g. {"3": 10, "4": 30, "5": 100}
    """
    ways3 = c[0] * c[1] * c[2]
    if c[3] == 0:
        return ways3 * pays["3"]
    if c[4] == 0:
        return ways3 * c[3] * pays["4"]
    return ways3 * c[3] * c[4] * pays["5"]


def board_win(stops, counts, s_counts, config):
    """Total win (in points) of one board: all symbol ways wins + scatter pay.

    stops:    stop position on each reel, e.g. [2, 3, 0, 4, 7]
    counts:   list of 5 arrays from window_counts (symbols with wild)
    s_counts: list of 5 arrays from window_counts(reel, ["S"])
    config:   dict from load_config
    """
    paytable = config["paytable"]
    total = 0
    for j, sym in enumerate(paytable):
        c = [counts[i][stops[i], j] for i in range(5)]
        total += symbol_win(c, paytable[sym])
    n_scatter = sum(s_counts[i][stops[i], 0] for i in range(5))
    total += config["scatter"]["pays"].get(str(n_scatter), 0)
    return int(total)


def expand(arr, axis):
    """Put a 1-D array on the given axis of a 5-D shape."""
    shape = [1, 1, 1, 1, 1]
    shape[axis] = len(arr)
    return arr.reshape(shape)


def all_board_wins(config):
    """Total win (in points) of every board, as a 5-D array of shape (L1, L2, L3, L4, L5).

    wins[p1, p2, p3, p4, p5] == board_win([p1, p2, p3, p4, p5], ...)
    """
    reels = config["reels"]
    paytable = config["paytable"]
    symbols = list(paytable)

    counts = [window_counts(r, symbols, wild=None if i == 0 else "W")
              for i, r in enumerate(reels)]
    s_counts = [window_counts(r, ["S"]) for r in reels]

    wins = np.zeros([len(r) for r in reels], dtype=np.int64)

    for j, sym in enumerate(symbols):
        c1, c2, c3, c4, c5 = (expand(counts[i][:, j], i) for i in range(5))
        pays = paytable[sym]
        tail = np.where(c4 == 0,
                        pays["3"],
                        c4 * np.where(c5 == 0, pays["4"], c5 * pays["5"]))
        wins += c1 * c2 * c3 * tail

    n_scatter = sum(expand(s_counts[i][:, 0], i) for i in range(5))
    scatter_pay = np.zeros(6, dtype=np.int64)
    for k, pay in config["scatter"]["pays"].items():
        scatter_pay[int(k)] = pay
    wins += scatter_pay[n_scatter]

    return wins


def all_board_awards(config):
    """Free spins awarded on every board, as a 5-D array (same shape as all_board_wins)."""
    reels = config["reels"]
    s_counts = [window_counts(r, ["S"]) for r in reels]
    n_scatter = sum(expand(s_counts[i][:, 0], i) for i in range(5))

    awards = np.zeros(6, dtype=np.int64)
    for k, spins in config["free_game"]["awards"].items():
        awards[int(k)] = spins

    return awards[n_scatter]


def moments(wins, bet):
    """Return (mean, variance, sd) of the win per spin, in multiples of bet."""
    n = wins.size
    mean = wins.sum() / n / bet          # E[X]：總點數 ÷ 盤面數 ÷ 押注
    ex2 = (wins**2).sum() / n / bet**2   # E[X²]：(點數²) 加總 ÷ 盤面數 ÷ 押注²
    var = ex2 - mean**2                  # 捷徑公式
    sd = np.sqrt(var)
    return mean, var, sd


def payout_distribution(wins, bet, edges):
    """Probability of the win falling in each interval (in multiples of bet).

    edges: interval boundaries, e.g. [0, 1, 5, 20, 100]
    returns: list of (label, probability)
    """
    x = wins / bet
    result = [("0", (x == 0).mean())]
    for lo, hi in zip(edges[:-1], edges[1:]):
        p = ((x > lo) & (x <= hi)).mean()
        result.append((f"{lo}-{hi}", p))
    result.append((f">{edges[-1]}", (x > edges[-1]).mean()))
    return result
