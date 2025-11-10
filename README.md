# CNC-ToolCalc

**Version:** v0.0.1-alpha
**Target:** Production-ready v1.0.0
**Status:** In Development

---

## Project Overview

CNC-ToolCalc is a professional CNC cutting parameter calculator designed for small to medium-sized manufacturing businesses (KMU). It calculates optimal cutting parameters based on tool geometry, material properties, and machining operations.

### Key Features (v1.0.0 Target)

- **13 Operations:** Face, Slot, Geometry, Special strategies
- **7 Materials:** Softwood → Steel (hardness-sorted)
- **6 Tool Coatings:** None, TiN, TiAlN, AlTiN, Diamond, Carbide
- **4 Surface Quality Levels:** Roughing, Standard, Finishing, High-Finish
- **Expert Mode:** Global slider + individual parameter overrides
- **Fusion 360 Export:** Parametric .tools with 13 expressions
- **Smart Preset Detection:** Auto-detect existing presets from Fusion
- **Mathematical Workbook:** Formula transparency for every calculation

---

## Technology Stack

### Frontend
- **Framework:** React 18 + Vite
- **Language:** TypeScript (strict)
- **State:** Zustand
- **Testing:** Vitest + React Testing Library
- **Styling:** CSS (Dark Theme only, no UI libraries)

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Engine:** V2.0 Calculation Engine (NO-TOUCH principle)
- **Validation:** Pydantic
- **Testing:** pytest

### Infrastructure
- **Database:** PostgreSQL (production) / SQLite (dev)
- **Cache:** Redis (optional)
- **Deployment:** Docker Compose (local MacBook)

---

## Project Structure

```
cnc-toolcalc/
├── backend/               # FastAPI Backend
│   ├── v2_engine/        # V2.0 Calculation Engine (NO-TOUCH!)
│   ├── services/         # Service Layer (wrappers)
│   ├── api/              # FastAPI Routes
│   ├── models/           # Pydantic Models
│   └── tests/            # Backend Tests
├── frontend/             # React Frontend
│   ├── src/
│   │   ├── screens/     # 8 Screens (workflow)
│   │   ├── components/  # Reusable components
│   │   ├── state/       # Zustand store
│   │   └── api/         # API client
│   └── tests/           # Frontend Tests
├── docs/                # Architecture & Documentation
│   ├── architecture/    # Complete V4 Architecture
│   ├── contracts/       # API Contracts, Component Interfaces
│   └── adrs/            # Architecture Decision Records
├── .agent-reports/      # Agent Status Reports (Git-tracked!)
│   ├── governance/
│   ├── ui-specialist/
│   ├── frontend-workflow/
│   └── backend-calculation/
├── scripts/             # Build, Deploy, Quality Gates
└── README.md
```

---

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Setup

```bash
# Clone repository
git clone <repository-url>
cd cnc-toolcalc

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
npm install

# Run Development Servers
# Terminal 1 - Backend
cd backend
uvicorn api.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Frontend:** http://localhost:5173
**Backend API:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

---

## Development Workflow

### Agents & Responsibilities

This project uses a **Multi-Agent Development Approach**:

1. **Governance Agent** (Claude Code main instance)
   - Project coordination
   - Quality assurance (SONAR-style)
   - Integration management
   - Quality gate execution

2. **UI Specialist Agent**
   - Design system implementation
   - Component library (Slider, Table, etc.)
   - Dark theme compliance

3. **Frontend/Workflow Agent**
   - 8-Screen workflow implementation
   - State management (Material per Tool!)
   - Expert Mode UI

4. **Backend/Calculation Agent**
   - V2.0 Engine wrapper
   - 10-Phase calculation logic
   - API endpoints

### Agent Communication

All agents commit status reports to `.agent-reports/` directory:
- `STATUS.md` - Current progress
- `TODOS.md` - Task list
- `CHANGES.md` - Change log
- `AUDIT.md` - Quality audit

### Branching Strategy

```
main                    # Production-ready releases (protected)
develop                 # Integration branch
agent/ui-specialist     # UI Agent work
agent/frontend-workflow # Frontend Agent work
agent/backend-calc      # Backend Agent work
```

### Commit Convention

```
[AGENT] TYPE: Short description

- Change details

Agent: <agent-name>
Phase: <phase-number>
Quality Gate: <passed/pending>
```

**Types:** IMPL, TEST, DOCS, AUDIT, STATUS, FIX, REFACTOR

---

## Roadmap to v1.0.0

### Phase 0: Foundation (Days 1-2)
- [x] Project setup
- [ ] V2.0 Engine integration
- [ ] API contracts definition
- [ ] Component interfaces definition

### Phase 1: Core Implementation (Days 3-5)
- [ ] Design system + base components
- [ ] Backend API + V2.0 wrapper
- [ ] 10-Phase calculation logic
- [ ] Basic 6-screen workflow

### Phase 2: Advanced Features (Days 6-8)
- [ ] Tool Coating system (6 types)
- [ ] Surface Quality system (4 levels)
- [ ] Expert Mode (Global Slider + Overrides)
- [ ] SLOT_TROCHOIDAL operation

### Phase 3: Export & Polish (Days 9-10)
- [ ] Fusion 360 export (13 expressions)
- [ ] Smart Preset Detection
- [ ] Mathematical Workbook
- [ ] E2E testing

### Phase 4: Production Ready (Days 11-12)
- [ ] Performance optimization (<100ms)
- [ ] Security audit
- [ ] Documentation complete
- [ ] Deployment setup

**Estimated Timeline:** 12 days to v1.0.0

---

## Architecture Principles

### AP-1: NO-TOUCH Calculation Engine
The V2.0 calculation engine remains **unchanged**. All new features are implemented via wrapper services.

### AP-2: Material Per Tool (NOT Global!)
**Critical:** Material selection is per-tool, not global. This was the fundamental error in V3.x.

### AP-3: Dark Theme Only
Single theme with 3 contrast modes (medium/balanced/high). No light theme.

### AP-4: Zero External UI Libraries
No shadcn/ui, no Material-UI, no external component libraries. Custom components only.

### AP-5: Performance Budget
- Calculation response: <100ms (p95)
- UI render: <16ms (60 FPS)
- Page load: <2s

---

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ --cov=backend --cov-report=html
```

**Coverage Target:** >90%

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

**Coverage Target:** >90%

### E2E Tests
```bash
npm run test:e2e
```

---

## Documentation

- **Architecture:** `/docs/architecture/CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md`
- **Operationalization:** `/docs/architecture/OPERATIONALIZATION_STRATEGY.md`
- **API Docs:** http://localhost:8000/docs (auto-generated by FastAPI)
- **Component Docs:** Storybook (coming in Phase 1)

---

## Contributing

### For Agents
1. Read agent-specific documentation in `/docs/agents/<agent-name>/`
2. Update `.agent-reports/<agent-name>/` after each work session
3. Follow commit convention
4. Run tests before commit
5. Wait for Governance Agent approval at Quality Gates

### Code Quality Standards (Pragmatic KMU!)
- Type safety: 100% (TypeScript/Pydantic)
- Test coverage: >90%
- Code duplication: <5%
- Cyclomatic complexity: <15
- **No over-engineering!** KISS principle.

---

## License

Proprietary - Internal use only

---

## Contact

**Project Lead:** Governance Agent (Claude Code)
**Architecture:** V4.0 Final Consolidated
**Status:** In Development (v0.0.1-alpha → v1.0.0)

---

**Last Updated:** 2025-11-10
**Next Milestone:** Phase 0 Complete (Quality Gate 0)
