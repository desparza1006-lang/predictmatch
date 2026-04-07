from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from app.services.feature_service import FeatureService


MODEL_DIR = Path("app/data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "match_result_model.pkl"


def train_match_result_model() -> dict:
    feature_service = FeatureService()
    feature_data = feature_service.get_training_features()

    preview = feature_data.get("preview", [])
    if not preview:
        raise ValueError("No hay datos suficientes para entrenar el modelo.")

    df = pd.DataFrame(preview)

    feature_columns = [
        "matchday",
        "home_team_id",
        "away_team_id",
        "home_avg_goals_for",
        "home_avg_goals_against",
        "away_avg_goals_for",
        "away_avg_goals_against",
        "home_recent_points",
        "away_recent_points",
    ]

    X = df[feature_columns].fillna(0)
    y = df["result_label"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return {
        "message": "Modelo prepartido mejorado entrenado correctamente",
        "model_path": str(MODEL_PATH),
        "training_rows": len(df),
        "features": feature_columns,
        "classes": list(model.classes_)
    }