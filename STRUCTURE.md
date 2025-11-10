# CNC-ToolCalc - Detaillierte Verzeichnisstruktur

**Für:** Benutzer & Agents
**Ziel:** Schnelles Auffinden aller Projekt-Ressourcen

---

## Root-Ebene (minimal!)

```
CNC-ToolCalc/
├── README.md                # Projekt-Übersicht & Quick Start
├── STRUCTURE.md            # Diese Datei (Wo finde ich was?)
├── cnc-toolcalc.sh        # Start-Script für Anwendung
└── VERSION.txt             # Aktuelle Version
```

---

## 01-dokumentation/ - Architektur & Benutzerdoku (Deutsch)

```
01-dokumentation/
├── ARCHITECTURE.md              # V4 Architektur (komplett, ~7500 Zeilen)
├── OPERATIONALIZATION.md        # Multi-Agent Strategie
├── BENUTZERHANDBUCH_DE.md       # Bedienungsanleitung (Deutsch)
├── API_DOKUMENTATION.md         # API Endpoints & Schemas
├── COMPONENT_LIBRARY.md         # UI Komponenten-Doku
└── GLOSSAR.md                   # Fachbegriffe erklärt
```

**Wer nutzt das:**
- User: Benutzerhandbuch
- Agents: Architektur, API, Components
- Governance: Alle Dokumente

---

## 02-change-requests/ - Change Request Management

```
02-change-requests/
├── CR_TEMPLATE.md               # Template für neue CRs
├── CHANGELOG.md                 # Version History
├── active/                      # Aktive CRs (in Bearbeitung)
│   ├── CR-2025-11-10-001.md    # Backend: Phase 1 Setup
│   └── CR-2025-11-10-002.md    # UI: Design System
├── approved/                    # Abgeschlossene & gemergte CRs
│   └── CR-2025-11-09-001.md
└── rejected/                    # Abgelehnte CRs (zur Referenz)
    └── CR-2025-11-08-001.md
```

**Wer nutzt das:**
- Governance: Erstellt, reviewt, merged CRs
- Agents: Lesen zugewiesene CRs, implementieren, updaten Status
- User: Liest CR für UAT, gibt Feedback

**Workflow:**
1. Governance erstellt CR in `active/`
2. Agent implementiert & updatet CR
3. Nach UAT PASSED → Governance moved to `approved/`

---

## 03-development/ - Code & Git Repository

```
03-development/
├── backend/                     # FastAPI Backend
│   ├── calculation/            # 10-Phasen Logik (100% cleanroom!)
│   ├── api/                    # FastAPI Routes
│   ├── models/                 # Pydantic Models
│   ├── services/               # Business Logic Services
│   └── tests/                  # Backend Tests
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── screens/           # 8 Screens
│   │   ├── components/        # UI Components
│   │   ├── state/             # Zustand Store
│   │   └── api/               # API Client
│   └── tests/                  # Frontend Tests
├── scripts/                     # Build, Test, Quality Gate Scripts
├── .git/                        # Git Repository
├── package.json                 # Root Workspace Config
└── README.md                    # Development README
```

**Wer nutzt das:**
- Agents: Schreiben Code hier
- Governance: Reviewt Code, merged Branches
- User: Startet Anwendung von hier

**Git Branches:**
- `main`: Production
- `develop`: Integration
- `agent/ui-specialist`
- `agent/frontend-workflow`
- `agent/backend-calculation`

---

## 04-finale-version/ - Production Builds

```
04-finale-version/
├── v1.0.0/                      # Production Release v1.0.0
│   ├── cnc-toolcalc-v1.0.0.tar.gz
│   ├── RELEASE_NOTES.md
│   └── INSTALLATION.md
├── v0.5.0/                      # Beta Release
└── latest -> v1.0.0/            # Symlink to latest
```

**Wer nutzt das:**
- User: Download & Installation
- Governance: Erstellt nach Release

---

## 05-audits/ - Quality Audits & Test Reports

