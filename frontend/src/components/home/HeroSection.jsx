function HeroSection() {
  return (
    <section className="hero-section" id="home">
      <div className="pm-container hero-section__content">
        <div className="hero-section__text">
          <span className="hero-section__badge">Versión 1.0</span>
          <h2>Predicciones prepartido con datos reales y análisis claro</h2>
          <p>
            PredictMatch analiza partidos de distintas ligas, compara métricas
            recientes y genera una predicción explicable sobre el posible
            resultado del encuentro.
          </p>

          <div className="hero-section__actions">
            <a href="#matches" className="pm-button pm-button--primary">
              Ver partidos
            </a>
            <a href="#analysis" className="pm-button pm-button--secondary">
              Explorar analisis
            </a>
          </div>
        </div>

        <div className="hero-section__card">
          <div className="hero-metric">
            <span className="hero-metric__label">Modelo</span>
            <strong>Prepartido mejorado</strong>
          </div>
          <div className="hero-metric">
            <span className="hero-metric__label">Cobertura inicial</span>
            <strong>Premier League y La Liga</strong>
          </div>
          <div className="hero-metric">
            <span className="hero-metric__label">Fuente</span>
            <strong>football-data.org</strong>
          </div>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;