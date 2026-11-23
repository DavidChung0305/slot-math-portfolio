from pathlib import Path

import numpy as np
import pytest

from sim.simulate import simulate_detailed, simulate_spins
from slotmath.exact import (all_board_scatter_pays, all_board_wins, board_win,
                            load_config, symbol_win, total_moments, window_counts)

CONFIG = Path(__file__).resolve().parents[2] / "config" / "game.json"


@pytest.fixture(scope="module")
def game():
    """Load game.json once and build the window-count tables used by board_win."""
    config = load_config(CONFIG)
    reels = config["reels"]
    symbols = list(config["paytable"])
    counts = [window_counts(r, symbols, wild=None if i == 0 else "W")
              for i, r in enumerate(reels)]
    s_counts = [window_counts(r, ["S"]) for r in reels]
    return config, counts, s_counts


@pytest.fixture(scope="module")
def all_wins(game):
    """Win (points) of every one of the 30^5 base-game boards."""
    config, _, _ = game
    return all_board_wins(config)


def test_symbol_win_three_of_a_kind():
    pays = {"3": 10, "4": 30, "5": 100}
    assert symbol_win([1, 2, 1, 0, 3], pays) == 20

def test_symbol_win_four_of_a_kind():
    pays = {"3": 10, "4": 30, "5": 100}
    # 2 x 1 x 1 x 3 = 6 ways, reel 5 has none -> 6 x 30
    assert symbol_win([2, 1, 1, 3, 0], pays) == 180


def test_symbol_win_five_of_a_kind():
    pays = {"3": 10, "4": 30, "5": 100}
    # 1 x 1 x 2 x 1 x 2 = 4 ways -> 4 x 100
    assert symbol_win([1, 1, 2, 1, 2], pays) == 400


def test_symbol_win_reel1_missing():
    pays = {"3": 10, "4": 30, "5": 100}
    assert symbol_win([0, 1, 2, 3, 2], pays) == 0


def test_symbol_win_gap_on_reel3():
    pays = {"3": 10, "4": 30, "5": 100}
    assert symbol_win([1, 2, 0, 3, 2], pays) == 0


def test_board_win_scatter_exactly_three(game):
    # reel 1 middle, reel 4 bottom, reel 5 bottom = 3 S -> 100; no line wins
    #    T  J  A  A  Q
    #    S  T  J  K  T
    #    K  Q  Q  S  S
    config, counts, s_counts = game
    assert board_win([0, 0, 4, 3, 2], counts, s_counts, config) == 100


def test_board_win_scatter_exactly_two(game):
    # reel 1 middle, reel 5 bottom = only 2 S -> no scatter pay; no line wins
    #    T  J  A  J  Q
    #    S  T  J  T  T
    #    K  Q  Q  Q  S
    config, counts, s_counts = game
    assert board_win([0, 0, 4, 0, 2], counts, s_counts, config) == 0


def test_board_win_max_win_five_scatters(game):
    # 5 S (one on every reel) -> 2500 = 50x bet (scatter only, no line wins)
    # T and K stop at 2 in a row (reel 3 has neither them nor W)
    #    T  A  H2 K  T
    #    S  W  A  S  S
    #    K  S  S  W  A
    config, counts, s_counts = game
    assert board_win([0, 4, 7, 4, 3], counts, s_counts, config) == 2500


def test_board_win_max_line_win(game):
    # K on reel 1 + W on reels 2-5: H1 1 way x700 + H2 1 way x400 + K 2*2*2*2 = 16 ways x140
    #    K  K  J  K  K
    #    H2 A  K  S  Q
    #    H1 W  W  W  W
    config, counts, s_counts = game
    assert board_win([18, 3, 1, 4, 6], counts, s_counts, config) == 700 + 400 + 16 * 140


def test_max_win_over_all_boards(all_wins):
    # exhaustive: since the v2 paytable (K 5-kind = 140), the W-heavy line board beats 5 S (2500)
    assert all_wins.max() == 3340
    assert (all_wins == 3340).sum() == 12
    assert (all_wins == 2500).sum() == 3**5


def test_base_rtp_regression(all_wins):
    # total points over all 30^5 boards; base RTP 0.6925627 (paytable v2, cross-checked with Excel Scatter!F7)
    assert all_wins.sum() == 841_463_640


def test_window_counts_wraps_around(game):
    # reel 2, stop 29: window = cells 29, 0, 1 = H3, J, T (wraps to the start)
    config, _, _ = game
    symbols = list(config["paytable"])          # H1 H2 H3 A K Q J T
    counts = window_counts(config["reels"][1], symbols)
    assert list(counts[29]) == [0, 0, 1, 0, 0, 0, 1, 1]


def test_window_counts_wild_adds_to_every_symbol(game):
    # reel 2, stop 4: window = A, W, S; W counts as every symbol, S is not a line symbol
    config, _, _ = game
    symbols = list(config["paytable"])          # H1 H2 H3 A K Q J T
    counts = window_counts(config["reels"][1], symbols, wild="W")
    assert list(counts[4]) == [1, 1, 1, 2, 1, 1, 1, 1]


def test_simulation_matches_theory(game):
    # total RTP by first-step analysis must lie within 4 sd/sqrt(N) of the simulated mean;
    # a correct program fails about 1 in 15,800 seeds (fixed seed -> deterministic)
    config, _, _ = game
    n = 1_000_000
    x = simulate_spins(config, n, seed=2026) / config["bet"]
    rtp, _, sd = total_moments(config)
    assert abs(x.mean() - rtp) < 4 * sd / np.sqrt(n)


def test_scatter_pays_split_off_line_win(game):
    # board [0, 4, 7, 4, 3] has 5 S and no line win: whole 2500 is scatter pay
    config, _, _ = game
    assert all_board_scatter_pays(config)[0, 4, 7, 4, 3] == 2500
    assert (all_board_wins(config) >= all_board_scatter_pays(config)).all()


def test_simulate_detailed_parts_are_consistent(game):
    # parts must add up: line <= base <= total; free-game win only where triggered;
    # simulate_spins must give exactly the same totals (same random stream)
    config, _, _ = game
    d = simulate_detailed(config, 100_000, seed=7)
    assert (d["line"] <= d["base"]).all()
    assert (d["base"] <= d["total"]).all()
    assert (d["total"][d["awards"] == 0] == d["base"][d["awards"] == 0]).all()
    assert (simulate_spins(config, 100_000, seed=7) == d["total"]).all()
