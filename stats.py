from typing import List, Optional

import pandas as pd
from unidecode import unidecode_expect_ascii


SCORED_STATS = ["pts", "trb", "ast", "stl", "blk", "fg3"]


def cohort_overall_stats(df: pd.DataFrame) -> pd.DataFrame:
    means = df[SCORED_STATS].mean().to_frame()
    stds = df[SCORED_STATS].std().to_frame()
    
    overall_stats = means.merge(stds, left_index=True, right_index=True)
    overall_stats.columns = ["mean", "std"]

    stacked = overall_stats.stack()
    stacked.index = stacked.index.map('{0[0]}_{0[1]}'.format)
    return stacked.to_frame().T


def cohort_player_stats(df: pd.DataFrame) -> pd.DataFrame:
    players = df.groupby(["player", "team"])

    means = players[SCORED_STATS].mean()
    stds = players[SCORED_STATS].std()
    
    player_stats = means.merge(stds, left_index=True, right_index=True)
    player_stats.columns = (
      [f"{s}_mean" for s in SCORED_STATS] +
      [f"{s}_std" for s in SCORED_STATS]
    )
    return player_stats


def cross_join(
    df1:pd.DataFrame,
    df2:pd.DataFrame, 
    suffixes: Optional[List[str]] = None
) -> pd.DataFrame:
    df1["tmp"] = 1
    df2["tmp"] = 1
    kwargs = {"on": "tmp"}
    if suffixes:
        kwargs["suffixes"] = suffixes

    joined = pd.merge(df1, df2, **kwargs)
    joined.drop('tmp', axis=1)
    return joined


def score_cohort(df: pd.DataFrame) -> pd.DataFrame:
    # Drop DNPs and select only the stats we care about
    relevant_stats = ["player", "team", "opponent", "date", "mp"] + SCORED_STATS
    preprocessed = df[df.mp.notnull()][relevant_stats]

    # Get means and std_devs overall and by player, and join
    overall_stats = cohort_overall_stats(preprocessed)
    player_stats = cohort_player_stats(preprocessed)
    # Drop diacriticals
    player_stats["player_raw"] = player_stats.index.map('{0[0]}'.format)
    player_stats["player"] = player_stats["player_raw"].apply(unidecode_expect_ascii)
    player_stats["team"] = player_stats.index.map('{0[1]}'.format)
    combined = cross_join(
        player_stats,
        overall_stats,
        suffixes=["", "_overall"],
    )
    combined.index = combined["player"]
    
    # Calculate z-scores
    for s in SCORED_STATS:
        combined[f"{s}_z"] = (combined[f"{s}_mean"] - combined[f"{s}_mean_overall"]) / combined[f"{s}_std_overall"]
    combined["player_z"] = sum([combined[f"{s}_z"] for s in SCORED_STATS])


    cols = ["team", "player_z"]
    for s in SCORED_STATS:
        cols += [f"{s}_z", f"{s}_mean", f"{s}_std"]
    return combined[cols].sort_values(by=["player_z"], ascending=False)
