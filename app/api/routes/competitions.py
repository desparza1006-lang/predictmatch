from fastapi import APIRouter, HTTPException

from app.db.repositories.competition_repository import CompetitionRepository
from app.services.football_data_client import FootballDataClient

router = APIRouter(prefix="/competitions", tags=["Competitions"])


@router.get("/")
def get_competitions():
    try:
        client = FootballDataClient()
        data = client.get_competitions()

        competitions = data.get("competitions", [])

        repository = CompetitionRepository()
        repository.save_many(competitions)

        return {
            "count": len(competitions),
            "competitions": competitions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))