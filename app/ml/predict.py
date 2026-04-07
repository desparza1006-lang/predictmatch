import joblib
import pandas as pd

from app.ml.model_registry import MODEL_PATH


def predict_match_result(features: dict) -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("El modelo aún no ha sido entrenado.")

    model = joblib.load(MODEL_PATH)

    df = pd.DataFrame([features])
    probabilities = model.predict_proba(df)[0]
    predicted_class = model.predict(df)[0]

    class_probabilities = {
        model.classes_[index]: float(probabilities[index])
        for index in range(len(model.classes_))
    }

    return {
        "predicted_result": predicted_class,
        "probabilities": class_probabilities
    }