```
05-audits/
├── code-quality/
│   ├── 2025-11-10-phase-1.md   # Code Quality Audit Phase 1
│   └── 2025-11-15-phase-2.md
├── security/
│   ├── 2025-11-20-security-audit.md
│   └── 2025-11-21-penetration-test.md
├── performance/
│   ├── 2025-11-22-load-test.md
│   └── 2025-11-22-calculation-benchmark.md
└── smoke-tests/
    ├── smoke-test-cr-001.log
    └── smoke-test-cr-002.log
```

**Wer nutzt das:**
- Agents: Dokumentieren Audit-Ergebnisse
- Governance: Reviewt Audits, validiert Quality Gates
- User: Liest bei Interesse

---

## 06-sprints/ - Sprint-Planung & Meilensteine

```
06-sprints/
├── MASTERPLAN.md                # Gesamt-Roadmap v0.0.1 → v1.0.0
├── SPRINT_01.md                 # Week 1: Foundation
├── SPRINT_02.md                 # Week 2: Calculation Core
├── SPRINT_03.md                 # Week 3: Frontend Workflow
├── SPRINT_04.md                 # Week 4: Export & Polish
├── SPRINT_BOARD.md              # Aktueller Sprint Status
└── RETROSPECTIVE.md             # Sprint Retrospectives
```

**Wer nutzt das:**
- Governance: Erstellt Sprint-Pläne, updatet Board
- Agents: Lesen Sprint-Pläne, arbeiten Tasks ab
- User: Sieht Fortschritt

**Sprint-Struktur:**
- Sprint 1 (Week 1): Phase 0-1 Foundation
- Sprint 2 (Week 2): Phase 2 Calculation Core
- Sprint 3 (Week 3): Phase 3 Frontend
- Sprint 4 (Week 4): Phase 4-5 Export & Polish

---

## 07-agent-reports/ - Agent Status & Kommunikation

```
07-agent-reports/
├── governance/
│   ├── STATUS.md                # Aktueller Status
│   ├── TODOS.md                 # Governance TODOs
│   ├── DECISIONS.md             # Architektur-Entscheidungen
│   └── PRIORITIES.md            # Tages-Prioritäten für Agents
├── ui-specialist/
│   ├── STATUS.md
│   ├── TODOS.md
│   ├── CHANGES.md               # Change Log
│   └── AUDIT.md                 # Self-Audit
├── frontend-workflow/
│   ├── STATUS.md
│   ├── TODOS.md
│   ├── CHANGES.md
│   └── AUDIT.md
└── backend-calculation/
    ├── STATUS.md
    ├── TODOS.md
    ├── CHANGES.md
    └── AUDIT.md
```

**Wer nutzt das:**
- Agents: Updaten eigene Reports nach jedem Task
- Governance: Liest alle Reports, koordiniert Agents
- User: Sieht Fortschritt

**Daily Workflow:**
- Morgens: Agent liest `governance/PRIORITIES.md`
- Tagsüber: Agent updated `<agent>/STATUS.md`, `CHANGES.md`
- Abends: Agent commitet Updates → Governance reviewt

---

## 08-claude-prompts/ - Agent Start-Prompts

```
08-claude-prompts/
├── 01-governance-agent.md       # Governance Start-Prompt
├── 02-ui-specialist-agent.md    # UI Agent Start-Prompt
├── 03-frontend-workflow-agent.md
├── 04-backend-calculation-agent.md
└── PROMPT_TEMPLATE.md           # Template für neue Agent-Prompts
```

**Wer nutzt das:**
- User: Startet neue Claude Sessions mit diesen Prompts
- Agents: Lesen bei Session-Start

**Wie verwenden:**
1. Neue Claude Code Session öffnen
2. Prompt kopieren (z.B. `01-governance-agent.md`)
3. In Claude einfügen → Session startet mit Rolle & Context

**Prompt-Struktur:**
- Rolle & Zuständigkeiten
- Context (Architektur, API Contracts, etc.)
- Autonomie-Modus (aus CONTROL_PROMPT_TEMPLATE)
- Workflow & Kommunikation
- Tools & Commands

