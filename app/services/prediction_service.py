from app.db.database import get_connection
from app.db.repositories.prediction_repository import PredictionRepository
from app.ml.predict import predict_match_result
from app.ml.train_model import train_match_result_model
from app.services.explanation_service import ExplanationService


class PredictionService:
    def __init__(self) -> None:
        self.repository = PredictionRepository()
        self.explanation_service = ExplanationService()

    def train_model(self) -> dict:
        return train_match_result_model()

    def predict(self, match_id: int, features: dict) -> dict:
        result = predict_match_result(features)

        predicted_result = result.get("predicted_result")
        probabilities = result.get("probabilities", {})

        explanation = self.explanation_service.build_prediction_explanation(
            predicted_result=predicted_result,
            probabilities=probabilities
        )

        self.repository.save_prediction(
            match_id=match_id,
            predicted_winner=predicted_result,
            home_win_prob=probabilities.get("HOME_TEAM", 0.0),
            draw_prob=probabilities.get("DRAW", 0.0),
            away_win_prob=probabilities.get("AWAY_TEAM", 0.0),
            explanation=explanation
        )

        return {
            "match_id": match_id,
            "predicted_result": predicted_result,
            "probabilities": probabilities,
            "explanation": explanation
        }

    def get_prediction_history(self) -> dict:
        connection = get_connection()
        cursor = connection.cursor()

        rows = cursor.execute("""
            SELECT
                id,
                match_id,
                predicted_winner,
                home_win_prob,
                draw_prob,
                away_win_prob,
                explanation,
                created_at
            FROM predictions
            ORDER BY id DESC
        """).fetchall()

        connection.close()

        predictions = [dict(row) for row in rows]

        return {
            "count": len(predictions),
            "predictions": predictions
        }