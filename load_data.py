"""Load the Meta Social Connectedness Index CSVs into DuckDB.

By default this loads into the shared MotherDuck database. It needs a
MotherDuck access token in the `motherduck_token` environment variable.

    python load_data.py            # load into MotherDuck (md:meta_datamining)
    python load_data.py --local    # load into data/meta.duckdb instead
    python load_data.py --tables sci_gadm1   # load only some tables
"""

import argparse
import os
import sys
from pathlib import Path

import duckdb

DATA_DIR = Path(__file__).parent / "data"
MOTHERDUCK_DB = "meta_datamining"
LOCAL_DB = DATA_DIR / "meta.duckdb"

# table name -> CSV file in data/
TABLES = {
    "sci_gadm1": "gadm1.csv",
    "sci_nuts1": "nuts1_2024.csv",
}

SCI_COLUMNS = {
    "user_country": "VARCHAR",
    "friend_country": "VARCHAR",
    "user_region": "VARCHAR",
    "friend_region": "VARCHAR",
    "scaled_sci": "BIGINT",
}


def connect(local: bool) -> duckdb.DuckDBPyConnection:
    if local:
        LOCAL_DB.parent.mkdir(exist_ok=True)
        print(f"Connecting to local database {LOCAL_DB}")
        return duckdb.connect(str(LOCAL_DB))

    if not os.environ.get("motherduck_token"):
        sys.exit(
            "motherduck_token is not set. Create a token at "
            "https://app.motherduck.com (Settings -> Access Tokens) and set it "
            "as an environment variable, or run with --local."
        )
    print(f"Connecting to MotherDuck database md:{MOTHERDUCK_DB}")
    con = duckdb.connect("md:")
    con.execute(f"CREATE DATABASE IF NOT EXISTS {MOTHERDUCK_DB}")
    con.execute(f"USE {MOTHERDUCK_DB}")
    return con


def load_table(con: duckdb.DuckDBPyConnection, table: str, csv_name: str) -> None:
    csv_path = DATA_DIR / csv_name
    if not csv_path.exists():
        print(f"  skipping {table}: {csv_path} not found")
        return

    print(f"  loading {csv_name} -> {table} ...")
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {table} AS
        SELECT * FROM read_csv(?, header = true, columns = ?)
        """,
        [csv_path.as_posix(), SCI_COLUMNS],
    )
    rows = con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {rows:,} rows")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local", action="store_true", help="load into data/meta.duckdb instead of MotherDuck")
    parser.add_argument("--tables", nargs="+", choices=TABLES, default=list(TABLES), help="tables to load")
    args = parser.parse_args()

    con = connect(args.local)
    for table in args.tables:
        load_table(con, table, TABLES[table])
    con.close()
    print("Done.")


if __name__ == "__main__":
    main()
