import requests

from app.config.settings import settings


class FootballDataClient:
    def __init__(self) -> None:
        self.base_url = settings.FOOTBALL_DATA_BASE_URL
        self.api_key = settings.FOOTBALL_DATA_API_KEY
        self.headers = {
            "X-Auth-Token": self.api_key
        }

    def get_competitions(self) -> dict:
        url = f"{self.base_url}/competitions"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_matches(
        self,
        competition_code: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None
    ) -> dict:
        if competition_code:
            url = f"{self.base_url}/competitions/{competition_code}/matches"
        else:
            url = f"{self.base_url}/matches"

        params = {}

        if date_from:
            params["dateFrom"] = date_from

        if date_to:
            params["dateTo"] = date_to

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()