import { useEffect, useState } from "react";

import Header from "../components/layout/Header";
import HeroSection from "../components/home/HeroSection";
import FiltersSection from "../components/home/FiltersSection";
import MatchesSection from "../components/home/MatchesSection";
import AnalysisModal from "../components/home/AnalysisModal";
import {
  fetchCompetitions,
  fetchMatchesByCompetition,
  predictMatch,
} from "../services/api";

function HomePage() {
  const [competitions, setCompetitions] = useState([]);
  const [selectedLeague, setSelectedLeague] = useState("PD");
  const [selectedDate, setSelectedDate] = useState("");
  const [matches, setMatches] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoadingMatches, setIsLoadingMatches] = useState(false);
  const [isLoadingPrediction, setIsLoadingPrediction] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCompetitions();
  }, []);

  useEffect(() => {
    if (selectedLeague) {
      loadMatches(selectedLeague, selectedDate, selectedDate);
    }
  }, [selectedLeague, selectedDate]);

  async function loadCompetitions() {
    try {
      setError(null);
      const data = await fetchCompetitions();
      setCompetitions(data.competitions || []);
    } catch (err) {
      console.error(err);
      setError("No se pudieron cargar las competiciones.");
    }
  }

  async function loadMatches(competitionCode, dateFrom = "", dateTo = "") {
    try {
      setIsLoadingMatches(true);
      setError(null);
      const data = await fetchMatchesByCompetition(
        competitionCode,
        dateFrom,
        dateTo
      );
      setMatches(data.matches || []);
    } catch (err) {
      console.error(err);
      setError("No se pudieron cargar los partidos.");
      setMatches([]);
    } finally {
      setIsLoadingMatches(false);
    }
  }

  function handleLeagueChange(event) {
    setSelectedLeague(event.target.value);
  }

  function handleDateChange(event) {
    setSelectedDate(event.target.value);
  }

  function handleSearch() {
    if (!selectedLeague) {
      return;
    }

    loadMatches(selectedLeague, selectedDate, selectedDate);
  }

  function handleCloseModal() {
    setSelectedMatch(null);
    setPrediction(null);
  }

  async function handleAnalyzeMatch(match) {
    setSelectedMatch(match);
    setPrediction(null);

    try {
      setIsLoadingPrediction(true);
      setError(null);
      const result = await predictMatch(match);
      setPrediction(result);
    } catch (err) {
      console.error(err);
      // No mostramos error global, solo dejamos que el modal muestre estado de error
      setPrediction(null);
    } finally {
      setIsLoadingPrediction(false);
    }
  }

  return (
    <>
      <Header />
      <main>
        <HeroSection />
        {error && (
          <div className="pm-container">
            <div className="error-message">{error}</div>
          </div>
        )}
        <FiltersSection
          competitions={competitions}
          selectedLeague={selectedLeague}
          onLeagueChange={handleLeagueChange}
          selectedDate={selectedDate}
          onDateChange={handleDateChange}
          onSearch={handleSearch}
          isLoading={isLoadingMatches}
        />
        <MatchesSection
          matches={matches}
          onAnalyzeMatch={handleAnalyzeMatch}
          isLoading={isLoadingMatches}
          selectedDate={selectedDate}
        />
      </main>

      {/* Modal de analisis */}
      <AnalysisModal
        match={selectedMatch}
        prediction={prediction}
        isLoading={isLoadingPrediction}
        onClose={handleCloseModal}
      />
    </>
  );
}

export default HomePage;
