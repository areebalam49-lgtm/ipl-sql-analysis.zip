"""Run every query in queries.sql and save the results to query_results.md.

Usage:  python run_reports.py
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent


def main():
    con = sqlite3.connect(HERE / "ipl.db")
    blocks = re.split(r"\n(?=-- Q\d+\.)", (HERE / "queries.sql").read_text())[1:]
    lo, hi = con.execute("SELECT MIN(season), MAX(season) FROM matches").fetchone()
    out = ["# IPL Cricket Analysis: query results", "",
           f"Seasons {lo}-{hi}. Source: IPL Complete Dataset (Kaggle), ball-by-ball data.", ""]
    for b in blocks:
        title = b.splitlines()[0].lstrip("- ").strip()
        df = pd.read_sql_query(b, con)
        for c in df.columns:                      # show whole numbers without ".0"
            if df[c].dtype.kind == "f" and df[c].dropna().apply(float.is_integer).all():
                df[c] = df[c].astype("Int64")
        fmt = tuple(".0f" if df[c].dtype.kind in "iu" or str(df[c].dtype) == "Int64" else ".1f" for c in df.columns)
        out += [f"## {title}", "", df.to_markdown(index=False, floatfmt=fmt), ""]
        print(f"{title[:70]:70s} {len(df):>3} rows")
    (HERE / "query_results.md").write_text("\n".join(out))


if __name__ == "__main__":
    main()
