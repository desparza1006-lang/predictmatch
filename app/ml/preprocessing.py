import pandas as pd


def load_matches_dataframe(matches: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(matches)


def clean_matches_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    numeric_columns = [
        "matchday",
        "home_team_id",
        "away_team_id",
        "full_time_home",
        "full_time_away",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "utc_date" in df.columns:
        df["utc_date"] = pd.to_datetime(df["utc_date"], errors="coerce")

    return df