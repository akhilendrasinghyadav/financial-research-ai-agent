import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "watchlist.db"


def init_watchlist_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
                symbol TEXT PRIMARY KEY,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_watchlist_symbol(symbol):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO watchlist (symbol) VALUES (?)",
            (symbol,),
        )


def remove_watchlist_symbol(symbol):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM watchlist WHERE symbol = ?",
            (symbol,),
        )


def get_watchlist_symbols():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT symbol FROM watchlist ORDER BY added_at DESC"
        ).fetchall()

    return [row[0] for row in rows]