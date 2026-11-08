# IPL Cricket Analysis: query results

Seasons 2008-2024. Source: IPL Complete Dataset (Kaggle), ball-by-ball data.

## Q1. Does winning the toss help you win the match?

|   matches |   toss_winner_won |   toss_win_pct |
|----------:|------------------:|---------------:|
|      1090 |               554 |           50.8 |

## Q2. After winning the toss, is it better to bat or to field?

| toss_decision   |   times_chosen |   win_pct_for_toss_winner |
|:----------------|---------------:|--------------------------:|
| bat             |            390 |                      45.4 |
| field           |            700 |                      53.9 |

## Q3. Batting first or chasing: which wins more, season by season?

|   season |   matches |   bat_first_win_pct |
|---------:|----------:|--------------------:|
|     2008 |        58 |                37.9 |
|     2009 |        56 |                46.4 |
|     2010 |        59 |                52.5 |
|     2011 |        72 |                44.4 |
|     2012 |        74 |                45.9 |
|     2013 |        74 |                50.0 |
|     2014 |        59 |                37.3 |
|     2015 |        56 |                57.1 |
|     2016 |        60 |                31.7 |
|     2017 |        58 |                44.8 |
|     2018 |        60 |                46.7 |
|     2019 |        57 |                38.6 |
|     2020 |        56 |                48.2 |
|     2021 |        59 |                37.3 |
|     2022 |        74 |                50.0 |
|     2023 |        73 |                54.8 |
|     2024 |        71 |                49.3 |

## Q4. Which franchises win most often?

| team_name                   |   played |   won |   win_pct |
|:----------------------------|---------:|------:|----------:|
| Chennai Super Kings         |      237 |   138 |      58.2 |
| Mumbai Indians              |      261 |   144 |      55.2 |
| Kolkata Knight Riders       |      251 |   131 |      52.2 |
| Rajasthan Royals            |      219 |   112 |      51.1 |
| Royal Challengers Bengaluru |      252 |   123 |      48.8 |
| Sunrisers Hyderabad         |      182 |    88 |      48.4 |
| Delhi Capitals              |      250 |   115 |      46.0 |
| Punjab Kings                |      246 |   112 |      45.5 |
| Deccan Chargers             |       75 |    29 |      38.7 |

## Q5. Who won each season? (winner of the final)

|   season | champion              | runner_up                   | final_venue                         |
|---------:|:----------------------|:----------------------------|:------------------------------------|
|     2008 | Rajasthan Royals      | Chennai Super Kings         | Dr DY Patil Sports Academy          |
|     2009 | Deccan Chargers       | Royal Challengers Bengaluru | New Wanderers Stadium               |
|     2010 | Chennai Super Kings   | Mumbai Indians              | Dr DY Patil Sports Academy          |
|     2011 | Chennai Super Kings   | Royal Challengers Bengaluru | MA Chidambaram Stadium              |
|     2012 | Kolkata Knight Riders | Chennai Super Kings         | MA Chidambaram Stadium              |
|     2013 | Mumbai Indians        | Chennai Super Kings         | Eden Gardens                        |
|     2014 | Kolkata Knight Riders | Punjab Kings                | M Chinnaswamy Stadium               |
|     2015 | Mumbai Indians        | Chennai Super Kings         | Eden Gardens                        |
|     2016 | Sunrisers Hyderabad   | Royal Challengers Bengaluru | M Chinnaswamy Stadium               |
|     2017 | Mumbai Indians        | Rising Pune Supergiant      | Rajiv Gandhi International Stadium  |
|     2018 | Chennai Super Kings   | Sunrisers Hyderabad         | Wankhede Stadium                    |
|     2019 | Mumbai Indians        | Chennai Super Kings         | Rajiv Gandhi International Stadium  |
|     2020 | Mumbai Indians        | Delhi Capitals              | Dubai International Cricket Stadium |
|     2021 | Chennai Super Kings   | Kolkata Knight Riders       | Dubai International Cricket Stadium |
|     2022 | Gujarat Titans        | Rajasthan Royals            | Narendra Modi Stadium               |
|     2023 | Chennai Super Kings   | Gujarat Titans              | Narendra Modi Stadium               |
|     2024 | Kolkata Knight Riders | Sunrisers Hyderabad         | MA Chidambaram Stadium              |

