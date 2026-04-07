from app.db.database import get_connection


class CompetitionRepository:
    def save_many(self, competitions: list[dict]) -> None:
        connection = get_connection()
        cursor = connection.cursor()

        for competition in competitions:
            cursor.execute("""
                INSERT OR REPLACE INTO competitions (id, code, name, type, emblem)
                VALUES (?, ?, ?, ?, ?)
            """, (
                competition.get("id"),
                competition.get("code"),
                competition.get("name"),
                competition.get("type"),
                competition.get("emblem"),
            ))

        connection.commit()
        connection.close()