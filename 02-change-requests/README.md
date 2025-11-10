# 02-change-requests - Change Request Management

Alle Change Requests (CRs) für das Projekt.

---

## Verzeichnisstruktur

```
02-change-requests/
├── README.md           # Diese Datei
├── active/             # Aktive CRs (in Bearbeitung)
├── approved/           # Abgeschlossene & gemergte CRs
└── rejected/           # Abgelehnte CRs (Referenz)
```

---

## Aktive CRs (in Bearbeitung)

### CR-2025-11-11-001 - Design System & Base Components
- **Agent:** ui-specialist
- **Status:** ✅ APPROVED (conditional on UAT)
- **Scope:** 7 Components, Storybook, Design System

### CR-2025-11-11-002 - Frontend Screens & State Management
- **Agent:** frontend-workflow
- **Status:** ✅ APPROVED
- **Scope:** 6 Screens, 5 Zustand Stores, API Client

### CR-2025-11-11-003 - Backend API Setup & Calculation Engine
- **Agent:** backend-calculation
- **Status:** ✅ APPROVED
- **Scope:** 10-Phase Engine, FastAPI, Tests

### CR-2025-11-10-001 - Legacy CR
- **Status:** Superseded by CR-2025-11-11-001

---

## CR Lifecycle

1. **DRAFT** - Governance creates CR
2. **IN_PROGRESS** - Agent implements
3. **TESTING** - Agent runs tests
4. **GOVERNANCE_REVIEW** - Governance reviews
5. **UAT** - User tests
6. **APPROVED** - Ready for merge
7. **MERGED** - Moved to `approved/`

---

## CR Template

Siehe: `docs/change-requests/CR_TEMPLATE.md`

---

**Mehr Infos:** Siehe `../01-dokumentation/OPERATIONALIZATION_STRATEGY.md`
