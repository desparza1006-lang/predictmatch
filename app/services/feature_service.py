from app.db.database import get_connection
from app.ml.feature_engineering import create_basic_features
from app.ml.preprocessing import clean_matches_dataframe, load_matches_dataframe


class FeatureService:
    """Servicio para generar features de partidos.
    
    Soporta dos modos:
    1. Partidos guardados en BD (con o sin resultado): extrae datos de la BD.
    2. Partidos nuevos/futuros: recibe datos directamente sin necesidad de BD.
    """
    def get_training_features(self) -> dict:
        connection = get_connection()
        cursor = connection.cursor()

        rows = cursor.execute("""
            SELECT
                id,
                competition_code,
                utc_date,
                status,
                matchday,
                home_team_id,
                home_team_name,
                away_team_id,
                away_team_name,
                winner,
                full_time_home,
                full_time_away
            FROM matches
            WHERE full_time_home IS NOT NULL
              AND full_time_away IS NOT NULL
              AND winner IS NOT NULL
            ORDER BY utc_date ASC
        """).fetchall()

        connection.close()

        matches = [dict(row) for row in rows]

        df = load_matches_dataframe(matches)
        df = clean_matches_dataframe(df)
        df = create_basic_features(df)

        if df.empty:
            return {
                "count": 0,
                "columns": [],
                "preview": []
            }

        enriched_rows = []

        for _, row in df.iterrows():
            home_team_id = row["home_team_id"]
            away_team_id = row["away_team_id"]
            current_date = row["utc_date"]

            previous_matches = df[df["utc_date"] < current_date]

            home_previous = previous_matches[
                (previous_matches["home_team_id"] == home_team_id) |
                (previous_matches["away_team_id"] == home_team_id)
            ].tail(5)

            away_previous = previous_matches[
                (previous_matches["home_team_id"] == away_team_id) |
                (previous_matches["away_team_id"] == away_team_id)
            ].tail(5)

            home_avg_goals_for = self._avg_goals_for(home_previous, home_team_id)
            home_avg_goals_against = self._avg_goals_against(home_previous, home_team_id)
            away_avg_goals_for = self._avg_goals_for(away_previous, away_team_id)
            away_avg_goals_against = self._avg_goals_against(away_previous, away_team_id)

            home_recent_points = self._recent_points(home_previous, home_team_id)
            away_recent_points = self._recent_points(away_previous, away_team_id)

            enriched_row = row.to_dict()
            enriched_row["home_avg_goals_for"] = home_avg_goals_for
            enriched_row["home_avg_goals_against"] = home_avg_goals_against
            enriched_row["away_avg_goals_for"] = away_avg_goals_for
            enriched_row["away_avg_goals_against"] = away_avg_goals_against
            enriched_row["home_recent_points"] = home_recent_points
            enriched_row["away_recent_points"] = away_recent_points

            enriched_rows.append(enriched_row)

        enriched_df = load_matches_dataframe(enriched_rows)

        return {
            "count": len(enriched_df),
            "columns": list(enriched_df.columns),
            "preview": enriched_df.head(10).to_dict(orient="records")
        }

    def get_pre_match_features(self, match_id: int) -> dict:
        connection = get_connection()
        cursor = connection.cursor()

        row = cursor.execute("""
            SELECT
                id,
                competition_code,
                utc_date,
                status,
                matchday,
                home_team_id,
                home_team_name,
                away_team_id,
                away_team_name,
                winner,
                full_time_home,
                full_time_away
            FROM matches
            WHERE id = ?
        """, (match_id,)).fetchone()

        if not row:
            connection.close()
            raise ValueError("No se encontró el partido.")

        all_rows = cursor.execute("""
            SELECT
                id,
                competition_code,
                utc_date,
                status,
                matchday,
                home_team_id,
                home_team_name,
                away_team_id,
                away_team_name,
                winner,
                full_time_home,
                full_time_away
            FROM matches
            WHERE competition_code = ?
              AND winner IS NOT NULL
              AND full_time_home IS NOT NULL
              AND full_time_away IS NOT NULL
            ORDER BY utc_date ASC
        """, (row["competition_code"],)).fetchall()

        connection.close()

        current_match = dict(row)
        matches = [dict(item) for item in all_rows]

        df = load_matches_dataframe(matches)
        df = clean_matches_dataframe(df)
        df = create_basic_features(df)

        current_date = current_match["utc_date"]
        home_team_id = current_match["home_team_id"]
        away_team_id = current_match["away_team_id"]

        current_date = clean_matches_dataframe(
            load_matches_dataframe([{"utc_date": current_date}])
        )["utc_date"].iloc[0]

        previous_matches = df[df["utc_date"] < current_date]

        home_previous = previous_matches[
            (previous_matches["home_team_id"] == home_team_id) |
            (previous_matches["away_team_id"] == home_team_id)
        ].tail(5)

        away_previous = previous_matches[
            (previous_matches["home_team_id"] == away_team_id) |
            (previous_matches["away_team_id"] == away_team_id)
        ].tail(5)

        return {
            "match_id": current_match["id"],
            "matchday": current_match["matchday"],
            "home_team_id": current_match["home_team_id"],
            "away_team_id": current_match["away_team_id"],
            "home_avg_goals_for": self._avg_goals_for(home_previous, home_team_id),
            "home_avg_goals_against": self._avg_goals_against(home_previous, home_team_id),
            "away_avg_goals_for": self._avg_goals_for(away_previous, away_team_id),
            "away_avg_goals_against": self._avg_goals_against(away_previous, away_team_id),
            "home_recent_points": self._recent_points(home_previous, home_team_id),
            "away_recent_points": self._recent_points(away_previous, away_team_id),
        }

    def _avg_goals_for(self, team_matches, team_id: int) -> float:
        if team_matches.empty:
            return 0.0

        goals = []

        for _, match in team_matches.iterrows():
            if match["home_team_id"] == team_id:
                goals.append(match["full_time_home"])
            elif match["away_team_id"] == team_id:
                goals.append(match["full_time_away"])

        return round(sum(goals) / len(goals), 2) if goals else 0.0

    def _avg_goals_against(self, team_matches, team_id: int) -> float:
        if team_matches.empty:
            return 0.0

        goals = []

        for _, match in team_matches.iterrows():
            if match["home_team_id"] == team_id:
                goals.append(match["full_time_away"])
            elif match["away_team_id"] == team_id:
                goals.append(match["full_time_home"])

        return round(sum(goals) / len(goals), 2) if goals else 0.0

    def _recent_points(self, team_matches, team_id: int) -> int:
        if team_matches.empty:
            return 0

        points = 0

        for _, match in team_matches.iterrows():
            if match["winner"] == "DRAW":
                points += 1
            elif match["winner"] == "HOME_TEAM" and match["home_team_id"] == team_id:
                points += 3
            elif match["winner"] == "AWAY_TEAM" and match["away_team_id"] == team_id:
                points += 3

        return points

    def get_pre_match_features_from_api_match(self, match: dict) -> dict:
        """Genera features para un partido que viene directamente de la API.
        
        Esto permite predecir partidos futuros que aún no están en la BD
        o que no tienen resultados todavía.
        
        Args:
            match: Diccionario con datos del partido desde la API.
            
        Returns:
            dict: Features listas para el modelo de predicción.
        """
        connection = get_connection()
        cursor = connection.cursor()

        competition_code = match.get("competition", {}).get("code")
        home_team_id = match.get("homeTeam", {}).get("id")
        away_team_id = match.get("awayTeam", {}).get("id")
        match_date = match.get("utcDate")
        matchday = match.get("matchday", 1)
        match_id = match.get("id", 0)

        if not competition_code or not home_team_id or not away_team_id:
            connection.close()
            raise ValueError("Datos de partido incompletos para generar features.")

        all_rows = cursor.execute("""
            SELECT
                id,
                competition_code,
                utc_date,
                status,
                matchday,
                home_team_id,
                home_team_name,
                away_team_id,
                away_team_name,
                winner,
                full_time_home,
                full_time_away
            FROM matches
            WHERE competition_code = ?
              AND winner IS NOT NULL
              AND full_time_home IS NOT NULL
              AND full_time_away IS NOT NULL
            ORDER BY utc_date ASC
        """, (competition_code,)).fetchall()

        connection.close()

        matches = [dict(item) for item in all_rows]

        if not matches:
            return {
                "match_id": match_id,
                "matchday": matchday,
                "home_team_id": home_team_id,
                "away_team_id": away_team_id,
                "home_avg_goals_for": 0.0,
                "home_avg_goals_against": 0.0,
                "away_avg_goals_for": 0.0,
                "away_avg_goals_against": 0.0,
                "home_recent_points": 0,
                "away_recent_points": 0,
            }

        df = load_matches_dataframe(matches)
        df = clean_matches_dataframe(df)
        df = create_basic_features(df)

        current_date = clean_matches_dataframe(
            load_matches_dataframe([{"utc_date": match_date}])
        )["utc_date"].iloc[0]

        previous_matches = df[df["utc_date"] < current_date]

        home_previous = previous_matches[
            (previous_matches["home_team_id"] == home_team_id) |
            (previous_matches["away_team_id"] == home_team_id)
        ].tail(5)

        away_previous = previous_matches[
            (previous_matches["home_team_id"] == away_team_id) |
            (previous_matches["away_team_id"] == away_team_id)
        ].tail(5)

        return {
            "match_id": match_id,
            "matchday": matchday,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "home_avg_goals_for": self._avg_goals_for(home_previous, home_team_id),
            "home_avg_goals_against": self._avg_goals_against(home_previous, home_team_id),
            "away_avg_goals_for": self._avg_goals_for(away_previous, away_team_id),
            "away_avg_goals_against": self._avg_goals_against(away_previous, away_team_id),
            "home_recent_points": self._recent_points(home_previous, home_team_id),
            "away_recent_points": self._recent_points(away_previous, away_team_id),
        }