from datetime import date, datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from nba import Game


def get_games(symbol: str) -> List[Game]:
    response = requests.get(
        f"https://www.basketball-reference.com/teams/{symbol}/2020_games.html"
    )
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find(id="games")
    rows = table.tbody.find_all("tr")
    games = []

    for row in rows:
        if row.get("class") and "thead" in row.get("class"):
            continue
        date_string = row.find(attrs={"data-stat": "date_game"}).get("csk")
        game_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        link = date_string = row.find(attrs={"data-stat": "box_score_text"}).a.get(
            "href"
        )

        opponent = row.find(attrs={"data-stat": "opp_name"}).get("csk")[:3]
        at_home = row.find(attrs={"data-stat": "game_location"}).text == "@"
        if game_date > datetime.now().date():
            winner = None
        else:
            won = row.find(attrs={"data-stat": "game_result"}).text == "W"
            winner = symbol if won else opponent

        if at_home:
            games.append(Game(symbol, opponent, winner, game_date, link))
        else:
            games.append(Game(opponent, symbol, winner, game_date, link))

    return games


def parse_box_score(table, team: str, opponent: str, game_date: date) -> List[Dict]:
    rows = table.tbody.find_all("tr", class_=None)
    box_stats = []
    for row in rows:
        name = row.th.a.text
        stats = {"player": name}
        stats["team"] = team
        stats["opponent"] = opponent
        stats["date"] = game_date
        cols = row.find_all("td")

        if len(cols) > 1:
            for c in row.find_all("td"):
                stats[c["data-stat"]] = c.text

        box_stats.append(stats)
    return box_stats


def get_game_stats(game) -> List[Dict]:
    response = requests.get(f"https://www.basketball-reference.com/{game.link}")
    soup = BeautifulSoup(response.text, "html.parser")

    home = game.home
    home_table = soup.find(id=f"box-{home}-game-basic")

    away = game.away
    away_table = soup.find(id=f"box-{away}-game-basic")

    return parse_box_score(home_table, home, away, game.date) + parse_box_score(
        away_table, away, home, game.date
    )
