# GrantFinder Ireland

Discover every government grant, scheme, relief, and entitlement you qualify for in Ireland.

## Architecture

- **Backend**: Python / FastAPI / PostgreSQL / Redis
- **Frontend**: Next.js 14 / TypeScript / Tailwind CSS
- **AI**: Anthropic Claude API for summaries and chat
- **Payments**: Stripe
- **PDF Reports**: WeasyPrint + Jinja2

## Quick Start

### Prerequisites

- Docker & Docker Compose (for database + Redis)
- Python 3.12+
- Node.js 20+

### 1. Start the database

```bash
docker compose up -d db redis
```

### 2. Set up the backend

```bash
cd backend
cp .env.example .env       # Edit with your settings
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is now at http://localhost:8000 (docs at http://localhost:8000/docs).

### 3. Seed the grant database

Use the admin import endpoint to load the initial grant catalogue:

```bash
curl -X POST http://localhost:8000/api/v1/admin/grants/import \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@data/grants_seed.json"
```

Or in development, the tables auto-create and you can import via the Swagger UI.

### 4. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

The app is now at http://localhost:3000.

### 5. Run tests

```bash
cd backend
pytest tests/ -v
```

## Project Structure

```
grantfinder/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── config.py         # Environment settings
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models/           # ORM models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── api/              # Route handlers
│   │   ├── engine/           # Grant matching rules engine
│   │   ├── ai/               # Claude API integration
│   │   ├── reports/          # PDF report generator
│   │   ├── services/         # Business logic
│   │   └── utils/            # Auth, S3, validators
│   ├── data/                  # Seed data (grants JSON)
│   └── tests/                 # Unit tests
├── frontend/
│   └── src/
│       ├── app/              # Next.js pages
│       ├── components/       # React components
│       ├── lib/              # API client, utils
│       ├── stores/           # Zustand state
│       └── types/            # TypeScript types
└── docker-compose.yml
```

## Key Features

1. **Rules Engine** (`backend/app/engine/matcher.py`): Evaluates user profiles against eligibility rules using AND/OR logic groups
2. **7-Step Questionnaire**: Mobile-first wizard with conditional logic
3. **89 Irish Grants**: Comprehensive catalogue with eligibility rules
4. **AI Summaries**: Claude-powered personalised result summaries
5. **PDF Reports**: Professional grant reports with application guides
6. **Stripe Payments**: Free/Report/Premium tiers

## API Documentation

When running locally, visit http://localhost:8000/docs for the full Swagger/OpenAPI documentation.

## Grant Data

The initial grant catalogue (`backend/data/grants_seed.json`) contains 40+ Irish grants with eligibility rules. The full 89-grant catalogue should be completed by populating rules for all grants listed in the specification.

## License

Proprietary — GrantFinder Ireland.
