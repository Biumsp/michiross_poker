# %%
import random
import itertools
import pandas as pd
from alive_progress import alive_bar

# %%
def generate_random_play(deck, n_players, min_cards = 1, max_cards = 5):

    n_cards = random.randint(n_players*min_cards, n_players*max_cards)
    play = random.sample(deck, n_cards)

    return n_cards, n_players, play


def find_combinations(play):

    combs = {
        "one pair":         0,
        "two pairs":        0,
        "three of a kind":  0,
        "straight":         0,
        "flush":            0,
        "full house":       0,
        "four of a kind":   0,
        "straight flush":   0,
    }

    play.sort(key = lambda x: x[0])

    combs["one pair"]        = find_one_pair(play, is_sorted=True)
    combs["two pairs"]       = find_two_pairs(play, is_sorted=True)
    combs["three of a kind"] = find_three_of_a_kind(play, is_sorted=True)
    combs["four of a kind"]  = find_four_of_a_kind(play, is_sorted=True)
    combs["full house"]      = find_full_house(play, is_sorted=True)
    combs["straight"]        = find_straight(play)
    combs["flush"]           = find_flush(play)
    combs["straight flush"]  = find_straight_flush(play)

    return combs


def find_one_pair(play, is_sorted=False):

    if not is_sorted: play.sort(key = lambda x: x[0])
    
    for i in range(1, len(play)):
        if play[i-1][0] == play[i][0]: return 1

    return 0       


def find_two_pairs(play, is_sorted=False):

    if len(play) < 4: return 0

    if not is_sorted: play.sort(key = lambda x: x[0])

    pairs = 0

    for _, group in itertools.groupby(play, lambda x: x[0]): 
        if len(list(group)) > 1: pairs += 1

    return 1 if pairs > 1 else 0


def find_three_of_a_kind(play, is_sorted=False):

    if len(play) < 3: return 0

    if not is_sorted: play.sort(key = lambda x: x[0])

    for i in range(2, len(play)):
        if play[i-2][0] == play[i][0]: return 1

    return 0


def find_four_of_a_kind(play, is_sorted=False):

    if len(play) < 4: return 0

    if not is_sorted: play.sort(key = lambda x: x[0])
    
    for i in range(3, len(play)):
        if play[i-3][0] == play[i][0]: return 1

    return 0


def find_full_house(play, is_sorted=False):

    if len(play) < 5: return 0

    if not is_sorted: play.sort(key = lambda x: x[0])

    groups = []
    
    for _, group in itertools.groupby(play, lambda x: x[0]): 
        groups.append(len(list(group)))

    groups.sort(reverse=True)

    if groups[0] > 2 and groups[1] > 1: return 1

    return 0


def find_straight(play):

    play = list(set(c[0] for c in play))
    play.sort()
    
    if len(play) < 5: return 0

    for i in range(len(play)):
        if play[i-4] == play[i] - 4: return 1

    return 0


def find_flush(play):

    if len(play) < 5: return 0

    play.sort(key = lambda x: x[1])

    for _, group in itertools.groupby(play, lambda x: x[1]): 
        if len(list(group)) > 4: return 1

    return 0


def find_straight_flush(play):

    if len(play) < 5: return 0

    play.sort(key = lambda x: x[1])

    for _, group in itertools.groupby(play, lambda x: x[1]): 
        subplay = list(group)
        if find_straight(subplay) == 1: return 1

    return 0

# %%
values = range(5, 15)
suits = "HDCS"

deck = [(v, s) for v in values for s in suits]

active_players = [2, 3, 4, 5, 6]

df = pd.DataFrame(columns=[
    "active_players",
    "active_cards",
    "one pair",
    "two pairs",
    "three of a kind",
    "straight",
    "flush",
    "full house",
    "four of a kind",
    "straight flush"])

# %%
iterations_per_player = 5000

with alive_bar(sum(active_players)*iterations_per_player, force_tty = True) as bar:
        
    for i, ap in enumerate(active_players):

        for _ in range(ap*iterations_per_player):
            n_cards, n_players, play = generate_random_play(deck, ap)
            results = find_combinations(play)

            results.update({
                "active_players": n_players,
                "active_cards": n_cards,
            })

            df.loc[len(df)] = results

            bar()

# %%
df.groupby("active_players").mean().to_csv("results.csv")


