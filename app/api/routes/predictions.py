from fastapi import APIRouter, HTTPException

from app.services.feature_service import FeatureService
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/predict-match")
def predict_match(match: dict):
    """Genera una prediccion para un partido enviado directamente.
    
    Este endpoint permite predecir partidos futuros que vienen de la API
    sin necesidad de que esten guardados en la base de datos.
    
    Args:
        match: Datos del partido con formato de la API football-data.org.
        
    Returns:
        dict: Prediccion con probabilidades y explicacion.
    """
    try:
        feature_service = FeatureService()
        prediction_service = PredictionService()

        features = feature_service.get_pre_match_features_from_api_match(match)
        match_id = features.pop("match_id")

        return prediction_service.predict(
            match_id=match_id,
            features=features
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail="El modelo no ha sido entrenado. Entrena el modelo primero con /matches/train"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
