-- =====================================================================
--  IPL Cricket Analysis (2008 onwards) - database schema
--  Engine: SQLite 3. Loaded from Kaggle's matches.csv and deliveries.csv
--  by load_data.py. Team names are mapped to their current franchise
--  (e.g. Delhi Daredevils -> Delhi Capitals) so history stays together.
-- =====================================================================

PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS v_balls;
DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS teams;

-- One row per franchise (current name)
CREATE TABLE teams (
    team_id     INTEGER PRIMARY KEY,
    team_name   TEXT NOT NULL UNIQUE
);

-- Grounds, with the city they are in
CREATE TABLE venues (
    venue_id    INTEGER PRIMARY KEY,
    venue_name  TEXT NOT NULL UNIQUE,
    city        TEXT
);

-- Every batter, bowler and fielder who appears in the data
CREATE TABLE players (
    player_id   INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL UNIQUE
);

-- One row per match
CREATE TABLE matches (
    match_id         INTEGER PRIMARY KEY,
    season           INTEGER NOT NULL,                 -- 2008, 2009, ...
    match_date       DATE    NOT NULL,
    match_type       TEXT,                             -- League, Qualifier 1, Eliminator, Final, ...
    venue_id         INTEGER REFERENCES venues(venue_id),
    team1_id         INTEGER NOT NULL REFERENCES teams(team_id),
    team2_id         INTEGER NOT NULL REFERENCES teams(team_id),
    toss_winner_id   INTEGER REFERENCES teams(team_id),
    toss_decision    TEXT CHECK (toss_decision IN ('bat', 'field')),
    winner_id        INTEGER REFERENCES teams(team_id), -- NULL = no result
    result           TEXT,                             -- runs, wickets, tie, no result
    result_margin    REAL,
    player_of_match  TEXT,
    super_over       TEXT,
    method           TEXT                              -- D/L when rain-affected
);

-- One row per ball bowled
CREATE TABLE deliveries (
    match_id             INTEGER NOT NULL REFERENCES matches(match_id),
    inning               INTEGER NOT NULL,             -- 1, 2 (3+ = super over)
    over_no              INTEGER NOT NULL,             -- 1 to 20
    ball                 INTEGER NOT NULL,
    batting_team_id      INTEGER NOT NULL REFERENCES teams(team_id),
    bowling_team_id      INTEGER NOT NULL REFERENCES teams(team_id),
    batter_id            INTEGER NOT NULL REFERENCES players(player_id),
    bowler_id            INTEGER NOT NULL REFERENCES players(player_id),
    batter_runs          INTEGER NOT NULL,
    extra_runs           INTEGER NOT NULL,
    total_runs           INTEGER NOT NULL,
    extras_type          TEXT,                         -- wides, noballs, byes, legbyes, penalty
    is_wicket            INTEGER NOT NULL CHECK (is_wicket IN (0, 1)),
    dismissal_kind       TEXT,
    player_dismissed_id  INTEGER REFERENCES players(player_id)
);

CREATE INDEX idx_matches_season     ON matches(season);
CREATE INDEX idx_deliv_match        ON deliveries(match_id);
CREATE INDEX idx_deliv_batter       ON deliveries(batter_id);
CREATE INDEX idx_deliv_bowler       ON deliveries(bowler_id);

-- Convenience view: every ball with names, season and match phase
CREATE VIEW v_balls AS
SELECT  d.*,
        m.season,
        bt.player_name                               AS batter,
        bw.player_name                               AS bowler,
        t1.team_name                                 AS batting_team,
        t2.team_name                                 AS bowling_team,
        CASE WHEN d.over_no <= 6  THEN 'Powerplay (1-6)'
             WHEN d.over_no <= 15 THEN 'Middle (7-15)'
             ELSE 'Death (16-20)' END                AS phase,
        -- a ball counts towards the batter's balls faced unless it is a wide
        CASE WHEN d.extras_type = 'wides' THEN 0 ELSE 1 END AS faced,
        -- a legal ball for the bowler excludes wides and no-balls
        CASE WHEN d.extras_type IN ('wides', 'noballs') THEN 0 ELSE 1 END AS legal,
        -- runs charged to the bowler exclude byes and leg-byes
        d.batter_runs + CASE WHEN d.extras_type IN ('wides', 'noballs') THEN d.extra_runs ELSE 0 END
                                                     AS bowler_runs,
        -- wickets credited to the bowler (run outs etc. are not)
        CASE WHEN d.is_wicket = 1 AND d.dismissal_kind NOT IN
                  ('run out', 'retired hurt', 'retired out', 'obstructing the field')
             THEN 1 ELSE 0 END                       AS bowler_wicket
FROM    deliveries d
JOIN    matches m  ON m.match_id  = d.match_id
JOIN    players bt ON bt.player_id = d.batter_id
JOIN    players bw ON bw.player_id = d.bowler_id
JOIN    teams   t1 ON t1.team_id  = d.batting_team_id
JOIN    teams   t2 ON t2.team_id  = d.bowling_team_id
WHERE   d.inning <= 2;                               -- super overs excluded
