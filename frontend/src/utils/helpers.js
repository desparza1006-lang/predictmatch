/**
 * Traduce el estado de un partido de la API a español.
 * @param {string} status - Estado del partido en inglés
 * @returns {string} - Estado traducido
 */
export function translateMatchStatus(status) {
  const statusMap = {
    SCHEDULED: "Programado",
    TIMED: "Horario definido",
    IN_PLAY: "En juego",
    PAUSED: "Descanso",
    FINISHED: "Finalizado",
    SUSPENDED: "Suspendido",
    POSTPONED: "Aplazado",
    CANCELLED: "Cancelado",
    AWARDED: "Asignado",
  };
  return statusMap[status] || status || "Sin estado";
}

/**
 * Formatea una fecha para mostrarla de forma legible.
 * @param {string} dateString - Fecha en formato ISO
 * @returns {string} - Fecha formateada
 */
export function formatMatchDate(dateString) {
  if (!dateString) return "Fecha no disponible";

  const date = new Date(dateString);
  return date.toLocaleString("es-ES", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Formatea solo la hora de un partido.
 * @param {string} dateString - Fecha en formato ISO
 * @returns {string} - Hora formateada
 */
export function formatMatchTime(dateString) {
  if (!dateString) return "";

  const date = new Date(dateString);
  return date.toLocaleTimeString("es-ES", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Obtiene la etiqueta legible para un resultado de predicción.
 * @param {string} result - Resultado (HOME_TEAM, AWAY_TEAM, DRAW)
 * @returns {string} - Etiqueta legible
 */
export function getResultLabel(result) {
  const labels = {
    HOME_TEAM: "Victoria local",
    AWAY_TEAM: "Victoria visitante",
    DRAW: "Empate",
  };
  return labels[result] || result;
}
