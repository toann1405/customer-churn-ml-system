

import argparse
import logging
from pathlib import Path

import pandas as pd
import sqlite3


def _ensure_dir(path: Path) -> None:
    """Ensure the parent directory exists for a given path."""
    path.parent.mkdir(parents=True, exist_ok=True)


def setup_database(
    db_path: Path, csv_path: Path, sql_script_path: Path, table_name: str = "raw_customer_churn"
) -> None:
    """Load raw CSV into SQLite and execute transformation SQL script."""

    logging.info("Using database: %s", db_path)
    logging.info("Loading raw CSV: %s", csv_path)
    logging.info("Applying SQL script: %s", sql_script_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Raw CSV not found: {csv_path}")
    if not sql_script_path.exists():
        raise FileNotFoundError(f"SQL script not found: {sql_script_path}")

    _ensure_dir(db_path)

    conn = sqlite3.connect(str(db_path))
    try:
        raw_df = pd.read_csv(csv_path)
        raw_df.to_sql(table_name, conn, if_exists="replace", index=False)

        with sql_script_path.open("r", encoding="utf-8") as f:
            sql_query = f.read()

        conn.executescript(sql_query)
        conn.commit()

        logging.info("Database setup complete. Raw table: %s", table_name)
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load raw data into SQLite and run a transformation SQL script."
    )

    parser.add_argument(
        "--db",
        dest="db_path",
        default="data/database/telco_customer_churn.db",
        help="Path to SQLite database file (will be created if missing).",
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default="data/raw/telco_customer_churn.csv",
        help="Path to raw CSV file to ingest.",
    )
    parser.add_argument(
        "--sql",
        dest="sql_script_path",
        default="sql_scripts/transform_data.sql",
        help="Path to SQL script to execute against the database.",
    )
    parser.add_argument(
        "--table",
        dest="table_name",
        default="raw_customer_churn",
        help="Table name to write raw CSV data into (raw data).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    setup_database(
        db_path=Path(args.db_path),
        csv_path=Path(args.csv_path),
        sql_script_path=Path(args.sql_script_path),
        table_name=args.table_name,
    )


if __name__ == "__main__":
    main()
