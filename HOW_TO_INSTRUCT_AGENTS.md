# 🤖 How to Instruct Agents: Smoke Tests ausführen

**Date:** 2025-11-10
**Task:** Smoke Tests für alle 3 Agents
**Priority:** 🚨 URGENT
**Deadline:** HEUTE (vor 18:00)

---

## ✅ WAS BEREITS GEMACHT WURDE

**Governance hat bereits:**

1. ✅ **URGENT_SMOKE_TEST_TASK.md** auf jedem agent branch erstellt:
   - `agent/backend-calculation/.agent-reports/backend-calculation/URGENT_SMOKE_TEST_TASK.md`
   - `agent/frontend-workflow/.agent-reports/frontend-workflow/URGENT_SMOKE_TEST_TASK.md`
   - `agent/ui-specialist/.agent-reports/ui-specialist/URGENT_SMOKE_TEST_TASK.md`

2. ✅ **Committed & pushed** zu GitHub

3. ✅ **Instruction Document** erstellt:
   - `08-claude-prompts/RUN_SMOKE_TESTS_INSTRUCTION.md`

4. ✅ **Check Script** erstellt:
   - `scripts/check-smoke-tests.sh`

**Die Agents MÜSSEN NUR NOCH ihre Task-Files lesen und ausführen!**

---

## 🎯 DEINE OPTIONEN (als User)

### **Option 1: Automatisch (via neue Claude Sessions)** ⭐ EMPFOHLEN

**Starte für jeden Agent eine neue Claude Session:**

#### Backend Agent:

```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/02-backend-calculation-agent.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

WICHTIG: Lies zuerst deine URGENT_SMOKE_TEST_TASK.md:
.agent-reports/backend-calculation/URGENT_SMOKE_TEST_TASK.md

Führe die Smoke Tests aus wie beschrieben. Deadline: HEUTE 18:00.
```

#### Frontend Agent:

```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/03-frontend-workflow-agent.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

WICHTIG: Lies zuerst deine URGENT_SMOKE_TEST_TASK.md:
.agent-reports/frontend-workflow/URGENT_SMOKE_TEST_TASK.md

Führe die Smoke Tests aus wie beschrieben. Deadline: HEUTE 18:00.
```

#### UI Agent:

```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/04-ui-specialist-agent.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

WICHTIG: Lies zuerst deine URGENT_SMOKE_TEST_TASK.md:
.agent-reports/ui-specialist/URGENT_SMOKE_TEST_TASK.md

Führe die Smoke Tests aus wie beschrieben. Deadline: HEUTE 18:00.
```

---

### **Option 2: Via GitHub (wenn Agents ihre Branches checken)**

**Die Agents sehen automatisch:**

Wenn ein Agent zu seinem Branch wechselt (`git checkout agent/backend-calculation`), wird er die neue Datei sehen:

```
.agent-reports/backend-calculation/URGENT_SMOKE_TEST_TASK.md (NEU!)
```

Jeder Agent sollte bei der nächsten Session automatisch diese Datei lesen und die Aufgabe ausführen.

---

### **Option 3: Zentrale Instruction (für alle gleichzeitig)**

**Erstelle eine neue Claude Session (Governance):**

```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/RUN_SMOKE_TESTS_INSTRUCTION.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

Koordiniere alle 3 Agents um ihre Smoke Tests auszuführen:
- backend-calculation
- frontend-workflow
- ui-specialist

Deadline: HEUTE 18:00
```

**Governance startet dann parallel 3 Task Agents für Backend/Frontend/UI.**

---

## 🔍 STATUS PRÜFEN

**Jederzeit Status checken:**

