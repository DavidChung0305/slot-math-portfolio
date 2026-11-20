import numpy as np

from slotmath.exact import all_board_wins, all_board_awards


def simulate_spins(config, n, seed):
    """Simulate n base-game spins; return total win (points, int64) of each,
    including all free spins and retriggers."""
    wins = all_board_wins(config).ravel()
    awards = all_board_awards(config).ravel()
    mult = config["free_game"]["multiplier"]
    rng = np.random.default_rng(seed)

    idx = rng.integers(0, wins.size, size=n)
    total = wins[idx]
    pending = awards[idx]

    while (pending > 0).any():
        k = np.flatnonzero(pending > 0)
        j = rng.integers(0, wins.size, size=k.size)
        total[k] += mult * wins[j]
        pending[k] += awards[j] - 1

    return total
