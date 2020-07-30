from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional, Tuple


class Conference(Enum):
    EAST = "East"
    WEST = "West"


@dataclass
class Team:
    symbol: str
    city: str
    name: str
    conference: Conference


@dataclass
class Game:
    home: str
    away: str
    winner: Optional[str]
    date: date
    link: str

    def teams(self) -> Tuple[str, str]:
        return (self.home, self.away)


SCORED_STATS = ["pts", "trb", "ast", "stl", "blk", "fg3"]

TEAMS = [
    Team("BOS", "Boston", "Celtics", Conference.EAST),
    Team("BRK", "Brooklyn", "Nets", Conference.EAST),
    Team("IND", "Indiana", "Pacers", Conference.EAST),
    Team("MIA", "Miami", "Heat", Conference.EAST),
    Team("MIL", "Milwaukee", "Bucks", Conference.EAST),
    Team("ORL", "Orlando", "Magic", Conference.EAST),
    Team("PHI", "Philadelphia", "76ers", Conference.EAST),
    Team("TOR", "Toronto", "Raptors", Conference.EAST),
    Team("WAS", "Washington", "Wizards", Conference.EAST),
    Team("DAL", "Dallas", "Mavericks", Conference.WEST),
    Team("DEN", "Denver", "Nuggets", Conference.WEST),
    Team("HOU", "Houston", "Rockets", Conference.WEST),
    Team("LAC", "Los Angeles", "Clippers", Conference.WEST),
    Team("LAL", "Los Angeles", "Lakers", Conference.WEST),
    Team("MEM", "Memphis", "Grizzlies", Conference.WEST),
    Team("NOP", "New Orleans", "Pelicans", Conference.WEST),
    Team("OKC", "Oklahoma City", "Thunder", Conference.WEST),
    Team("PHO", "Phoenix", "Suns", Conference.WEST),
    Team("POR", "Portland", "Trail Blazers", Conference.WEST),
    Team("SAC", "Sacramento", "Kings", Conference.WEST),
    Team("SAS", "San Antonio", "Spurs", Conference.WEST),
    Team("UTA", "Utah", "Jazz", Conference.WEST),
]
OTHER_TEAMS = [
    Team("CHO", "Charlotte", "Hornets", Conference.EAST),
    Team("CHI", "Chicago", "Bulls", Conference.EAST),
    Team("NYK", "New York", "Knicks", Conference.EAST),
    Team("DET", "Detroit", "Pistons", Conference.EAST),
    Team("ATL", "Atlanta", "Hawks", Conference.EAST),
    Team("CLE", "Cleveland", "Cavaliers", Conference.EAST),
    Team("MIN", "Minnesota", "Timberwolves", Conference.WEST),
    Team("GSW", "Golden State", "Warriors", Conference.WEST),
]
ALL_TEAMS = TEAMS + OTHER_TEAMS


def position_order(position: str):
    if position == "G":
        return 0
    if position == "X":
        return 1
    if position == "F":
        return 2
    if position == "C":
        return 3
