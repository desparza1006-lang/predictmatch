# PredictMatch

<p align="center">
  <strong>Análisis predictivo de partidos de fútbol con Machine Learning</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/Python-3.10+-green.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/React-19+-61DAFB.svg" alt="React 19+">
  <img src="https://img.shields.io/badge/FastAPI-0.135+-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="License MIT">
</p>

---

## 📋 Descripción General

**PredictMatch** es una aplicación web full-stack que permite consultar partidos de fútbol de diversas competiciones europeas, analizar estadísticas de equipos y obtener predicciones de resultados (victoria local, empate o victoria visitante) mediante modelos de Machine Learning.

El sistema combina datos en tiempo real de la API [football-data.org](https://www.football-data.org/) con algoritmos de clasificación para ofrecer predicciones fundamentadas y explicaciones de los factores clave que influyen en cada pronóstico.

---

## 🎯 Objetivo del Sistema

Proporcionar a los usuarios una herramienta intuitiva para:

- Explorar competiciones y partidos de fútbol actualizados
- Visualizar estadísticas previas de los equipos
- Obtener predicciones de resultados basadas en datos históricos
- Comprender qué factores pesan más en cada predicción

---

## ✨ Características Principales

| Característica | Descripción |
|----------------|-------------|
| **🏆 Competiciones** | Listado de ligas disponibles (La Liga, Premier League, Bundesliga, Serie A, etc.) |
| **⚽ Partidos** | Visualización de partidos por competición y fecha |
| **🔮 Predicciones ML** | Pronósticos de resultados usando Random Forest |
| **📊 Explicaciones** | Factores clave que influyen en cada predicción |
| **🗄️ Persistencia** | Almacenamiento local de datos en SQLite |
| **📱 Responsive** | Interfaz adaptada a dispositivos móviles y escritorio |

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10+** - Lenguaje principal
- **FastAPI 0.135** - Framework web moderno y rápido
- **SQLite** - Base de datos local (sin servidor externo)
- **scikit-learn** - Machine Learning (Random Forest Classifier)
- **pandas** - Manipulación y análisis de datos
- **requests** - Cliente HTTP para API externa
- **uvicorn** - Servidor ASGI

### Frontend
- **React 19** - Biblioteca de UI
- **Vite** - Build tool y dev server
- **ESLint** - Linter para código JavaScript

### APIs Externas
- **football-data.org** - Datos de competiciones y partidos en tiempo real

---

## 📁 Estructura del Proyecto

```
PredictMatch/
├── app/                          # Backend FastAPI
│   ├── api/
│   │   ├── routes/               # Endpoints (competitions, matches, predictions)
│   │   └── schemas/              # Esquemas Pydantic
│   ├── config/                   # Configuración y logging
│   ├── db/                       # Modelos y conexión SQLite
│   │   └── repositories/         # Capa de acceso a datos
│   ├── jobs/                     # Scripts de sincronización
│   ├── ml/                       # Modelos ML (entrenamiento, predicción, features)
│   ├── services/                 # Lógica de negocio
│   └── utils/                    # Utilidades
├── frontend/                     # Frontend React
│   ├── src/
│   │   ├── components/           # Componentes UI
│   │   ├── pages/                # Páginas principales
│   │   └── services/             # Cliente API
│   └── public/                   # Assets estáticos
├── notebooks/                    # Experimentos Jupyter
├── scripts/                      # Scripts utilitarios
├── tests/                        # Suite de tests
├── predictmatch.db               # Base de datos SQLite
├── requirements.txt              # Dependencias Python
└── .env                          # Variables de entorno
```

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10** o superior
- **Node.js 18** o superior (para el frontend)
- **npm** o **yarn**
- **Git**

Además, necesitarás:
- Una **API Key gratuita** de [football-data.org](https://www.football-data.org/) (registro gratuito con límite de 10 requests/minuto)

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd PredictMatch
```

### 2. Configurar el Backend

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar el Frontend

```bash
cd frontend
npm install
cd ..
```

---

## ⚙️ Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (o copia el ejemplo):

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores:

```env
# Configuración de la aplicación
APP_NAME=PredictMatch
APP_ENV=development
APP_DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000

# API de football-data.org (OBLIGATORIO)
# Obtén tu API key gratuita en: https://www.football-data.org/
FOOTBALL_DATA_API_KEY=tu_api_key_aqui
FOOTBALL_DATA_BASE_URL=https://api.football-data.org/v4
```

> ⚠️ **Importante**: Sin la API key de football-data.org, la aplicación no podrá obtener datos de partidos. El plan gratuito permite 10 requests por minuto.

---

## ▶️ Ejecución Local

El proyecto requiere ejecutar **backend y frontend por separado** en terminales diferentes.

### Terminal 1 - Backend

```bash
# Asegúrate de estar en la raíz del proyecto y el venv activado
venv\Scripts\activate  # Windows

# Iniciar servidor FastAPI
uvicorn app.main:app --reload
```

El backend estará disponible en: **http://127.0.0.1:8000**

Documentación automática:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Terminal 2 - Frontend

```bash
cd frontend

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

> La aplicación frontend se conecta automáticamente al backend mediante CORS configurado.

---

## 🔌 APIs y Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Estado de la API |
| `/competitions/` | GET | Listar todas las competiciones |
| `/matches/` | GET | Listar partidos (opcional: filtrar por competición/fecha) |
| `/matches/predict-test/{match_id}` | GET | Predicción para un partido existente |
| `/matches/train` | POST | Entrenar el modelo ML |
| `/predictions/predict-match` | POST | Predicción para partido enviado directamente |

---

## 🤖 Machine Learning

El sistema utiliza un modelo **Random Forest Classifier** para predecir resultados:

1. **Entrenamiento**: Ejecuta `POST /matches/train` para entrenar el modelo con datos históricos
2. **Predicción**: Selecciona un partido y el modelo calculará probabilidades para:
   - Victoria local (HOME)
   - Empate (DRAW)
   - Victoria visitante (AWAY)
3. **Explicación**: El sistema explica qué factores influyeron más en la predicción

> **Nota**: El modelo debe entrenarse al menos una vez antes de realizar predicciones.

---

## 🗄️ Base de Datos

El proyecto utiliza **SQLite** (archivo local `predictmatch.db`), lo que significa:

- ✅ No requiere instalar ni configurar un servidor de base de datos
- ✅ Los datos se almacenan localmente en un archivo
- ✅ Las tablas se crean automáticamente al iniciar la aplicación

**Tablas principales:**
- `competitions` - Competiciones disponibles
- `matches` - Partidos sincronizados
- `predictions` - Historial de predicciones realizadas

---

## 📝 Datos de Fútbol (API Externa)

Los datos provienen de **football-data.org**:

- **Plan gratuito**: 10 requests/minuto
- **Datos disponibles**: Competiciones europeas principales, partidos, resultados, clasificaciones
- **Actualización**: Datos en tiempo real (con restricciones del plan)

Para usar la API:
1. Regístrate en https://www.football-data.org/
2. Obtén tu API key gratuita
3. Configúrala en el archivo `.env`

---

## ⚠️ Limitaciones y Notas Importantes

### Version 1.0.0 - Estado Actual

| Aspecto | Estado | Notas |
|---------|--------|-------|
| Funcionalidad básica | ✅ Operativa | Listado de partidos y predicciones |
| API externa | ⚠️ Limitada | 10 req/min en plan gratuito |
| Modelo ML | ✅ Funcional | Requiere entrenamiento previo |
| Base de datos | ✅ SQLite local | No requiere servidor externo |
| Tests | ⚠️ Básicos | Suite de tests en desarrollo |
| Jobs de sincronización | ⚠️ Parciales | Algunos scripts están en desarrollo |

### Consideraciones para Producción

- **No está optimizado para producción** en su estado actual
- El modelo ML requiere datos suficientes para entrenar correctamente
- La API gratuita tiene limitaciones de rate limiting
- SQLite es adecuado para desarrollo; considerar PostgreSQL/MySQL para producción
- Se recomienda agregar autenticación antes de exponer públicamente

---

## 🧪 Testing

### Backend (Python)

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_api/test_matches.py

# Con cobertura
pytest --cov=app --cov-report=html
```

### Frontend (JavaScript)

```bash
cd frontend
npm run lint
```

---

## 🐛 Solución de Problemas

### Error: "No se pudieron cargar las competiciones"
- Verifica que tu `FOOTBALL_DATA_API_KEY` esté configurada correctamente en `.env`
- Reinicia el servidor backend después de cambiar variables de entorno

### Error: "El modelo no ha sido entrenado"
- Ejecuta el endpoint `POST /matches/train` para entrenar el modelo antes de predecir

### Error de CORS en el navegador
- Asegúrate de que el backend esté corriendo en el puerto 8000
- El CORS está configurado para permitir `http://localhost:5173`

---

## 📌 Estado del Proyecto

- **Versión actual**: `1.0.0`
- **Estado**: Funcional para desarrollo local
- **Próximas mejoras**: Tests completos, jobs de sincronización, modelo ML mejorado

---

## 📄 Licencia

Este proyecto es de código abierto. Consulta el archivo LICENSE para más detalles.

---

<p align="center">
  Desarrollado con ⚽ para aficionados al fútbol y la tecnología
</p>
