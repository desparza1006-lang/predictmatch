from app.db.database import get_connection


class MatchRepository:
    def save_many(self, matches: list[dict], competition_code: str) -> None:
        connection = get_connection()
        cursor = connection.cursor()

        for match in matches:
            cursor.execute("""
                INSERT OR REPLACE INTO matches (
                    id,
                    competition_code,
                    utc_date,
                    status,
                    matchday,
                    home_team_id,
                    home_team_name,
                    away_team_id,
                    away_team_name,
                    winner,
                    full_time_home,
                    full_time_away
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match.get("id"),
                competition_code,
                match.get("utcDate"),
                match.get("status"),
                match.get("matchday"),
                match.get("homeTeam", {}).get("id"),
                match.get("homeTeam", {}).get("name"),
                match.get("awayTeam", {}).get("id"),
                match.get("awayTeam", {}).get("name"),
                match.get("score", {}).get("winner"),
                match.get("score", {}).get("fullTime", {}).get("home"),
                match.get("score", {}).get("fullTime", {}).get("away"),
            ))

        connection.commit()
        connection.close()