from dataclasses import dataclass
import itertools
from typing import Dict, List, Optional, Tuple

import pandas as pd

from nba import position_order, SCORED_STATS


@dataclass
class Player:
    name: str
    position: str
    team: str
    stats: pd.Series

    @property    
    def is_guard(self):
        return self.position == "G"

    @property
    def is_big(self):
        return self.position in ("F", "C")

    @property
    def is_flex(self):
        return self.position == "X"

    @property
    def is_rookie(self):
        return self.stats["rookie"] == "X"

    @property
    def is_special(self):
        return self.stats["special"] == "X"

    @property
    def z_score(self):
        if self.is_special:
            return self.stats["player_z_adj"]
        else:
            return self.stats["player_z"]
    


class Lineup:
    def __init__(self, owner: str, players: Optional[List[Player]] = None):
        self.owner = owner
        self.players = players or []

    def __repr__(self):
        sorted_players = sorted(
            self.players, 
            key=lambda p: f"{position_order(p.position)}{p.name}"
        )
        return f"Lineup({[(p.name, p.position) for p in sorted_players]})"

    @property
    def num_guards(self) -> int:
        return sum(1 for p in self.players if p.is_guard)

    @property
    def num_bigs(self) -> int:
        return sum(1 for p in self.players if p.is_big)

    @property
    def is_valid(self) -> int:
        return (
            len(self.players) == 5 and self.num_guards <= 2 and self.num_bigs <= 3
        )

    def add_if_possible(self, p: Player) -> bool:
        if len(self.players) >= 5:
            return False

        if p.is_guard and self.num_guards >= 2:
            return False
        if p.is_big and self.num_bigs >= 3:
            return False

        self.players.append(p)
        return True

    @property
    def player_stats(self) -> pd.DataFrame:
        player_df = pd.DataFrame([p.stats for p in self.players])

        combined_stats = []
        for stat, measure in itertools.product(SCORED_STATS, ["z", "mean", "std"]):
            s = f"{stat}_{measure}"
            player_df[f"{s}"] = player_df[f"{s}_adj"].combine_first(player_df[s])
            combined_stats.append(s)

        player_df["owner"] = self.owner
        return player_df[["owner", "player"] + combined_stats]


@dataclass
class FantasyTeam:
    data: pd.DataFrame

    def __post_init__(self):
        self.owner = self.data["owner"].iloc[0]
        self.players = [
            Player(name=p["player"], position=p["position"], team=p["team"], stats=p,)
            for p in self.data.T.to_dict().values()
        ]
        self.default_lineup = self.determine_default_lineup()
        self.max_z_lineup = self.determine_max_z_lineup()

    def determine_default_lineup(self) -> Lineup:
        lineup = Lineup(self.owner)
        for p in self.players:
            lineup.add_if_possible(p)

        assert lineup.is_valid, "Could not form valid lineup"
        return lineup

    def determine_max_z_lineup(self) -> Lineup:
        lineup = Lineup(self.owner)
        sorted_p = sorted(self.players, key=lambda p: p.z_score, reverse=True)

        for p in sorted_p:
            lineup.add_if_possible(p)

        assert lineup.is_valid, "Could not form valid lineup"
        return lineup

    def all_possible_lineups(self) -> List[Lineup]:
        combinations = itertools.combinations(self.players, 5)
        possible_lineups = [Lineup(self.owner, players=list(c)) for c in combinations]
        return [l for l in possible_lineups if l.is_valid]


@dataclass
class Week:
    lineups: List[Lineup]

    def __post_init__(self):
        self.results_by_averages = self.score_by_averages()

    def totals_by_averages(self):
        all_stats = pd.concat([l.player_stats for l in self.lineups])
        relevant_stats = all_stats[["owner"] + [f"{s}_mean" for s in SCORED_STATS]]
        results = pd.DataFrame(relevant_stats.groupby("owner").sum())
        return results.rename(columns={f"{s}_mean": s for s in SCORED_STATS})

    def score(self, totals: pd.DataFrame):
        for s in SCORED_STATS:
            totals[f"{s}_rank"] = totals[s].rank()

        ranks = totals[[f"{s}_rank" for s in SCORED_STATS]].T.sum()
        return ranks, totals.T

    def score_by_averages(self):
        totals = self.totals_by_averages()
        return self.score(totals)
        
