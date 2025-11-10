# Sprint 1: Foundation (Week 1)

**Dauer:** 2025-11-10 bis 2025-11-17 (7 Tage)
**Ziel:** Phase 0-1 Complete - Development Foundation Ready
**Target Version:** v0.1.0

---

## Sprint Goals

1. ✅ **Setup Complete** - Git, Structure, Architecture (DONE Phase 0)
2. 🎯 **Design System** - UI Components Library
3. 🎯 **Backend Foundation** - FastAPI + Calculation Stubs
4. 🎯 **Frontend Foundation** - React Setup + First Screen

---

## Change Requests (CRs)

### CR-2025-11-10-001: Backend Phase 1 Setup
- **Agent:** backend-calculation
- **Status:** DRAFT
- **Description:** FastAPI application structure, Pydantic models, first calculation stub
- **Story Points:** 5

### CR-2025-11-10-002: Design System Implementation
- **Agent:** ui-specialist
- **Status:** DRAFT
- **Description:** design-tokens.css, Base components (Slider, Table, Button)
- **Story Points:** 8

### CR-2025-11-10-003: Frontend State Management
- **Agent:** frontend-workflow
- **Status:** DRAFT
- **Description:** Zustand store setup, Tool selection state
- **Story Points:** 5

---

## Definition of Done (Sprint 1)

- [ ] Backend läuft auf Port 8000
- [ ] Frontend läuft auf Port 5173
- [ ] Design tokens implementiert (Dark Theme)
- [ ] Slider Component (NO visible thumb!)
- [ ] Table Component (Dark Theme)
- [ ] Tool Selection Screen (basic)
- [ ] API Health Check funktioniert
- [ ] Unit Tests >50% Coverage
- [ ] Smoke Tests für alle Components

---

## Daily Goals

### Tag 1 (Mo): Setup & Kickoff
- Governance: CRs erstellen & zuweisen
- Alle Agents: CRs lesen, Branches checken

### Tag 2-3 (Di-Mi): Design System
- UI Specialist: design-tokens.css + Slider
- Backend: FastAPI Setup

### Tag 4-5 (Do-Fr): First Features
- Frontend: Tool Selection Screen
- Backend: First Calculation Endpoint
- UI: Table Component

### Tag 6 (Sa): Integration
- Governance: Integration Tests
- Alle: Bug Fixes

### Tag 7 (So): Sprint Review
- User UAT
- Sprint Retrospective
- Plan Sprint 2

---

## Risks

- ⚠️ Slider Component komplex (marker-basiert, kein Thumb)
- ⚠️ API Contract muss finalisiert sein (Governance)

---

**Status:** 🚀 READY TO START
**Next:** Governance erstellt CRs in 02-change-requests/active/
