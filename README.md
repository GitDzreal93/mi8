# Military Intelligence Dashboard

A comprehensive military situational awareness system that aggregates, processes, and visualizes military events from multiple data sources.

## Features

### Backend (FastAPI + Python)
- **Multi-source data ingestion**: GNews, NewsAPI, ACLED, RSSHub
- **AI-powered structuring**: DeepSeek LLM for event extraction and analysis
- **PostgreSQL + PostGIS**: Geospatial data storage and querying
- **Smart deduplication**: Hash-based and similarity-based duplicate detection
- **Quota management**: Per-source API rate limiting and usage tracking
- **Alert system**: Email and Slack notifications for high-importance events
- **REST API**: Comprehensive endpoints for events, heatmap, and source health

### Frontend (Next.js + TypeScript)
- **Interactive map**: Leaflet/OSM with event markers and clustering
- **Real-time updates**: Auto-refreshing data with React Query
- **Advanced filtering**: Time range, importance, event type, source, and search
- **Event details**: Comprehensive event information display
- **Source health monitoring**: Real-time API usage and status tracking
- **Bilingual support**: English and Chinese (i18n)
- **Responsive design**: Mobile-friendly interface with Tailwind CSS

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   FastAPI       │───▶│   PostgreSQL    │
│  (GNews, ACLED, │    │   Backend       │    │   + PostGIS     │
│   NewsAPI, etc) │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   DeepSeek LLM  │
                       │  (Structuring)  │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Next.js Front  │
                       │     (Web UI)    │
                       └─────────────────┘
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Node.js 18+
- API keys for data sources (see `.env.example`)

### 1. Start PostgreSQL with PostGIS

```bash
docker-compose up -d
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Initialize database
python -m app.db

# Run the backend
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs` (Swagger UI)

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed (default API URL: http://localhost:8000)

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Backend Environment Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/milintel

# DeepSeek LLM
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_MODEL=deepseek-chat

# Data Sources
GNEWS_API_KEY=your_key
NEWSAPI_API_KEY=your_key
ACLED_API_KEY=your_key

# Alerting (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
SLACK_WEBHOOK_URL=your_webhook_url
```

### Frontend Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### Events
- `GET /events` - List events with filters
- `GET /events/{id}` - Get event details
- `GET /events/types/list` - List event types
- `GET /events/sources/list` - List event sources

### Heatmap
- `GET /heatmap` - Get heatmap data points
- `GET /heatmap/geojson` - Get heatmap as GeoJSON

### Sources
- `GET /sources/health` - Get data source health and quota status

### Admin (Requires authentication)
- `POST /admin/refresh` - Trigger manual data refresh
- `GET /admin/stats` - Get system statistics

### Authentication
- `POST /auth/login` - Login and get JWT token

## Data Sources

| Source | Description | Daily Limit |
|--------|-------------|-------------|
| GNews | Google News aggregator | 100 requests |
| NewsAPI | News articles | 100 requests |
| ACLED | Armed conflict events | 1000 requests |
| RSSHub | RSS feed aggregator | 1000 requests |
| NASA FIRMS | Fire data (optional) | 200 requests |

## Development

### Backend Project Structure

```
backend/
├── app/
│   ├── api/routes/       # API endpoints
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── config.py         # Configuration
│   ├── db.py             # Database connection
│   └── services/
│       ├── ingest/       # Data source fetchers
│       ├── deepseek.py   # LLM integration
│       ├── dedup.py      # Deduplication logic
│       ├── quota.py      # Quota management
│       ├── alerts.py     # Alert system
│       └── scheduler.py  # Background tasks
└── requirements.txt
```

### Frontend Project Structure

```
frontend/
├── app/
│   ├── page.tsx          # Main dashboard page
│   ├── layout.tsx        # Root layout
│   ├── globals.css       # Global styles
│   └── providers.tsx     # React Query provider
├── components/
│   ├── map/              # Map components
│   ├── events/           # Event components
│   └── sources/          # Source health components
├── lib/
│   ├── api.ts            # API client
│   └── i18n.ts           # Translations
├── hooks/
│   └── use-events.ts     # React Query hooks
└── package.json
```

## Production Deployment

### Backend

```bash
# Use production ASGI server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
# Build production bundle
npm run build

# Start production server
npm start
```

### Docker Deployment

```bash
# Build and run all services
docker-compose up -d
```

## Features in Detail

### Event Structuring with DeepSeek LLM

The system uses DeepSeek's language model to extract structured information from raw news articles:

- Event type classification
- Importance scoring (1-5)
- Location extraction (lat/lng)
- Actor identification
- Equipment detection
- Casualty information
- Tag generation
- Bilingual summaries (English/Chinese)

### Smart Deduplication

- Hash-based deduplication using title, source, and timestamp
- Similarity-based filtering using Jaccard similarity
- Canonical event IDs for cross-source correlation

### Alert System

High-importance events (importance ≥ 4) trigger automatic alerts via:

- Email notifications with detailed event information
- Slack webhooks for team notifications
- Configurable importance thresholds
- Quota usage alerts when approaching limits

### Source Health Monitoring

Real-time tracking of:

- API response status
- Last successful poll time
- Daily quota usage
- Error messages and retry logic
- Automatic throttling at 80% quota threshold

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the ISC License.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [Leaflet](https://leafletjs.com/) - Interactive maps
- [DeepSeek](https://www.deepseek.com/) - AI language model
- [PostGIS](https://postgis.net/) - Spatial database extension
