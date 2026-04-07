from app.db.database import get_connection


class PredictionRepository:
    def save_prediction(
        self,
        match_id: int,
        predicted_winner: str,
        home_win_prob: float,
        draw_prob: float,
        away_win_prob: float,
        explanation: str
    ) -> None:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO predictions (
                match_id,
                predicted_winner,
                home_win_prob,
                draw_prob,
                away_win_prob,
                explanation
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            match_id,
            predicted_winner,
            home_win_prob,
            draw_prob,
            away_win_prob,
            explanation,
        ))

        connection.commit()
        connection.close()