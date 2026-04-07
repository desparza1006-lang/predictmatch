import pandas as pd


def create_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    df["goal_difference"] = df["full_time_home"] - df["full_time_away"]
    df["total_goals"] = df["full_time_home"] + df["full_time_away"]

    df["home_win"] = (df["winner"] == "HOME_TEAM").astype(int)
    df["away_win"] = (df["winner"] == "AWAY_TEAM").astype(int)
    df["draw"] = (df["winner"] == "DRAW").astype(int)

    df["result_label"] = df["winner"].fillna("UNKNOWN")

    return df