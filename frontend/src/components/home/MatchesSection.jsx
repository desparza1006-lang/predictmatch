import { useState } from "react";
import {
  translateMatchStatus,
  formatMatchTime,
} from "../../utils/helpers";

const MATCHES_PER_PAGE = 20;

function MatchesSection({
  matches,
  onAnalyzeMatch,
  isLoading,
  selectedDate,
}) {
  const [currentPage, setCurrentPage] = useState(1);

  // Calcular paginacion
  const totalPages = Math.max(1, Math.ceil(matches.length / MATCHES_PER_PAGE));

  // Asegurar que la pagina actual sea valida
  const validPage = Math.min(currentPage, totalPages);
  if (validPage !== currentPage) {
    setCurrentPage(validPage);
  }

  const startIndex = (validPage - 1) * MATCHES_PER_PAGE;
  const paginatedMatches = matches.slice(
    startIndex,
    startIndex + MATCHES_PER_PAGE
  );

  function handlePageChange(newPage) {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
      // Scroll suave al inicio de la seccion de partidos
      document.getElementById("matches")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }

  // Generar array de numeros de pagina a mostrar
  function getPageNumbers() {
    const pages = [];
    const maxVisiblePages = 5;

    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Mostrar primera pagina, ultima pagina, y paginas alrededor de la actual
      if (validPage <= 3) {
        for (let i = 1; i <= 4; i++) pages.push(i);
        pages.push("...");
        pages.push(totalPages);
      } else if (validPage >= totalPages - 2) {
        pages.push(1);
        pages.push("...");
        for (let i = totalPages - 3; i <= totalPages; i++) pages.push(i);
      } else {
        pages.push(1);
        pages.push("...");
        for (let i = validPage - 1; i <= validPage + 1; i++) pages.push(i);
        pages.push("...");
        pages.push(totalPages);
      }
    }
    return pages;
  }

  // Mensaje personalizado segun el estado
  function getEmptyStateMessage() {
    if (selectedDate) {
      return `No hay partidos disponibles para la fecha seleccionada (${selectedDate}). Intenta con otra fecha.`;
    }
    return "No hay partidos disponibles para esta liga en este momento. Intenta con otra liga o fecha.";
  }

  return (
    <section className="matches-section" id="matches">
      <div className="pm-container">
        <div className="section-heading">
          <h3>Partidos disponibles</h3>
          <p>
            {matches.length > 0
              ? `Mostrando ${matches.length} partido${matches.length !== 1 ? "s" : ""}`
              : "Selecciona una liga y fecha para ver los partidos disponibles"}
          </p>
        </div>

        <div className="matches-grid">
          {isLoading ? (
            <div className="empty-state empty-state--loading">
              <div className="loading-spinner"></div>
              <p>Cargando partidos...</p>
            </div>
          ) : matches.length === 0 ? (
            <div className="empty-state">
              <p className="empty-state__title">No hay partidos</p>
              <p className="empty-state__message">{getEmptyStateMessage()}</p>
            </div>
          ) : (
            paginatedMatches.map((match) => (
              <article key={match.id} className="match-card">
                <div className="match-card__top">
                  <span className="match-card__league">
                    {match.competition?.name || "Liga"}
                  </span>
                  <span
                    className={`match-card__status status-${match.status?.toLowerCase()}`}
                  >
                    {translateMatchStatus(match.status)}
                  </span>
                </div>

                <div className="match-card__teams">
                  <div className="match-team">
                    <span className="match-team__label">Local</span>
                    <strong>
                      {match.homeTeam?.shortName || match.homeTeam?.name}
                    </strong>
                  </div>
                  <span className="match-card__vs">vs</span>
                  <div className="match-team">
                    <span className="match-team__label">Visitante</span>
                    <strong>
                      {match.awayTeam?.shortName || match.awayTeam?.name}
                    </strong>
                  </div>
                </div>

                <div className="match-card__bottom">
                  <span className="match-time">
                    {formatMatchTime(match.utcDate)}
                  </span>
                  <button
                    className="pm-button pm-button--secondary"
                    onClick={() => onAnalyzeMatch(match)}
                    disabled={isLoading}
                  >
                    Ver analisis
                  </button>
                </div>
              </article>
            ))
          )}
        </div>

        {/* Controles de paginacion */}
        {!isLoading && matches.length > 0 && totalPages > 1 && (
          <nav className="pagination" aria-label="Paginacion de partidos">
            <button
              className="pagination__button pagination__button--prev"
              onClick={() => handlePageChange(validPage - 1)}
              disabled={validPage === 1}
              aria-label="Pagina anterior"
            >
              Anterior
            </button>

            <div className="pagination__pages">
              {getPageNumbers().map((page, index) =>
                page === "..." ? (
                  <span key={`ellipsis-${index}`} className="pagination__ellipsis">
                    ...
                  </span>
                ) : (
                  <button
                    key={page}
                    className={`pagination__page ${validPage === page ? "pagination__page--active" : ""}`}
                    onClick={() => handlePageChange(page)}
                    aria-label={`Pagina ${page}`}
                    aria-current={validPage === page ? "page" : undefined}
                  >
                    {page}
                  </button>
                )
              )}
            </div>

            <button
              className="pagination__button pagination__button--next"
              onClick={() => handlePageChange(validPage + 1)}
              disabled={validPage === totalPages}
              aria-label="Pagina siguiente"
            >
              Siguiente
            </button>
          </nav>
        )}

        {/* Info de paginacion */}
        {!isLoading && matches.length > 0 && (
          <div className="pagination__info">
            Mostrando {startIndex + 1} -{" "}
            {Math.min(startIndex + MATCHES_PER_PAGE, matches.length)} de{" "}
            {matches.length} partidos
          </div>
        )}
      </div>
    </section>
  );
}

export default MatchesSection;
