# 🔥 INSTRUCTION für alle Agents: Smoke Tests ausführen

**Date:** 2025-11-10
**Priority:** 🚨 **URGENT**
**Deadline:** HEUTE (vor 18:00)

---

## 📋 AN ALLE AGENTS

**backend-calculation, frontend-workflow, ui-specialist:**

Ihr habt jeweils eine **URGENT_SMOKE_TEST_TASK.md** auf eurem Branch erhalten.

**Location:**
- Backend: `.agent-reports/backend-calculation/URGENT_SMOKE_TEST_TASK.md`
- Frontend: `.agent-reports/frontend-workflow/URGENT_SMOKE_TEST_TASK.md`
- UI: `.agent-reports/ui-specialist/URGENT_SMOKE_TEST_TASK.md`

---

## 🎯 EURE AUFGABE

1. **Lest** eure URGENT_SMOKE_TEST_TASK.md
2. **Erstellt** die Smoke Test Scripts (wie in der Task beschrieben)
3. **Führt** die Smoke Tests aus
4. **Erstellt** einen SMOKE_TEST_REPORT.md
5. **Committed & pusht** alles

**Timeline:** 30-45 Minuten pro Agent

---

## 🤖 FÜR BACKEND-CALCULATION AGENT

**Aufgabe:**
```bash
# 1. Lese Task
cat .agent-reports/backend-calculation/URGENT_SMOKE_TEST_TASK.md

# 2. Erstelle backend/smoke_test.py
# (siehe URGENT_SMOKE_TEST_TASK.md für vollständiges Script)

# 3. Ausführen
python backend/smoke_test.py

# 4. Report erstellen
vi .agent-reports/backend-calculation/SMOKE_TEST_REPORT.md

# 5. Commit
git add backend/smoke_test.py .agent-reports/backend-calculation/SMOKE_TEST_REPORT.md
git commit -m "[BACKEND] Add smoke test + report - READY FOR INTEGRATION"
git push origin agent/backend-calculation
```

**Erwartetes Ergebnis:**
- ✅ 5/5 Checks PASS
- ✅ Server startet
- ✅ Alle Endpoints funktionieren
- ✅ 10-Phase Engine arbeitet korrekt

---

## 🖥️ FÜR FRONTEND-WORKFLOW AGENT

**Aufgabe:**
```bash
# 1. Lese Task
cat .agent-reports/frontend-workflow/URGENT_SMOKE_TEST_TASK.md

# 2. Erstelle frontend/smoke-test.sh
# (siehe URGENT_SMOKE_TEST_TASK.md für vollständiges Script)

# 3. Erstelle frontend/src/__tests__/smoke.test.tsx

# 4. Ausführen
cd frontend
./smoke-test.sh

# 5. Report erstellen
vi .agent-reports/frontend-workflow/SMOKE_TEST_REPORT.md

# 6. Commit
git add frontend/smoke-test.sh frontend/src/__tests__/ .agent-reports/frontend-workflow/SMOKE_TEST_REPORT.md
git commit -m "[FRONTEND] Add smoke test + report - READY FOR INTEGRATION"
git push origin agent/frontend-workflow
```

**Erwartetes Ergebnis:**
- ✅ 4/4 Checks PASS
- ✅ TypeScript kompiliert ohne Fehler
- ✅ Production Build erfolgreich
- ✅ Dev Server startet

---

## 🎨 FÜR UI-SPECIALIST AGENT

**Aufgabe:**
```bash
# 1. Lese Task
cat .agent-reports/ui-specialist/URGENT_SMOKE_TEST_TASK.md

# 2. Erstelle frontend/smoke-test-storybook.sh
# (siehe URGENT_SMOKE_TEST_TASK.md für vollständiges Script)

# 3. Erstelle frontend/verify-components.sh

# 4. Ausführen
cd frontend
./smoke-test-storybook.sh

# 5. Report erstellen
vi .agent-reports/ui-specialist/SMOKE_TEST_REPORT.md

# 6. Commit
git add frontend/smoke-test-storybook.sh frontend/verify-components.sh .agent-reports/ui-specialist/SMOKE_TEST_REPORT.md
git commit -m "[UI] Add smoke test + report - READY FOR INTEGRATION"
git push origin agent/ui-specialist
```

**Erwartetes Ergebnis:**
- ✅ 5/5 Checks PASS
- ✅ Storybook baut ohne Fehler
- ✅ Alle 7 Components vorhanden
- ✅ **Slider NO visible thumb** verified

---

## ✅ SUCCESS CRITERIA

**Jeder Agent muss liefern:**

1. **Smoke Test Script** erstellt
2. **Smoke Test ausgeführt** (alle Checks PASS)
3. **SMOKE_TEST_REPORT.md** erstellt
4. **Committed & pushed**

**Governance Review:** Morgen (2025-11-11) 09:00

---

## 🚨 WENN TESTS FEHLSCHLAGEN

**Falls Smoke Test fehlschlägt:**

1. **Identifiziere** das Problem (welcher Check failed?)
2. **Fixe** den Code
3. **Führe Test erneut aus** (bis PASS)
4. **Dokumentiere** Fix im Report
5. **Commit** mit Details

**Format:**
```bash
git commit -m "[AGENT] Fix: <problem>

Issue: Smoke test failed at check X
Root Cause: <reason>
Fix: <what you did>
Status: ✅ Smoke test now PASS

Time: $(date +%H:%M)"
```

---

## ⏰ DEADLINE

**HEUTE (2025-11-10) vor 18:00**

Integration Day ist MORGEN. Ohne Smoke Tests können wir nicht mergen!

---

**Created:** 2025-11-10
**By:** Governance Agent
**For:** All agents (backend-calculation, frontend-workflow, ui-specialist)