## Q6. Top 10 run scorers of all time

| batter         |   runs |   balls |   strike_rate |   sixes |
|:---------------|-------:|--------:|--------------:|--------:|
| V Kohli        |   8004 |    6065 |         132.0 |     273 |
| S Dhawan       |   6769 |    5324 |         127.1 |     153 |
| RG Sharma      |   6628 |    5054 |         131.1 |     281 |
| DA Warner      |   6565 |    4697 |         139.8 |     236 |
| SK Raina       |   5528 |    4043 |         136.7 |     203 |
| MS Dhoni       |   5243 |    3812 |         137.5 |     252 |
| AB de Villiers |   5162 |    3403 |         151.7 |     251 |
| CH Gayle       |   4965 |    3333 |         149.0 |     357 |
| RV Uthappa     |   4952 |    3799 |         130.4 |     182 |
| KD Karthik     |   4842 |    3577 |         135.4 |     161 |

## Q7. Orange Cap: top run scorer in every season (window function)

|   season | batter        |   runs |
|---------:|:--------------|-------:|
|     2008 | SE Marsh      |    616 |
|     2009 | ML Hayden     |    572 |
|     2010 | SR Tendulkar  |    618 |
|     2011 | CH Gayle      |    608 |
|     2012 | CH Gayle      |    733 |
|     2013 | MEK Hussey    |    733 |
|     2014 | RV Uthappa    |    660 |
|     2015 | DA Warner     |    562 |
|     2016 | V Kohli       |    973 |
|     2017 | DA Warner     |    641 |
|     2018 | KS Williamson |    735 |
|     2019 | DA Warner     |    692 |
|     2020 | KL Rahul      |    670 |
|     2021 | RD Gaikwad    |    635 |
|     2022 | JC Buttler    |    863 |
|     2023 | Shubman Gill  |    890 |
|     2024 | V Kohli       |    741 |

## Q8. Top 10 wicket takers of all time

| bowler     |   wickets |   overs |   economy |
|:-----------|----------:|--------:|----------:|
| YS Chahal  |       205 |     586 |       7.8 |
| PP Chawla  |       192 |     641 |       8.0 |
| DJ Bravo   |       183 |     520 |       8.4 |
| B Kumar    |       181 |     651 |       7.6 |
| R Ashwin   |       180 |     754 |       7.1 |
| SP Narine  |       180 |     679 |       6.7 |
| A Mishra   |       174 |     561 |       7.4 |
| SL Malinga |       170 |     471 |       7.1 |
| JJ Bumrah  |       165 |     508 |       7.3 |
| RA Jadeja  |       160 |     638 |       7.6 |

## Q9. Best death-over bowlers (overs 16-20, minimum 500 balls)

| bowler      |   balls |   death_economy |   death_wickets |
|:------------|--------:|----------------:|----------------:|
| SP Narine   |    1021 |             7.4 |              73 |
| SL Malinga  |    1117 |             7.9 |             108 |
| Rashid Khan |     516 |             8.1 |              39 |
| R Ashwin    |     595 |             8.1 |              36 |
| JJ Bumrah   |    1247 |             8.3 |              91 |
| DW Steyn    |     634 |             8.3 |              50 |
| CH Morris   |     646 |             8.7 |              58 |
| RA Jadeja   |     518 |             8.7 |              29 |
| A Nehra     |     527 |             8.9 |              54 |
| Z Khan      |     607 |             9.1 |              37 |

## Q10. Is the IPL getting more aggressive? Average first-innings score and sixes per match

