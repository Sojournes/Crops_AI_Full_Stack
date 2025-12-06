import sqlite3
import pandas as pd
import os
from typing import List, Tuple, Any

DB_FILE = "agriculture_optimization.db"
# Ascending from app/ to backend/ to root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FARMER_CSV = os.path.join(BASE_DIR, "farmer_advisor_dataset.csv")
MARKET_CSV = os.path.join(BASE_DIR, "market_researcher_dataset.csv")
DB_PATH = os.path.join(BASE_DIR, "backend", DB_FILE)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Creates SQLite tables and loads data from CSV files."""
    print(f"Initializing database at {DB_PATH}")
    if os.path.exists(DB_PATH):
        # Optional: Skip if already exists, or remove to refresh. 
        # For this project, let's refresh to ensure clean state on startup if needed, 
        # but to save time we can check if tables exist.
        # Let's overwrite for consistency with the prompt's logic.
        try:
            os.remove(DB_PATH)
            print("Removed existing database.")
        except Exception as e:
            print(f"Could not remove existing DB: {e}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Load Farmer Data
        if os.path.exists(FARMER_CSV):
            df = pd.read_csv(FARMER_CSV)
            df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)
            df.to_sql('farmer_profiles', conn, if_exists='replace', index=False)
            print("Loaded farmer_profiles")
        else:
            print(f"Warning: {FARMER_CSV} not found.")

        # Load Market Data
        if os.path.exists(MARKET_CSV):
            df = pd.read_csv(MARKET_CSV)
            df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)
            df.to_sql('market_data', conn, if_exists='replace', index=False)
            print("Loaded market_data")
        else:
            print(f"Warning: {MARKET_CSV} not found.")

        conn.commit()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()

# Tools (as requested in prompt)
def list_tables() -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall() if t[0] not in ('sqlite_sequence',)]
    conn.close()
    return tables

def describe_table(table_name: str) -> List[Tuple[str, str]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        return [(col[1], col[2]) for col in schema]
    except Exception as e:
        return [("Error", str(e))]
    finally:
        conn.close()

def execute_query(sql: str) -> List[List[str]]:
    if not sql.strip().upper().startswith("SELECT"):
        return [["Error: Only SELECT queries are allowed."]]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # Convert to list of lists of strings
        return [[str(item) for item in row] for row in results]
    except Exception as e:
        return [[f"Error: {e}"]]
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
