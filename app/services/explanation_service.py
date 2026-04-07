class ExplanationService:
    def build_prediction_explanation(
        self,
        predicted_result: str,
        probabilities: dict
    ) -> str:
        home_prob = round(probabilities.get("HOME_TEAM", 0.0) * 100, 2)
        draw_prob = round(probabilities.get("DRAW", 0.0) * 100, 2)
        away_prob = round(probabilities.get("AWAY_TEAM", 0.0) * 100, 2)

        if predicted_result == "HOME_TEAM":
            return (
                f"El modelo favorece al equipo local con una probabilidad de "
                f"{home_prob}%. El empate tiene {draw_prob}% y la victoria "
                f"del visitante {away_prob}%."
            )

        if predicted_result == "AWAY_TEAM":
            return (
                f"El modelo favorece al equipo visitante con una probabilidad de "
                f"{away_prob}%. El empate tiene {draw_prob}% y la victoria "
                f"del local {home_prob}%."
            )

        if predicted_result == "DRAW":
            return (
                f"El modelo considera más probable el empate con un {draw_prob}%. "
                f"La victoria local tiene {home_prob}% y la victoria visitante "
                f"{away_prob}%."
            )

        return "No fue posible generar una explicación para esta predicción."