# 🔗 Six Degrees

A minimalist word association game where you connect two unrelated words in as few steps as possible.

![Six Degrees Game](https://img.shields.io/badge/React-18-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![SQLite](https://img.shields.io/badge/SQLite-3-orange)

## 🎮 How to Play

1. You're given two random words (e.g., **OCEAN** → **KEYBOARD**)
2. Build a chain of associations to connect them
3. Each word must be semantically related to the previous
4. Maximum of 6 moves allowed
5. Fewer links = higher score!

### Scoring

| Condition | Points |
|-----------|--------|
| Perfect (matches shortest path) | 100 |
| +1 extra word | 80 |
| +2 extra words | 60 |
| Completed but longer | 40 |
| No valid path found | 0 |

## 📁 Project Structure

```
six-degrees/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API service layer
│   │   ├── styles/         # Global styles
│   │   └── utils/          # Helper functions
│   ├── public/
│   └── package.json
│
├── backend/                # Flask API
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper utilities
│   ├── tests/              # Unit tests
│   ├── data/               # Word database
│   └── requirements.txt
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- pip

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m app.init_db

# Run server
flask run --port 5000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The game will be available at `http://localhost:5173`

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/game/new` | Generate new puzzle |
| POST | `/api/game/validate` | Validate a word in chain |
| POST | `/api/game/submit` | Submit completed chain |
| GET | `/api/game/hint` | Get hint for current puzzle |
| GET | `/api/stats` | Get game statistics |

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, CSS Modules
- **Backend**: Flask 3.0, SQLite3
- **Algorithm**: Breadth-First Search (BFS) for shortest path

## 📝 Game Logic

The backend uses a graph-based word association database where:
- Each word is a node
- Semantic connections form edges
- BFS finds the optimal path
- Player paths are validated against the graph

## 🎨 Design Philosophy

- Minimalist UI with focus on gameplay
- Responsive design for mobile/desktop
- Instant feedback on word validity
- Smooth animations for chain building

## 📄 License

MIT License - feel free to use and modify!