|   season |   avg_first_innings_score |   sixes_per_match |
|---------:|--------------------------:|------------------:|
|     2008 |                     161.0 |              10.7 |
|     2009 |                     150.3 |               8.9 |
|     2010 |                     164.8 |               9.8 |
|     2011 |                     152.4 |               8.8 |
|     2012 |                     157.5 |               9.9 |
|     2013 |                     155.9 |               8.9 |
|     2014 |                     163.1 |              11.9 |
|     2015 |                     166.3 |              11.7 |
|     2016 |                     162.6 |              10.7 |
|     2017 |                     165.8 |              11.9 |
|     2018 |                     172.5 |              14.5 |
|     2019 |                     166.7 |              13.1 |
|     2020 |                     169.5 |              12.3 |
|     2021 |                     159.3 |              11.4 |
|     2022 |                     171.1 |              14.4 |
|     2023 |                     182.7 |              15.2 |
|     2024 |                     189.6 |              17.8 |

## Q11. Run rate by phase of the innings, early seasons vs recent seasons

| phase           |   run_rate_2008_2012 |   run_rate_2023_onwards |
|:----------------|---------------------:|------------------------:|
| Powerplay (1-6) |                  7.4 |                     9.1 |
| Middle (7-15)   |                  7.4 |                     8.6 |
| Death (16-20)   |                  9.4 |                    10.8 |

## Q12. Most Player of the Match awards

| player_of_match   |   awards |
|:------------------|---------:|
| AB de Villiers    |       25 |
| CH Gayle          |       22 |
| RG Sharma         |       19 |
| V Kohli           |       18 |
| DA Warner         |       18 |
| MS Dhoni          |       17 |
| YK Pathan         |       16 |
| SR Watson         |       16 |
| RA Jadeja         |       16 |
| SP Narine         |       15 |

## Q13. Highest team totals ever

|   season | batting_team                | against                     |   total | venue_name                                          |
|---------:|:----------------------------|:----------------------------|--------:|:----------------------------------------------------|
|     2024 | Sunrisers Hyderabad         | Royal Challengers Bengaluru |     287 | M Chinnaswamy Stadium                               |
|     2024 | Sunrisers Hyderabad         | Mumbai Indians              |     277 | Rajiv Gandhi International Stadium                  |
|     2024 | Kolkata Knight Riders       | Delhi Capitals              |     272 | Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium |
|     2024 | Sunrisers Hyderabad         | Delhi Capitals              |     266 | Arun Jaitley Stadium                                |
|     2013 | Royal Challengers Bengaluru | Pune Warriors               |     263 | M Chinnaswamy Stadium                               |
|     2024 | Royal Challengers Bengaluru | Sunrisers Hyderabad         |     262 | M Chinnaswamy Stadium                               |
|     2024 | Punjab Kings                | Kolkata Knight Riders       |     262 | Eden Gardens                                        |
|     2024 | Kolkata Knight Riders       | Punjab Kings                |     261 | Eden Gardens                                        |
|     2023 | Lucknow Super Giants        | Punjab Kings                |     257 | Punjab Cricket Association Stadium                  |
|     2024 | Delhi Capitals              | Mumbai Indians              |     257 | Arun Jaitley Stadium                                |

## Q14. Venues where chasing is easiest (minimum 30 matches)

| venue_name                              | city       |   matches |   chasing_win_pct |
|:----------------------------------------|:-----------|----------:|------------------:|
| Sawai Mansingh Stadium                  | Jaipur     |        57 |              64.9 |
| Sheikh Zayed Stadium                    | Abu Dhabi  |        35 |              60.0 |
| Eden Gardens                            | Kolkata    |        93 |              59.1 |
| Narendra Modi Stadium                   | Ahmedabad  |        35 |              57.1 |
| Punjab Cricket Association Stadium      | Chandigarh |        61 |              55.7 |
| Rajiv Gandhi International Stadium      | Hyderabad  |        76 |              55.3 |
| Wankhede Stadium                        | Mumbai     |       117 |              54.7 |
| M Chinnaswamy Stadium                   | Bangalore  |        90 |              54.4 |
| Dr DY Patil Sports Academy              | Mumbai     |        37 |              54.1 |
| Dubai International Cricket Stadium     | Dubai      |        43 |              51.2 |
| Arun Jaitley Stadium                    | Delhi      |        88 |              51.1 |
| Maharashtra Cricket Association Stadium | Pune       |        35 |              48.6 |
| MA Chidambaram Stadium                  | Chennai    |        83 |              43.4 |
