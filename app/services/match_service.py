from app.services.football_data_client import FootballDataClient


class MatchService:
    def __init__(self) -> None:
        self.client = FootballDataClient()

    def get_matches(
        self,
        competition_code: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None
    ) -> dict:
        data = self.client.get_matches(
            competition_code=competition_code,
            date_from=date_from,
            date_to=date_to
        )
        matches = data.get("matches", [])

        normalized_matches = []

        for match in matches:
            normalized_matches.append({
                "id": match.get("id"),
                "utcDate": match.get("utcDate"),
                "status": match.get("status"),
                "matchday": match.get("matchday"),
                "homeTeam": {
                    "id": match.get("homeTeam", {}).get("id"),
                    "name": match.get("homeTeam", {}).get("name"),
                    "shortName": match.get("homeTeam", {}).get("shortName"),
                    "tla": match.get("homeTeam", {}).get("tla"),
                    "crest": match.get("homeTeam", {}).get("crest"),
                },
                "awayTeam": {
                    "id": match.get("awayTeam", {}).get("id"),
                    "name": match.get("awayTeam", {}).get("name"),
                    "shortName": match.get("awayTeam", {}).get("shortName"),
                    "tla": match.get("awayTeam", {}).get("tla"),
                    "crest": match.get("awayTeam", {}).get("crest"),
                },
                "score": {
                    "winner": match.get("score", {}).get("winner"),
                    "fullTime": match.get("score", {}).get("fullTime"),
                    "halfTime": match.get("score", {}).get("halfTime"),
                },
                "competition": {
                    "id": match.get("competition", {}).get("id"),
                    "name": match.get("competition", {}).get("name"),
                    "code": match.get("competition", {}).get("code"),
                    "type": match.get("competition", {}).get("type"),
                    "emblem": match.get("competition", {}).get("emblem"),
                },
            })

        return {
            "count": len(normalized_matches),
            "matches": normalized_matches
        }