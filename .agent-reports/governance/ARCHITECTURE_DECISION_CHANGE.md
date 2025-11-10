# Architecture Decision Change: Tool Database

**Date:** 2025-11-10
**Decision By:** User (Volker)
**Status:** APPROVED
**Impact:** Backend Implementation

---

## CHANGE SUMMARY

**Original Decision (Phase 0):**
- NO Database (in-memory only)
- Tool libraries as JSON files

**NEW Decision (Phase 1):**
- ✅ **SQLite for Tool Library** (approved 2025-11-10)
- Small, local database for tool import/export
- Persistent storage for tool library

---

## RATIONALE

User decision: "Ich denke SQL light für meine kleine bibliothek aus. OK?"

**Benefits:**
- Persistent tool library across sessions
- Better query capabilities for tool lookup
- Easier tool management (add/edit/delete)
- Standard SQL interface
- Lightweight, no server required (file-based)

**Trade-offs:**
- Adds SQLite dependency
- Need database schema migration
- Slightly more complex setup

---

## UPDATED ARCHITECTURE

### Database Usage

**SQLite:**
- ✅ Tool library storage (tools, presets)
- Schema: Tools, ToolGeometry, Presets
- File: `backend/data/tools.db`

**NO Database:**
- ❌ Materials (hardcoded in code)
- ❌ Operations (hardcoded in code)
- ❌ Calculations (in-memory only)
- ❌ Results (not persisted)

### Backend Stack UPDATE

**Before:**
```python
# No database
# All data in Python data structures
MATERIALS = [...]
OPERATIONS = [...]
```

**After:**
```python
# SQLite for tools only
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data/tools.db')

# Materials & Operations still hardcoded
MATERIALS = [...]
OPERATIONS = [...]
```

---

## BACKEND-AGENT CONFIRMATION

**Questions from Backend-Agent:**

1. **Cleanroom Approach bestätigen?**
   ✅ **JA** - 100% fresh code, keine V2.0 wrapper

2. **Tool Storage?**
   ✅ **SQLite** - Verwende SQLite für Tool-Bibliothek
   - File: `backend/data/tools.db`
   - ORM: SQLAlchemy (recommended)
   - Migrations: Alembic (optional for now)

3. **ae/ap nicht parametrisch?**
   ✅ **JA, KORREKT** - ae/ap nur berechnet, nicht exportiert

**Start Implementation:** ✅ JA, starte jetzt mit Cleanroom-Implementierung

---

## IMPLEMENTATION DETAILS

### Database Schema (SQLite)

```sql
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
    ld_classification TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

### Python Models (SQLAlchemy)

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class ToolDB(Base):
    __tablename__ = "tools"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    dc: Mapped[float]
    lcf: Mapped[float]
    dcon: Mapped[float]
    oal: Mapped[float]
    nof: Mapped[int]
    ld_ratio: Mapped[float]
    ld_classification: Mapped[str]

class PresetDB(Base):
    __tablename__ = "presets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tool_id: Mapped[str] = mapped_column(ForeignKey("tools.id"))
    name: Mapped[str]
    material: Mapped[str | None]
    operation: Mapped[str | None]
    vc: Mapped[float | None]
    n: Mapped[int | None]
    fz: Mapped[float | None]
    vf: Mapped[float | None]
    ae: Mapped[float | None]
    ap: Mapped[float | None]
```

---

## DEPENDENCIES UPDATE

### Backend Requirements (NEW)

```txt
# Add to backend/requirements.txt
sqlalchemy==2.0.23
alembic==1.13.0  # Optional: for migrations
```

---

## COMMIT REMINDER STRATEGY

### 30-Minute Commit Rule

**All agents MUST commit every 30 minutes during implementation.**

**Commit Format:**
```bash
git add .
git commit -m "[AGENT-NAME] PROGRESS: <what was done>

- Task 1 completed
- Task 2 in progress
- X files changed

Time: HH:MM
Next: <what's next>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Reminder in each CR:**
- Set timer for 30 minutes
- Commit after each logical unit of work
- Minimum 1 commit per 30 minutes
- Even if work is incomplete (WIP commits ok)

---

## UPDATED CHANGE REQUESTS

### CR-2025-11-11-003 (Backend) - UPDATE REQUIRED

**Section to update:**
```markdown
## Dependencies (UPDATED)

**backend/requirements.txt:**
```
fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
sqlalchemy==2.0.23        # NEW: For tool database
```
```

**Architecture Compliance:**
```markdown
- [x] SQLite for tool library ✓
- [x] NO Database for materials/operations (hardcoded)
- [x] NO Database for calculations (in-memory)
```

---

## COMMUNICATION TO AGENTS

### Message to Backend-Agent:

```
✅ BESTÄTIGUNG:

1. Cleanroom Approach: JA - 100% fresh code, keine V2.0 wrapper
2. Tool Storage: SQLite (backend/data/tools.db)
3. ae/ap nicht parametrisch: JA, KORREKT

START IMPLEMENTATION: ✅

Zusätzlich:
- Materials/Operations: Hardcoded (kein DB)
- Calculations: In-memory (kein DB)
- Nur Tools & Presets in SQLite

COMMIT-REGEL: Alle 30 Minuten committen!
```

### Message to ALL Agents:

```
📢 WICHTIG: COMMIT-REGEL

Alle 30 Minuten committen!

Format:
[AGENT-NAME] PROGRESS: <task>
- Was wurde gemacht
- Was ist nächster Schritt
Time: HH:MM

Auch WIP-Commits sind OK!
```

---

## SIGN-OFF

**Decision:** ✅ APPROVED
**By:** User (Volker)
**Date:** 2025-11-10
**Governance:** Documented & communicated

**Impact Assessment:**
- Low risk: SQLite is lightweight
- Well-supported library (SQLAlchemy)
- Easy to rollback if needed
- Does not affect frontend or calculation logic

---

**Last Updated:** 2025-11-10 11:30
**Next Review:** After Phase 1 implementation
