"""Draw the key findings as PNG charts (run after load_data.py).

Usage:  python make_charts.py
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
con = sqlite3.connect(HERE / "ipl.db")
q = lambda s: pd.read_sql_query(s, con)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.bbox": "tight"})
BLUE, ORANGE, GREY, INK = "#1F4E8C", "#E8833A", "#B8B8B8", "#333333"

# 1. Does the toss matter?
t = q("""SELECT ROUND(100.0 * SUM(toss_winner_id = winner_id) / COUNT(*), 1) AS pct
         FROM matches WHERE winner_id IS NOT NULL""").pct[0]
d = q("""SELECT toss_decision, ROUND(100.0 * SUM(toss_winner_id = winner_id) / COUNT(*), 1) AS pct
         FROM matches WHERE winner_id IS NOT NULL GROUP BY toss_decision""").set_index("toss_decision").pct
labels = ["Won the toss\n(any choice)", "Won toss,\nchose to bat", "Won toss,\nchose to field"]
vals = [t, d.get("bat", 0), d.get("field", 0)]
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(labels, vals, color=[BLUE, GREY, ORANGE], width=0.55)
ax.axhline(50, color=INK, ls="--", lw=1)
ax.text(1, 51.2, "coin flip (50%)", ha="center", fontsize=9, color=INK)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v:.1f}%", ha="center", fontweight="bold")
ax.set_ylim(0, max(vals) + 10)
ax.set_ylabel("Matches won by the toss winner (%)")
ax.set_title("Winning the toss barely matters", fontweight="bold")
fig.savefig(HERE / "chart_1_toss.png"); plt.close(fig)

# 2. Scores and sixes by season
s = q("""WITH inns AS (SELECT match_id, season, inning, SUM(total_runs) runs, SUM(batter_runs = 6) sixes
                       FROM v_balls GROUP BY match_id, inning)
         SELECT season, AVG(CASE WHEN inning = 1 THEN runs END) avg_score,
                1.0 * SUM(sixes) / COUNT(DISTINCT match_id) sixes
         FROM inns GROUP BY season ORDER BY season""")
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(s.season, s.avg_score, marker="o", color=BLUE, lw=2.2, label="Average first-innings score")
ax.set_ylabel("Runs", color=BLUE)
ax2 = ax.twinx()
ax2.bar(s.season, s.sixes, color=ORANGE, alpha=0.35, label="Sixes per match")
ax2.set_ylabel("Sixes per match", color=ORANGE)
ax2.spines["top"].set_visible(False)
ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
ax.set_xticks(s.season); ax.set_xticklabels(s.season, rotation=45)
last = s.iloc[-1]
ax.annotate(f"{last.avg_score:.0f}", (last.season, last.avg_score), xytext=(0, 8),
            textcoords="offset points", ha="center", fontweight="bold", color=BLUE)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")
ax.set_title("The IPL keeps getting more aggressive", fontweight="bold")
fig.savefig(HERE / "chart_2_scores_by_season.png"); plt.close(fig)

# 3. Run rate by phase: early vs recent seasons
p = q("""SELECT phase,
                6.0 * SUM(CASE WHEN season <= 2012 THEN total_runs END) / SUM(CASE WHEN season <= 2012 THEN legal END) AS early,
                6.0 * SUM(CASE WHEN season >= 2023 THEN total_runs END) / SUM(CASE WHEN season >= 2023 THEN legal END) AS recent
         FROM v_balls GROUP BY phase ORDER BY MIN(over_no)""")
fig, ax = plt.subplots(figsize=(8, 4.5))
x = range(len(p))
b1 = ax.bar([i - 0.2 for i in x], p.early, 0.4, color=GREY, label="2008-2012")
b2 = ax.bar([i + 0.2 for i in x], p.recent, 0.4, color=BLUE, label="2023 onwards")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.1, f"{b.get_height():.1f}", ha="center", fontsize=10)
ax.set_xticks(list(x)); ax.set_xticklabels(p.phase)
ax.set_ylabel("Runs per over")
ax.set_ylim(0, p.recent.max() * 1.25)
ax.legend(frameon=False, loc="upper left")
ax.set_title("Teams now score faster in every phase", fontweight="bold")
fig.savefig(HERE / "chart_3_phase_run_rate.png"); plt.close(fig)

# 4. Top 10 run scorers
r = q("""SELECT batter, SUM(batter_runs) runs, 100.0 * SUM(batter_runs) / SUM(faced) sr
         FROM v_balls GROUP BY batter_id ORDER BY runs DESC LIMIT 10""").iloc[::-1]
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(r.batter, r.runs, color=BLUE)
for b, sr in zip(bars, r.sr):
    ax.text(b.get_width() + 60, b.get_y() + b.get_height() / 2, f"SR {sr:.0f}", va="center", fontsize=9)
ax.set_xlim(0, r.runs.max() * 1.15)
ax.set_xlabel("Career IPL runs")
ax.set_title("Top 10 run scorers (with strike rate)", fontweight="bold")
fig.savefig(HERE / "chart_4_top_batters.png"); plt.close(fig)

# 5. Franchise win %
w = q("""WITH played AS (SELECT team1_id team_id, winner_id FROM matches WHERE winner_id IS NOT NULL
                         UNION ALL SELECT team2_id, winner_id FROM matches WHERE winner_id IS NOT NULL)
         SELECT t.team_name, 100.0 * SUM(p.winner_id = p.team_id) / COUNT(*) win_pct, COUNT(*) n
         FROM played p JOIN teams t ON t.team_id = p.team_id
         GROUP BY t.team_id HAVING COUNT(*) >= 50 ORDER BY win_pct""")
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(w.team_name, w.win_pct, color=[ORANGE if v >= 50 else GREY for v in w.win_pct])
ax.axvline(50, color=INK, ls="--", lw=1)
for b, v in zip(bars, w.win_pct):
    ax.text(v + 0.5, b.get_y() + b.get_height() / 2, f"{v:.1f}%", va="center", fontsize=9)
ax.set_xlim(0, w.win_pct.max() + 8)
ax.set_xlabel("Win % (franchises with 50+ matches)")
ax.set_title("Which franchises win most often", fontweight="bold")
fig.savefig(HERE / "chart_5_team_win_pct.png"); plt.close(fig)

print("charts written")
