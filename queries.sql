-- =====================================================================
--  IPL Cricket Analysis - 14 questions answered with SQL
--  Run against ipl.db. Each query starts with a "-- Qn." line.
-- =====================================================================

-- Q1. Does winning the toss help you win the match?
SELECT  COUNT(*)                                                   AS matches,
        SUM(toss_winner_id = winner_id)                            AS toss_winner_won,
        ROUND(100.0 * SUM(toss_winner_id = winner_id) / COUNT(*), 1) AS toss_win_pct
FROM    matches
WHERE   winner_id IS NOT NULL;

-- Q2. After winning the toss, is it better to bat or to field?
SELECT  toss_decision,
        COUNT(*)                                                   AS times_chosen,
        ROUND(100.0 * SUM(toss_winner_id = winner_id) / COUNT(*), 1) AS win_pct_for_toss_winner
FROM    matches
WHERE   winner_id IS NOT NULL
GROUP BY toss_decision;

-- Q3. Batting first or chasing: which wins more, season by season?
SELECT  season,
        COUNT(*)                                                   AS matches,
        ROUND(100.0 * AVG(CASE WHEN (toss_decision = 'bat'   AND winner_id = toss_winner_id)
                                 OR (toss_decision = 'field' AND winner_id <> toss_winner_id)
                               THEN 1.0 ELSE 0 END), 1)            AS bat_first_win_pct
FROM    matches
WHERE   winner_id IS NOT NULL AND result <> 'tie'
GROUP BY season
ORDER BY season;

-- Q4. Which franchises win most often?
WITH played AS (
    SELECT team1_id AS team_id, winner_id FROM matches WHERE winner_id IS NOT NULL
    UNION ALL
    SELECT team2_id, winner_id FROM matches WHERE winner_id IS NOT NULL
)
SELECT  t.team_name,
        COUNT(*)                                        AS played,
        SUM(p.winner_id = p.team_id)                    AS won,
        ROUND(100.0 * SUM(p.winner_id = p.team_id) / COUNT(*), 1) AS win_pct
FROM    played p
JOIN    teams t ON t.team_id = p.team_id
GROUP BY t.team_id
HAVING  COUNT(*) >= 50
ORDER BY win_pct DESC;

-- Q5. Who won each season? (winner of the final)
SELECT  m.season,
        w.team_name                                     AS champion,
        CASE WHEN m.winner_id = m.team1_id THEN t2.team_name ELSE t1.team_name END AS runner_up,
        v.venue_name                                    AS final_venue
FROM    matches m
JOIN    teams  w  ON w.team_id  = m.winner_id
JOIN    teams  t1 ON t1.team_id = m.team1_id
JOIN    teams  t2 ON t2.team_id = m.team2_id
JOIN    venues v  ON v.venue_id = m.venue_id
WHERE   m.match_type = 'Final'
ORDER BY m.season;

-- Q6. Top 10 run scorers of all time
SELECT  batter,
        SUM(batter_runs)                                AS runs,
        SUM(faced)                                      AS balls,
        ROUND(100.0 * SUM(batter_runs) / SUM(faced), 1) AS strike_rate,
        SUM(batter_runs = 6)                            AS sixes
FROM    v_balls
GROUP BY batter_id
ORDER BY runs DESC
LIMIT 10;

-- Q7. Orange Cap: top run scorer in every season (window function)
WITH season_runs AS (
    SELECT  season, batter, SUM(batter_runs) AS runs,
            ROW_NUMBER() OVER (PARTITION BY season ORDER BY SUM(batter_runs) DESC) AS rn
    FROM    v_balls
    GROUP BY season, batter_id
)
SELECT season, batter, runs
FROM   season_runs
WHERE  rn = 1
ORDER BY season;

-- Q8. Top 10 wicket takers of all time
SELECT  bowler,
        SUM(bowler_wicket)                              AS wickets,
        SUM(legal) / 6                                  AS overs,
        ROUND(6.0 * SUM(bowler_runs) / SUM(legal), 2)   AS economy
FROM    v_balls
GROUP BY bowler_id
ORDER BY wickets DESC
LIMIT 10;

-- Q9. Best death-over bowlers (overs 16-20, minimum 500 balls)
SELECT  bowler,
        SUM(legal)                                      AS balls,
        ROUND(6.0 * SUM(bowler_runs) / SUM(legal), 2)   AS death_economy,
        SUM(bowler_wicket)                              AS death_wickets
FROM    v_balls
WHERE   phase = 'Death (16-20)'
GROUP BY bowler_id
HAVING  SUM(legal) >= 500
ORDER BY death_economy
LIMIT 10;

-- Q10. Is the IPL getting more aggressive? Average first-innings score and sixes per match
WITH inns AS (
    SELECT  match_id, season, inning, SUM(total_runs) AS runs, SUM(batter_runs = 6) AS sixes
    FROM    v_balls
    GROUP BY match_id, inning
)
SELECT  season,
        ROUND(AVG(CASE WHEN inning = 1 THEN runs END), 1)       AS avg_first_innings_score,
        ROUND(1.0 * SUM(sixes) / COUNT(DISTINCT match_id), 1)   AS sixes_per_match
FROM    inns
GROUP BY season
ORDER BY season;

-- Q11. Run rate by phase of the innings, early seasons vs recent seasons
SELECT  phase,
        ROUND(6.0 * SUM(CASE WHEN season <= 2012 THEN total_runs END)
                  / SUM(CASE WHEN season <= 2012 THEN legal END), 1)  AS run_rate_2008_2012,
        ROUND(6.0 * SUM(CASE WHEN season >= 2023 THEN total_runs END)
                  / SUM(CASE WHEN season >= 2023 THEN legal END), 1)  AS run_rate_2023_onwards
FROM    v_balls
GROUP BY phase
ORDER BY MIN(over_no);

-- Q12. Most Player of the Match awards
SELECT  player_of_match,
        COUNT(*)                                        AS awards
FROM    matches
WHERE   player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;

-- Q13. Highest team totals ever
SELECT  b.season,
        b.batting_team,
        b.bowling_team                                  AS against,
        SUM(b.total_runs)                               AS total,
        v.venue_name
FROM    v_balls b
JOIN    matches m ON m.match_id = b.match_id
JOIN    venues  v ON v.venue_id = m.venue_id
GROUP BY b.match_id, b.inning
ORDER BY total DESC
LIMIT 10;

-- Q14. Venues where chasing is easiest (minimum 30 matches)
SELECT  v.venue_name,
        v.city,
        COUNT(*)                                        AS matches,
        ROUND(100.0 * AVG(CASE WHEN (m.toss_decision = 'field' AND m.winner_id = m.toss_winner_id)
                                 OR (m.toss_decision = 'bat'   AND m.winner_id <> m.toss_winner_id)
                               THEN 1.0 ELSE 0 END), 1) AS chasing_win_pct
FROM    matches m
JOIN    venues v ON v.venue_id = m.venue_id
WHERE   m.winner_id IS NOT NULL AND m.result <> 'tie'
GROUP BY v.venue_id
HAVING  COUNT(*) >= 30
ORDER BY chasing_win_pct DESC;