---

## 09-user-feedback/ - UAT & User Feedback

```
09-user-feedback/
├── uat-reports/
│   ├── uat-cr-001.md            # UAT für CR-001
│   ├── uat-cr-002.md
│   └── uat-summary.md           # Gesamtübersicht
├── feature-requests/
│   ├── request-001.md           # User Feature Request
│   └── request-002.md
├── bug-reports/
│   ├── bug-001.md               # User Bug Reports
│   └── bug-002.md
└── general-feedback.md          # Allgemeines Feedback
```

**Wer nutzt das:**
- User: Dokumentiert UAT-Ergebnisse, Bugs, Feature Requests
- Governance: Liest Feedback, erstellt CRs basierend darauf
- Agents: Lesen Bug Reports, fixen Issues

**UAT Workflow:**
1. Governance notifiziert User: "CR-XXX ready for UAT"
2. User testet Feature, dokumentiert in `uat-reports/uat-cr-xxx.md`
3. User Status: PASSED / FAILED (mit Details)
4. Governance liest Report → merged oder assigned fixes

---

## Symlinks & Connections

```
03-development/backend    → ../backend          # Git Repo Backend
03-development/frontend   → ../frontend         # Git Repo Frontend
03-development/.git       → ../.git            # Git Root

01-dokumentation/docs     → ../docs            # Docs aus Git Repo
```

Diese Symlinks verknüpfen die nummerierte Struktur mit dem Git Repository.

---

## Wichtige Dateipfade (Quick Reference)

| Was suche ich? | Wo finde ich es? |
|----------------|------------------|
| **Architektur** | `01-dokumentation/ARCHITECTURE.md` |
| **Benutzerhandbuch** | `01-dokumentation/BENUTZERHANDBUCH_DE.md` |
| **Aktueller Sprint** | `06-sprints/SPRINT_BOARD.md` |
| **Meine CRs (Agent)** | `07-agent-reports/<agent>/TODOS.md` |
| **CR Template** | `02-change-requests/CR_TEMPLATE.md` |
| **Agent Prompt starten** | `08-claude-prompts/0X-<agent>-agent.md` |
| **UAT durchführen** | `09-user-feedback/uat-reports/` |
| **Code schreiben** | `03-development/backend/` oder `/frontend/` |
| **Tests laufen** | `03-development/scripts/` |
| **Production Build** | `04-finale-version/latest/` |

---

## Datei-Naming Conventions

### Change Requests
```
CR-YYYY-MM-DD-NNN.md
Beispiel: CR-2025-11-10-001.md
```

### Agent Reports
```
<agent-name>/STATUS.md
<agent-name>/TODOS.md
<agent-name>/CHANGES.md
<agent-name>/AUDIT.md
```

### Audits
```
<category>/YYYY-MM-DD-<description>.md
Beispiel: code-quality/2025-11-10-phase-1.md
```

### UAT Reports
```
uat-cr-<cr-number>.md
Beispiel: uat-cr-001.md
```

---

## Git Integration

**Git Repository:** `/Users/nwt/developments/CNC-ToolCalc/.git`
**GitHub:** https://github.com/VoHoch/CNC-ToolCalc

**Was wird getrackt:**
- ✅ `03-development/` (Code)
- ✅ `01-dokumentation/` (Docs)
- ✅ `02-change-requests/` (CRs)
- ✅ `06-sprints/` (Sprint-Pläne)
- ✅ `07-agent-reports/` (Agent Status)
- ✅ `08-claude-prompts/` (Prompts)
- ❌ `04-finale-version/` (Production Builds - zu groß)
- ❌ `05-audits/` (Audit Logs - optional)
- ❌ `09-user-feedback/` (User Feedback - lokal)

---

**Letzte Aktualisierung:** 2025-11-10
**Version:** v0.0.1-alpha
**Status:** Initial Setup Complete
