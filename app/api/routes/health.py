from fastapi import APIRouter

from app.db.database import get_connection

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    return {"status": "ok"}


@router.get("/db")
def db_check():
    connection = get_connection()
    cursor = connection.cursor()

    competitions_count = cursor.execute(
        "SELECT COUNT(*) FROM competitions"
    ).fetchone()[0]

    matches_count = cursor.execute(
        "SELECT COUNT(*) FROM matches"
    ).fetchone()[0]

    predictions_count = cursor.execute(
        "SELECT COUNT(*) FROM predictions"
    ).fetchone()[0]

    connection.close()

    return {
        "status": "ok",
        "database": "connected",
        "competitions_count": competitions_count,
        "matches_count": matches_count,
        "predictions_count": predictions_count
    }