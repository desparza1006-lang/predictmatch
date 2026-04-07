from app.db.database import get_connection


def create_tables() -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            type TEXT,
            emblem TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            competition_code TEXT NOT NULL,
            utc_date TEXT NOT NULL,
            status TEXT,
            matchday INTEGER,
            home_team_id INTEGER,
            home_team_name TEXT,
            away_team_id INTEGER,
            away_team_name TEXT,
            winner TEXT,
            full_time_home INTEGER,
            full_time_away INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            predicted_winner TEXT,
            home_win_prob REAL,
            draw_prob REAL,
            away_win_prob REAL,
            explanation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    _create_indexes(cursor)

    connection.commit()
    connection.close()


def _create_indexes(cursor) -> None:
    """Crea indices para consultas frecuentes."""
    indices = [
        ("idx_matches_competition", "matches", "competition_code"),
        ("idx_matches_date", "matches", "utc_date"),
        ("idx_matches_competition_date", "matches", "competition_code, utc_date"),
        ("idx_matches_winner", "matches", "winner"),
        ("idx_matches_home_team", "matches", "home_team_id"),
        ("idx_matches_away_team", "matches", "away_team_id"),
        ("idx_predictions_match_id", "predictions", "match_id"),
    ]

    for index_name, table, columns in indices:
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS {index_name} ON {table}({columns})
        """)