```bash
cd /Users/nwt/developments/cnc-toolcalc

# Check smoke test status
./scripts/check-smoke-tests.sh

# Output:
# 🔥 Smoke Test Status Check
# ---
# 🤖 Agent: backend-calculation
#    ✅ Task assigned
#    ⚠️  Report not yet created (still working...)
#
# 🤖 Agent: frontend-workflow
#    ✅ Task assigned
#    ⚠️  Report not yet created (still working...)
#
# 🤖 Agent: ui-specialist
#    ✅ Task assigned
#    ⚠️  Report not yet created (still working...)
#
# Summary:
# ⚠️  MISSING: 3 / 3
# ⏰ Deadline: Today before 18:00
```

---

## 📊 MONITORING

**Option A: Check Script (lokal):**

```bash
# Status check
./scripts/check-smoke-tests.sh

# Activity report
./scripts/show-activity.sh
```

**Option B: GitHub (web):**

```
1. Gehe zu https://github.com/VoHoch/CNC-ToolCalc/commits
2. Dropdown: "All branches"
3. Suche nach commits: "[BACKEND] Add smoke test"
```

**Option C: Lokal Git:**

```bash
# Alle commits heute
git log --all --since="today" --oneline --grep="smoke"

# Zu agent branch wechseln und Report lesen
git checkout agent/backend-calculation
cat .agent-reports/backend-calculation/SMOKE_TEST_REPORT.md
git checkout main
```

---

## ❓ FAQ

### "Muss ich die Agent Prompts anpassen?"

**NEIN!** Die URGENT_SMOKE_TEST_TASK.md Files sind bereits auf den agent branches committed. Die Agents werden diese automatisch sehen.

### "Ist der Smoke Test als Change Request hinterlegt?"

**NEIN**, es ist eine **URGENT TASK**, keine Change Request. Es ist eine kleine Ergänzung zu bestehenden CRs:
- CR-2025-11-11-001 (UI) → Ergänzung: Smoke Test
- CR-2025-11-11-002 (Frontend) → Ergänzung: Smoke Test
- CR-2025-11-11-003 (Backend) → Ergänzung: Smoke Test

### "Kann ich das automatisch anstoßen?"

**Teilweise:**
- ✅ Status Check: `./scripts/check-smoke-tests.sh` (automatisch)
- ✅ Activity Monitor: `./scripts/show-activity.sh` (automatisch)
- ❌ Agent Ausführung: Du musst Claude Sessions starten (manuell)

**Zukünftig:** Könnte man mit GitHub Actions automatisieren (CI/CD Pipeline).

### "Wie weiß ich wenn ein Agent fertig ist?"

**3 Wege:**

1. **Check Script:**
   ```bash
   ./scripts/check-smoke-tests.sh
   # Zeigt: ✅ PASSED: 1/3 (wenn Backend fertig)
   ```

2. **GitHub Commits:**
   ```
   Commits → All branches → Suche: "[BACKEND] Add smoke test"
   ```

3. **Agent Branch check:**
   ```bash
   git fetch --all
   git checkout agent/backend-calculation
   ls -la .agent-reports/backend-calculation/SMOKE_TEST_REPORT.md
   # Wenn existiert → fertig!
   ```

---

## 🎯 ZUSAMMENFASSUNG

**Was du tun musst:**

1. **Starte 3 Claude Sessions** (eine pro Agent)
   - Verwende die Prompts oben (Option 1)
   - Oder: Starte 1 Governance Session die alle 3 koordiniert (Option 3)

2. **Warte 30-45 Minuten** (Agents arbeiten parallel)

3. **Check Status:**
   ```bash
   ./scripts/check-smoke-tests.sh
   ```

4. **Wenn alle PASSED:**
   ```
   🎉 Ready für Integration Day (morgen)!
   ```

**Alle Files sind bereits erstellt und committed:**
- ✅ URGENT_SMOKE_TEST_TASK.md (auf allen agent branches)
- ✅ RUN_SMOKE_TESTS_INSTRUCTION.md (zentrale Instruction)
- ✅ check-smoke-tests.sh (Status Script)
- ✅ show-activity.sh (Activity Script)

**Agents müssen nur noch ihre Tasks ausführen!**

---

**Created:** 2025-11-10
**By:** Governance Agent
**For:** Project Owner (User)
