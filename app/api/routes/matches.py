from fastapi import APIRouter, HTTPException, Query

from app.db.repositories.match_repository import MatchRepository
from app.services.feature_service import FeatureService
from app.services.match_service import MatchService
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("/")
def get_matches(
    competition_code: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None)
):
    try:
        service = MatchService()
        result = service.get_matches(
            competition_code=competition_code,
            date_from=date_from,
            date_to=date_to
        )

        matches = result.get("matches", [])

        if competition_code and matches:
            repository = MatchRepository()
            repository.save_many(matches, competition_code)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pre-match-features/{match_id}")
def get_pre_match_features(match_id: int):
    try:
        service = FeatureService()
        return service.get_pre_match_features(match_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train")
def train_model():
    try:
        service = PredictionService()
        return service.train_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict-test/{match_id}")
def predict_test(match_id: int):
    try:
        feature_service = FeatureService()
        prediction_service = PredictionService()

        features = feature_service.get_pre_match_features(match_id)

        match_id_value = features.pop("match_id")

        return prediction_service.predict(
            match_id=match_id_value,
            features=features
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prediction-history")
def prediction_history():
    try:
        service = PredictionService()
        return service.get_prediction_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))