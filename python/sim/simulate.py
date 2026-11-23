import numpy as np

from slotmath.exact import all_board_wins, all_board_awards, all_board_scatter_pays


def simulate_detailed(config, n, seed):
    """Simulate n base-game spins and return the parts of each spin (all int64 arrays, points):

    total:  base win + all free-game wins (incl. retriggers)
    base:   base-board win (line wins + scatter pay)
    line:   base-board line (ways) win only, no scatter pay -> used for hit frequency
    awards: free spins awarded by the base board (0 = no trigger)
    """
    wins = all_board_wins(config).ravel()
    awards = all_board_awards(config).ravel()
    line_wins = wins - all_board_scatter_pays(config).ravel()
    mult = config["free_game"]["multiplier"]
    rng = np.random.default_rng(seed)

    idx = rng.integers(0, wins.size, size=n)
    base = wins[idx]
    total = base.copy()
    pending = awards[idx]
    initial_awards = pending.copy()

    # one round = every spin that still has free spins left plays one more free spin
    while (pending > 0).any():
        k = np.flatnonzero(pending > 0)
        j = rng.integers(0, wins.size, size=k.size)
        total[k] += mult * wins[j]
        pending[k] += awards[j] - 1

    return {"total": total, "base": base, "line": line_wins[idx], "awards": initial_awards}


def simulate_spins(config, n, seed):
    """Simulate n base-game spins; return total win (points, int64) of each,
    including all free spins and retriggers."""
    return simulate_detailed(config, n, seed)["total"]
