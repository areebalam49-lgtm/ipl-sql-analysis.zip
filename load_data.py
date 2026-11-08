"""Load Kaggle's IPL Complete Dataset (matches.csv + deliveries.csv) into ipl.db.

Usage:  python load_data.py   (matches.csv and deliveries.csv or deliveries.csv.zip in this folder)

Cleaning done here:
  * seasons like "2007/08" or "2020/21" become a single year (2008, 2020)
  * renamed franchises are mapped to their current name
  * duplicate spellings of the same ground are merged
  * overs are stored as 1-20 (the source file counts from 0)
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
DB = HERE / "ipl.db"

TEAM_NAMES = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Deccan Chargers": "Deccan Chargers",          # defunct; kept separate from Sunrisers
}


def season_year(s) -> int:
    """'2007/08' -> 2008 (the IPL year), '2020/21' -> 2020 (played in 2020), '2015' -> 2015."""
    s = str(s).strip()
    m = re.match(r"^(\d{4})/(\d{2})$", s)
    if m:
        start, end = int(m.group(1)), 2000 + int(m.group(2))
        return 2020 if start == 2020 else end
    return int(float(s))


def clean_venue(v: str) -> str:
    v = str(v).strip()
    v = re.sub(r"\s+", " ", v)
    v = v.split(",")[0].strip()                     # "Wankhede Stadium, Mumbai" -> "Wankhede Stadium"
    v = v.replace("M.Chinnaswamy", "M Chinnaswamy").replace("Punjab Cricket Association IS Bindra Stadium",
                                                             "Punjab Cricket Association Stadium")
    v = v.replace("Feroz Shah Kotla", "Arun Jaitley Stadium")
    v = v.replace("Sardar Patel Stadium", "Narendra Modi Stadium")
    if v == "Zayed Cricket Stadium":
        v = "Sheikh Zayed Stadium"                  # same ground in Abu Dhabi
    return v


def pick(df, *names):
    for n in names:
        if n in df.columns:
            return df[n]
    raise KeyError(f"none of {names} found in columns {list(df.columns)}")


def main():
    m = pd.read_csv(HERE / "matches.csv")
    deliv = HERE / "deliveries.csv"
    if not deliv.exists():                          # zipped copy kept small enough for GitHub
        deliv = HERE / "deliveries.csv.zip"
    d = pd.read_csv(deliv, low_memory=False)
    team = lambda x: TEAM_NAMES.get(str(x).strip(), str(x).strip()) if pd.notna(x) else None

    m["season_y"] = m["season"].map(season_year)
    m["venue_c"] = m["venue"].map(clean_venue)
    for c in ("team1", "team2", "toss_winner", "winner"):
        m[c] = m[c].map(team)
    d["batting_team"] = d["batting_team"].map(team)
    d["bowling_team"] = d["bowling_team"].map(team)
    batter = pick(d, "batter", "batsman")

    teams = sorted(set(m.team1) | set(m.team2) | set(d.batting_team) | set(d.bowling_team))
    team_id = {t: i + 1 for i, t in enumerate(teams)}
    venues = (m.groupby("venue_c")["city"].agg(lambda s: s.dropna().mode().iat[0] if s.notna().any() else None)
              .reset_index())
    venue_id = {v: i + 1 for i, v in enumerate(venues.venue_c)}
    names = sorted(set(batter) | set(d.bowler) | set(d.player_dismissed.dropna()))
    player_id = {p: i + 1 for i, p in enumerate(names)}

    over = d["over"].astype(int)
    over_no = over + 1 if over.min() == 0 else over

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript((HERE / "schema.sql").read_text())
    con.executemany("INSERT INTO teams VALUES (?,?)", [(i, t) for t, i in team_id.items()])
    con.executemany("INSERT INTO venues VALUES (?,?,?)",
                    [(venue_id[r.venue_c], r.venue_c, r.city) for r in venues.itertuples()])
    con.executemany("INSERT INTO players VALUES (?,?)", [(i, p) for p, i in player_id.items()])

    nz = lambda x: None if pd.isna(x) else x
    con.executemany("INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [
        (int(r.id), int(r.season_y), str(r.date)[:10], nz(getattr(r, "match_type", None)),
         venue_id[r.venue_c], team_id[r.team1], team_id[r.team2],
         team_id.get(r.toss_winner), nz(r.toss_decision), team_id.get(r.winner),
         nz(r.result), nz(r.result_margin), nz(r.player_of_match),
         nz(getattr(r, "super_over", None)), nz(getattr(r, "method", None)))
        for r in m.itertuples()])

    rows = zip(d.match_id.astype(int), d.inning.astype(int), over_no, d.ball.astype(int),
               d.batting_team.map(team_id), d.bowling_team.map(team_id),
               batter.map(player_id), d.bowler.map(player_id),
               pick(d, "batsman_runs", "batter_runs").astype(int), d.extra_runs.astype(int),
               d.total_runs.astype(int), d.extras_type.where(d.extras_type.notna(), None),
               d.is_wicket.astype(int), d.dismissal_kind.where(d.dismissal_kind.notna(), None),
               d.player_dismissed.map(player_id).where(d.player_dismissed.notna(), None))
    con.executemany("INSERT INTO deliveries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [tuple(None if (isinstance(v, float) and pd.isna(v)) else (int(v) if hasattr(v, "item") and not isinstance(v, str) else v) for v in r) for r in rows])
    con.commit()
    for t in ("teams", "venues", "players", "matches", "deliveries"):
        print(f"{t:12s}{con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>10,}")
    print("seasons:", con.execute("SELECT MIN(season), MAX(season) FROM matches").fetchone())
    con.close()


if __name__ == "__main__":
    main()
