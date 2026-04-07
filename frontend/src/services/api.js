const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchCompetitions() {
  const response = await fetch(`${API_BASE_URL}/competitions/`);

  if (!response.ok) {
    throw new Error("No se pudieron cargar las competiciones.");
  }

  return response.json();
}

export async function fetchMatchesByCompetition(
  competitionCode,
  dateFrom = "",
  dateTo = ""
) {
  const params = new URLSearchParams();

  if (competitionCode) {
    params.append("competition_code", competitionCode);
  }

  if (dateFrom) {
    params.append("date_from", dateFrom);
  }

  if (dateTo) {
    params.append("date_to", dateTo);
  }

  const response = await fetch(
    `${API_BASE_URL}/matches/?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("No se pudieron cargar los partidos.");
  }

  return response.json();
}

export async function predictMatch(match) {
  const response = await fetch(
    `${API_BASE_URL}/predictions/predict-match`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(match),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "No se pudo generar la prediccion.");
  }

  return response.json();
}