# Antworten für Backend-Agent

**Date:** 2025-11-10 11:45
**From:** Governance Agent
**To:** Backend-Calculation Agent

---

## ✅ DEINE FRAGEN - ALLE BEANTWORTET

### 1. Cleanroom Approach bestätigen?

**✅ JA - 100% Bestätigt**

- Keine V2.0 wrapper
- 100% fresh code
- Basierend auf V4 Architektur (7558 Zeilen)
- Alle 10 Phasen neu implementiert

**Was bedeutet das für dich:**
- Implementiere alle Berechnungen von Grund auf
- Nutze die V4 Architektur als Spezifikation
- Keine alten Code-Fragmente übernehmen
- Frischer, sauberer Code mit modernen Patterns

---

### 2. Tool Storage: JSON-Dateien oder Database?

**✅ SQLite - Verwende SQLite für Tool-Bibliothek**

**ENTSCHEIDUNG (2025-11-10):**
- Tool Library: **SQLite** (`backend/data/tools.db`)
- Materials: **Hardcoded** (Python code)
- Operations: **Hardcoded** (Python code)
- Calculations: **In-Memory** (nicht persistiert)

**Warum SQLite?**
- User's tool library ist klein und lokal
- Persistente Speicherung über Sessions hinweg
- Einfaches Tool-Management (CRUD)
- Standard SQL interface
- Lightweight, kein Server (file-based)

**Database Schema:**
```sql
-- Tools table
CREATE TABLE tools (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    dc REAL NOT NULL,
    lcf REAL NOT NULL,
    dcon REAL NOT NULL,
    oal REAL NOT NULL,
    nof INTEGER NOT NULL,
    ld_ratio REAL NOT NULL,
    ld_classification TEXT NOT NULL
);

-- Presets table
CREATE TABLE presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id TEXT NOT NULL,
    name TEXT NOT NULL,
    material TEXT,
    operation TEXT,
    vc REAL,
    n INTEGER,
    fz REAL,
    vf REAL,
    ae REAL,
    ap REAL,
    FOREIGN KEY (tool_id) REFERENCES tools(id)
);
```

**Dependencies (ADD):**
```txt
sqlalchemy==2.0.23
alembic==1.13.0  # Optional, für Migrations
```

---

### 3. ae/ap nicht parametrisch?

**✅ JA, KORREKT - ae/ap sind NICHT parametrisch**

**Was wird exportiert:**
- ✅ **13 Parametrische Expressions** (vc, n, fz, vf, etc.)
- ✅ Diese werden als Fusion 360 Parameters exportiert

**Was wird NICHT exportiert:**
- ❌ **ae/ap** - Nur berechnet und im UI angezeigt
- ❌ Werden als feste Werte in Tool-Preset gespeichert
- ❌ NICHT als parametrische Expression nach Fusion

**Warum?**
- ae/ap sind operationsspezifisch
- Fusion nutzt sie als Input, nicht als Variable
- User sieht sie im Calculator, aber sie sind nicht editierbar in Fusion

**In Code:**
```python
# Calculation result
result = {
    # Parametric (exportiert nach Fusion)
    "vc_m_min": 150.0,
    "n_rpm": 15915,
    "fz_mm": 0.05,
    "vf_mm_min": 2387,
    # ... 9 weitere parametrische

    # Non-parametric (nur UI display)
    "ae_mm": 7.5,
    "ap_mm": 1.5,
}

# Export
export_to_fusion(
    expressions=["vc", "n", "fz", "vf", ...],  # 13 expressions
    # ae/ap NICHT enthalten
)
```

---

## 🚀 START IMPLEMENTATION

**✅ JA - Starte jetzt mit der Cleanroom-Implementierung!**

**Deine Aufgaben (CR-2025-11-11-003):**
1. FastAPI Projekt Setup
2. SQLAlchemy Models (Tool, Preset)
3. Pydantic Schemas (Tool, Material, Operation)
4. 3 Basic Endpoints:
   - GET /health
   - GET /api/materials (7 materials, hardcoded)
   - GET /api/operations (13 operations, hardcoded)
5. Testing Infrastructure (Pytest)

**Zeitrahmen:** 14-18 Stunden
**Deadline:** 2025-11-17 (Quality Gate 1)

---

## ⏰ WICHTIG: COMMIT EVERY 30 MINUTES

**MANDATORY:**
- Set timer for 30 minutes
- Commit after each logical unit
- WIP commits are OK
- Push to `origin agent/backend-calculation`

**Format:**
```bash
[BACKEND-CALC] PROGRESS: <task>

- Completed: <what was done>
- In Progress: <current work>
- Next: <next step>

Files changed: X
Time: HH:MM
```

---

## 📚 REFERENZEN

**Architecture:**
- `docs/architecture/CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md` (7558 lines)
- Part 2: Domänenmodell & Berechnungslogik
- Part 3: Backend-Architektur

**Contracts:**
- `docs/contracts/API_CONTRACT.md` (643 lines)
- Alle Endpoints, Schemas, Error Handling

**Your CR:**
- `docs/change-requests/active/CR-2025-11-11-003.md` (514 lines)
- UPDATED: SQLite dependency added (2025-11-10)

**Architecture Decision:**
- `.agent-reports/governance/ARCHITECTURE_DECISION_CHANGE.md`
- Warum SQLite, was ist hardcoded, was ist in-memory

---

## 💡 TIPS

**Cleanroom Implementation:**
- Lies V4 Architektur als Spezifikation
- Implementiere von Grund auf
- Nutze moderne Python Patterns (async, type hints)
- 90%+ Test Coverage

**SQLite Setup:**
- Use SQLAlchemy 2.0+ (async support)
- Create `backend/data/` directory
- Initialize DB on first run
- Optional: Alembic for migrations (später)

**Materials & Operations:**
- Hardcode in Python files
- Use Enums (MaterialType, OperationType)
- Data structures from Architecture doc

---

## ✅ CHECKLIST

- [x] Frage 1: Cleanroom? → JA
- [x] Frage 2: Tool Storage? → SQLite
- [x] Frage 3: ae/ap parametrisch? → NEIN
- [x] CR updated with SQLite
- [x] Architecture decision documented
- [x] Start implementation approved

**GO! 🚀**

---

**Governance Agent**
Date: 2025-11-10 11:45
