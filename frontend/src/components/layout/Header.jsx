import logo from "../../assets/PredictMatch.png";

function Header() {
  return (
    <header className="pm-header">
      <div className="pm-container pm-header__content">
        <div className="pm-brand">
          <img src={logo} alt="PredictMatch logo" className="pm-brand__logo" />
          <div className="pm-brand__text">
            <h1>PredictMatch</h1>
            <p>Analítica predictiva para fútbol</p>
          </div>
        </div>

        <nav className="pm-nav">
          <a href="#home">Inicio</a>
          <a href="#matches">Partidos</a>
          <a href="#analysis">Análisis</a>
        </nav>
      </div>
    </header>
  );
}

export default Header;