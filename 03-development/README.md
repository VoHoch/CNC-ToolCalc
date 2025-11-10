# 03-development - Entwicklungsbereich

**Hinweis:** Der Quellcode befindet sich aus praktischen Gründen im Root-Verzeichnis:

## Code-Struktur

```
CNC-ToolCalc/
├── backend/          ← Backend Code (FastAPI)
├── frontend/         ← Frontend Code (React + Vite)
└── scripts/          ← Build & Test Scripts
```

### Backend (FastAPI + Python)

**Verzeichnis:** `../backend/`

- **10-Phase Calculation Engine** (Cleanroom Implementation)
- **FastAPI REST API** (7 Endpoints)
- **8-Checks Validation System**
- **Tests:** 35 Unit + 9 Integration Tests

**Start Backend:**
```bash
cd backend
source venv/bin/activate  # Python venv
uvicorn main:app --reload
```

**Run Tests:**
```bash
cd backend
pytest --cov=backend
```

---

### Frontend (React + TypeScript + Vite)

**Verzeichnis:** `../frontend/`

- **6-Screen Workflow**
- **Design System** (Dark Theme + 3 Contrast Modes)
- **7 UI Components** (Slider, Table, Button, Card, etc.)
- **5 Zustand Stores** (State Management)
- **API Client** (Backend Integration)

**Start Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Storybook:**
```bash
cd frontend
npm run storybook
```

---

### Scripts

**Verzeichnis:** `../scripts/`

Build, Test und Quality Gate Scripts.

---

### Git Branches

- `main` - Production
- `develop` - Integration (wird morgen erstellt)
- `agent/ui-specialist` - UI Components & Design System
- `agent/frontend-workflow` - 6 Screens + State Management
- `agent/backend-calculation` - 10-Phase Engine + API

---

**Dokumentation:** Siehe `../01-dokumentation/`
