import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "cloud_costs.sqlite"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init():
    with get_conn() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT,
            service TEXT,
            region TEXT,
            month TEXT,
            cost REAL
        )
        """)

def insert_cost(provider, service, region, month, cost):
    with get_conn() as con:
        con.execute("INSERT INTO costs(provider,service,region,month,cost) VALUES(?,?,?,?,?)",
                    (provider, service, region, month, cost))
