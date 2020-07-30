# 2020-07-29 (setting roster)

- Pick my roster
  - ~~fill in team and position for every player~~
  - fill in estimated stats for special cases
    - ~~Bol Bol~~
    - ~~Zion~~
    - ~~Oladipo~~
  - collect basic lineup options:
    - default (first 5 with valid positions)
    - max total z-score
    - max stat rankings:
      - assuming default other lineups
      - assuming max z-score other lineups
  - fill in fake games for special cases?
  - build ability to Monte Carlo a set of lineups
    - per player, pick 4 games at random from their games played this year
    - score the whole league
    - run N simulations
  - test my possible lineups against the options
  - tune values:
    - different values for special players
    - treat rookies differently
    - prefer to pick games on their current team (relevant for any player?)
  - look at the schedule and pick the actual games

# 2020-07-24 (pre-draft)

- ~~Get the other games and incorporate into pipeline~~
- ~~Get active players~~
- ~~Normalize stats and calculate baseline scores~~
  - ~~import all stats~~
  - ~~convert to useful stuff~~
  - ~~determine absolute avg, std_dev for each stat~~
  - ~~determine avg, std_dev per player for each stat~~
  - ~~add together the important stats~~
- Have available:
  - players sorted by normalized stats
    - ~~operationalize~~
    - drop irrelevant players from the cohort and rescore
    - add position, team, team standings/notes, stds
  - standings/schedule
  - injury reports
  - dashboard for updating everyone's team
- Quick research about players who haven't played at all
  - news stories
  - make a wildcards sheet
  - update dashboard with some default values for wildcards

- Check out results of scrimmages
- Further refine:
  - add mp_mean, games_played to player stats
  - Identify team standings, usual minutes --> predict future minutes
  - Compare:
    - review players who've barely played at all
    - cut worst players
    - excluding games against non-bubble teams
    - per game vs per 36 minutes
    - first 20 vs second 20 vs third 20
