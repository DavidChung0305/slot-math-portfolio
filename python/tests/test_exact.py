from pathlib import Path

import numpy as np
import pytest

from sim.simulate import simulate_spins
from slotmath.exact import (all_board_wins, board_win, load_config, symbol_win,
                            total_moments, window_counts)

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
    # 5 S (one on every reel) -> 2500 = 50x bet, the maximum base-game win
    # T and K stop at 2 in a row (reel 3 has neither them nor W)
    #    T  A  H2 K  T
    #    S  W  A  S  S
    #    K  S  S  W  A
    config, counts, s_counts = game
    assert board_win([0, 4, 7, 4, 3], counts, s_counts, config) == 2500


def test_max_win_over_all_boards(all_wins):
    # exhaustive: no board pays more than 5 S
    assert all_wins.max() == 2500
    assert (all_wins == 2500).sum() == 3**5


def test_base_rtp_regression(all_wins):
    # total points over all 30^5 boards; RTP 0.5136737 cross-checked with Excel Scatter!F7
    assert all_wins.sum() == 624_113_505


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
