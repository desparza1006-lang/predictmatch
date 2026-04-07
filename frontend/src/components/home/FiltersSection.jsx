function FiltersSection({
  competitions,
  selectedLeague,
  onLeagueChange,
  selectedDate,
  onDateChange,
  onSearch,
  isLoading,
}) {
  return (
    <section className="filters-section" id="analysis">
      <div className="pm-container">
        <div className="section-heading">
          <h3>Centro de analisis</h3>
          <p>Selecciona una liga y revisa los partidos disponibles para analizar.</p>
        </div>

        <div className="filters-card">
          <div className="filters-grid">
            <div className="pm-field">
              <label htmlFor="league">Liga</label>
              <select
                id="league"
                value={selectedLeague}
                onChange={onLeagueChange}
                disabled={isLoading}
              >
                <option value="">Selecciona una liga</option>
                {competitions.map((competition) => (
                  <option key={competition.id} value={competition.code}>
                    {competition.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="pm-field">
              <label htmlFor="match-date">Fecha</label>
              <input
                id="match-date"
                type="date"
                value={selectedDate}
                onChange={onDateChange}
                disabled={isLoading}
              />
            </div>

            <div className="pm-field pm-field--action">
              <label className="pm-field__spacer">Buscar</label>
              <button
                className="pm-button pm-button--primary"
                onClick={onSearch}
                disabled={isLoading}
              >
                {isLoading ? "Cargando..." : "Analizar"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default FiltersSection;