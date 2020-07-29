# cyberdwarf

Tools for fantasy basketball

## TODO

x Get the other games and incorporate into pipeline
x Get active players
x Normalize stats and calculate baseline scores
  x import all stats
  x convert to useful stuff
  x determine absolute avg, std_dev for each stat
  x determine avg, std_dev per player for each stat
  x add together the important stats
- Have available:
  - players sorted by normalized stats
    x operationalize
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
