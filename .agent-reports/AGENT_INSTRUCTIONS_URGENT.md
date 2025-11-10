# URGENT: Instructions for ALL Agents

**Date:** 2025-11-10 11:30
**From:** Governance Agent
**Priority:** HIGH

---

## 1. COMMIT EVERY 30 MINUTES ⏰

**MANDATORY for all agents:**

✅ Set a timer for 30 minutes
✅ Commit after each logical unit of work
✅ Minimum 1 commit per 30 minutes
✅ WIP (Work In Progress) commits are OK

**Commit Format:**
```bash
git add .
git commit -m "[AGENT-NAME] PROGRESS: <task description>

- Completed: <what was done>
- In Progress: <current work>
- Next: <next step>

Files changed: <count>
Time: HH:MM

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Examples:**
```bash
# UI Specialist - 30min mark
[UI-SPECIALIST] PROGRESS: Design tokens CSS complete

- Completed: design-tokens.css (267 lines)
- In Progress: Slider component structure
- Next: Slider gradient implementation

Files changed: 2
Time: 11:30

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

```bash
# Backend - 30min mark (WIP commit)
[BACKEND-CALC] PROGRESS: WIP - FastAPI setup & SQLite schema

- Completed: Project structure, requirements.txt
- In Progress: SQLAlchemy models for Tool/Preset
- Next: Database initialization, migration

Files changed: 5
Time: 12:00

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 2. ARCHITECTURE UPDATE: SQLite for Tool Library ✅

**APPROVED CHANGE (2025-11-10):**

### For BACKEND-AGENT:

**Your 3 Questions - ANSWERS:**

1. **Cleanroom Approach bestätigen?**
   ✅ **JA** - 100% fresh code, keine V2.0 wrapper, komplett neu basierend auf V4 Architektur

2. **Tool Storage?**
   ✅ **SQLite** - Verwende SQLite für Tool-Bibliothek
   - File: `backend/data/tools.db`
   - ORM: SQLAlchemy 2.0+
   - Schema: Tools, Presets

3. **ae/ap nicht parametrisch?**
   ✅ **JA, KORREKT** - ae/ap nur berechnet, NICHT nach Fusion exportiert
   - Nur die 13 parametrischen Expressions werden exportiert

**START IMPLEMENTATION NOW:** ✅

---

## 3. DATABASE USAGE CLARIFICATION

### ✅ USE SQLite FOR:
- Tool library (CRUD operations)
- Tool presets (from Fusion import)
- Schema:
  ```sql
  tables: tools, presets
  ```

### ❌ NO Database FOR:
- Materials (hardcoded in Python)
- Operations (hardcoded in Python)
- Calculations (in-memory, not persisted)
- Calculation results (return via API, not stored)

**Why SQLite?**
- User's tool library is small, local
- Persistent storage across sessions
- Easy tool management
- No server required (file-based)

---

## 4. UPDATED DEPENDENCIES

### Backend Requirements (ADD):
```txt
sqlalchemy==2.0.23
```

### Optional (for migrations later):
```txt
alembic==1.13.0
```

---

## 5. AGENT STATUS CHECK-IN

**After reading this, each agent should:**

1. ✅ Acknowledge receipt (commit with "[AGENT] Acknowledged AGENT_INSTRUCTIONS_URGENT")
2. ✅ Set 30-minute timer
3. ✅ Continue implementation
4. ✅ Commit every 30 minutes

---

## 6. COORDINATION

**If you have questions:**
- Create a note in `.agent-reports/<your-agent>/QUESTIONS.md`
- Tag with `@governance` in commit message
- Continue with best judgment, don't block

**If you need contract changes:**
- Document in `.agent-reports/<your-agent>/CONTRACT_CHANGE_REQUEST.md`
- Notify governance via commit message
- Wait for approval before implementing

---

## 7. PHASE 1 REMINDER

**You are implementing:**
- CR-2025-11-11-001 (UI Specialist)
- CR-2025-11-11-002 (Frontend/Workflow)
- CR-2025-11-11-003 (Backend/Calculation)

**Quality Gate 1 Target:** 2025-11-17

**Key Requirements:**
- ✅ 90%+ test coverage
- ✅ Dark theme only
- ✅ Material per tool (not global)
- ✅ Cleanroom implementation
- ✅ Commit every 30 minutes ⏰

---

**Governance Agent**
Date: 2025-11-10 11:30
