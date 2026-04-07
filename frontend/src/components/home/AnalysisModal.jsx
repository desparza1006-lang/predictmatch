import { useEffect, useCallback } from "react";
import {
  translateMatchStatus,
  formatMatchDate,
  getResultLabel,
} from "../../utils/helpers";

function AnalysisModal({ match, prediction, isLoading, onClose }) {
  // Cerrar con tecla Escape
  const handleEscape = useCallback(
    (event) => {
      if (event.key === "Escape") {
        onClose();
      }
    },
    [onClose]
  );

  useEffect(() => {
    if (match) {
      document.addEventListener("keydown", handleEscape);
      // Bloquear scroll en el body
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      // Restaurar scroll
      document.body.style.overflow = "";
    };
  }, [match, handleEscape]);

  // No renderizar si no hay partido seleccionado
  if (!match) return null;

  // Cerrar al hacer clic en el overlay (fuera del modal)
  function handleOverlayClick(event) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  return (
    <div
      className="modal-overlay"
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="modal-container">
        <div className="modal-header">
          <h3 id="modal-title" className="modal-title">
            Analisis del partido
          </h3>
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="Cerrar modal"
          >
            ×
          </button>
        </div>

        <div className="modal-content">
          {/* Información del partido */}
          <div className="modal-match-info">
            <div className="modal-match-competition">
              {match.competition?.name || "Liga"}
            </div>

            <div className="modal-match-teams">
              <div className="modal-team home-team">
                <span className="team-label">Local</span>
                <strong className="team-name">
                  {match.homeTeam?.name || "Equipo local"}
                </strong>
              </div>

              <span className="modal-vs">VS</span>

              <div className="modal-team away-team">
                <span className="team-label">Visitante</span>
                <strong className="team-name">
                  {match.awayTeam?.name || "Equipo visitante"}
                </strong>
              </div>
            </div>

            <div className="modal-match-details">
              <span
                className={`match-status status-${match.status?.toLowerCase()}`}
              >
                {translateMatchStatus(match.status)}
              </span>
              <span className="match-date">
                {formatMatchDate(match.utcDate)}
              </span>
              {match.matchday && (
                <span className="match-matchday">
                  Jornada {match.matchday}
                </span>
              )}
            </div>
          </div>

          {/* Sección de predicción */}
          <div className="modal-prediction">
            <h4 className="prediction-title">Prediccion del modelo</h4>

            {isLoading ? (
              <div className="prediction-loading">
                <div className="loading-spinner"></div>
                <p>Analizando datos del partido...</p>
              </div>
            ) : prediction ? (
              <div className="prediction-content">
                <div className="prediction-result">
                  <span className="result-label">Resultado esperado:</span>
                  <span
                    className={`result-value result-${prediction.predicted_result?.toLowerCase()}`}
                  >
                    {getResultLabel(prediction.predicted_result)}
                  </span>
                </div>

                <div className="prediction-probabilities">
                  <div className="prob-item">
                    <span className="prob-name">Victoria local</span>
                    <div className="prob-bar-container">
                      <div
                        className="prob-bar prob-bar--home"
                        style={{
                          width: `${(prediction.probabilities?.HOME_TEAM || 0) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="prob-percentage">
                      {Math.round((prediction.probabilities?.HOME_TEAM || 0) * 100)}%
                    </span>
                  </div>

                  <div className="prob-item">
                    <span className="prob-name">Empate</span>
                    <div className="prob-bar-container">
                      <div
                        className="prob-bar prob-bar--draw"
                        style={{
                          width: `${(prediction.probabilities?.DRAW || 0) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="prob-percentage">
                      {Math.round((prediction.probabilities?.DRAW || 0) * 100)}%
                    </span>
                  </div>

                  <div className="prob-item">
                    <span className="prob-name">Victoria visitante</span>
                    <div className="prob-bar-container">
                      <div
                        className="prob-bar prob-bar--away"
                        style={{
                          width: `${(prediction.probabilities?.AWAY_TEAM || 0) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="prob-percentage">
                      {Math.round((prediction.probabilities?.AWAY_TEAM || 0) * 100)}%
                    </span>
                  </div>
                </div>

                {prediction.explanation && (
                  <div className="prediction-explanation-box">
                    <p>{prediction.explanation}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="prediction-error">
                <p>
                  No se pudo generar la prediccion. Es posible que no haya
                  suficientes datos historicos para estos equipos.
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="modal-footer">
          <button className="pm-button pm-button--primary" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}

export default AnalysisModal;
