# 📊 User Guide: Projekt Monitoring & Navigation

**Date:** 2025-11-10
**Version:** 1.0
**Audience:** Project Owner (User)

---

## 🎯 DAS PROBLEM

**Du sagst:**
- Lokal siehst du Verzeichnisse 01-09 ✅
- Auf GitHub siehst du diese auch ✅
- Aber im Sprint Board siehst du nicht den aktuellen Stand ❌
- Du möchtest einen Change Log sehen ❓

**GRUND:** Die aktuelle Implementierung ist auf **Agent Branches**, nicht auf `main`!

---

## 🌳 GIT BRANCH STRUKTUR (WICHTIG!)

```
main ← Du bist hier (nur Infrastructure)
├── 01-dokumentation/      ← ✅ Sichtbar
├── 02-change-requests/    ← ✅ Sichtbar
├── 06-sprints/            ← ✅ Sichtbar, aber...
│   └── SPRINT_BOARD.md    ← ⚠️ Stand von gestern!
└── .agent-reports/governance/ ← ✅ Sichtbar

agent/backend-calculation ← Code hier! (noch nicht gemerged)
├── backend/main.py
├── backend/calculation/engine.py
└── .agent-reports/backend-calculation/ ← Updates hier!

agent/frontend-workflow ← Code hier! (noch nicht gemerged)
├── frontend/src/screens/
└── .agent-reports/frontend-workflow/ ← Updates hier!

agent/ui-specialist ← Code hier! (noch nicht gemerged)
├── frontend/src/components/ui/
└── .agent-reports/ui-specialist/ ← Updates hier!
```

---

## 📂 WO FINDE ICH WAS?

### Auf GitHub (Web)

**1. Aktuellen Branch wechseln:**

```
1. Gehe zu https://github.com/VoHoch/CNC-ToolCalc
2. Klicke auf "main" Dropdown (oben links)
3. Wähle Branch:
   - agent/backend-calculation
   - agent/frontend-workflow
   - agent/ui-specialist
```

**2. Sprint Board auf agent branch sehen:**

```
URL: https://github.com/VoHoch/CNC-ToolCalc/blob/agent/ui-specialist/06-sprints/SPRINT_BOARD.md

Branch wählen: agent/ui-specialist (oder frontend/backend)
Dann: 06-sprints/SPRINT_BOARD.md öffnen
```

**3. Change Log / Activity Feed:**

```
Optionen:

A) Commits anzeigen (alle Branches):
   https://github.com/VoHoch/CNC-ToolCalc/commits
   → Dropdown: "All branches" wählen

B) Network Graph (visualisiert):
   https://github.com/VoHoch/CNC-ToolCalc/network
   → Zeigt alle Branches und Commits

C) Insights → Pulse:
   https://github.com/VoHoch/CNC-ToolCalc/pulse
   → Aktivität der letzten Woche

D) Compare Branches:
   https://github.com/VoHoch/CNC-ToolCalc/compare/main...agent/ui-specialist
   → Zeigt Unterschiede zwischen main und agent branch
```

---

### Lokal (Terminal)

**1. Zwischen Branches wechseln:**

```bash
# Aktuellen Branch sehen
git branch

# Zu agent branch wechseln
git checkout agent/backend-calculation
git checkout agent/frontend-workflow
git checkout agent/ui-specialist

# Zurück zu main
git checkout main
```

**2. Sprint Board auf agent branch lesen:**

```bash
# Zu agent branch wechseln
git checkout agent/ui-specialist

# Sprint Board lesen
cat 06-sprints/SPRINT_BOARD.md

# Oder mit Pager
less 06-sprints/SPRINT_BOARD.md

# Zurück zu main
git checkout main
```

**3. Change Log erstellen:**

```bash
# Alle Commits heute (alle Branches)
git log --all --since="today" --oneline --graph

# Detailliert mit Author und Date
git log --all --since="today" --pretty=format:"%h %an %ad %s" --date=short

# Nur specific agent
git log agent/backend-calculation --oneline --since="today"

# Alle veränderten Dateien heute
git log --all --since="today" --name-only --pretty=format:"" | sort | uniq

# Statistik
git log --all --since="today" --stat
```

---

## 🔍 BEISPIEL: Monitoring Session

**Szenario:** Du willst sehen was die Agents heute gemacht haben.

### Option A: GitHub Web (einfach)

```
1. Gehe zu https://github.com/VoHoch/CNC-ToolCalc/commits

2. Klicke "All branches" Dropdown

3. Siehst du jetzt ALLE Commits:
   [BACKEND] Add smoke test
   [FRONTEND] Add smoke test
   [UI] Add smoke test
   [GOVERNANCE] Status Report
   etc.

4. Klicke auf einen Commit → siehst du Details + Files changed
```

### Option B: Lokal (Terminal)

```bash
cd /Users/nwt/developments/cnc-toolcalc

# 1. Update von GitHub holen
git fetch --all

# 2. Alle Commits seit heute anzeigen
git log --all --since="today" --graph --oneline --decorate

# Output:
* b9b69da (agent/ui-specialist) [GOVERNANCE] URGENT: UI smoke test task assigned
* a5493ce (agent/frontend-workflow) [GOVERNANCE] URGENT: Frontend smoke test
* a02489f (agent/backend-calculation) [GOVERNANCE] URGENT: Backend smoke test
* 047e43c (main) [GOVERNANCE] Status Report 2025-11-10
* 3e3bfa5 [GOVERNANCE] Add project instructions to .claude/CLAUDE.md

# 3. Zu einem Agent branch wechseln um Code zu sehen
git checkout agent/backend-calculation

# 4. Sprint Board lesen (auf diesem branch)
cat 06-sprints/SPRINT_BOARD.md

# 5. Agent Report lesen
cat .agent-reports/backend-calculation/URGENT_SMOKE_TEST_TASK.md

# 6. Zurück zu main
git checkout main
```

---

## 📋 CHANGE LOG SCRIPT (AUTOMATISCH)

**Ich erstelle dir ein Script:**

`scripts/show-activity.sh`

```bash
#!/bin/bash
# Show Project Activity (alle Branches)

echo "============================================================"
echo "📊 CNC-ToolCalc Project Activity"
echo "============================================================"
echo ""

# Update from remote
echo "🔄 Fetching latest from GitHub..."
git fetch --all -q
echo ""

# Show today's commits
echo "📅 Commits heute ($(date +%Y-%m-%d)):"
echo "---"
git log --all --since="today" --pretty=format:"%h %Cgreen%an%Creset %ad %Cblue%s%Creset" --date=short
echo ""
echo ""

# Show changed files today
echo "📁 Geänderte Dateien heute:"
echo "---"
git log --all --since="today" --name-only --pretty=format:"" | sort | uniq | head -20
echo ""
echo ""

# Show branch status
echo "🌳 Branch Status:"
echo "---"
git branch -a | grep -E "agent|main|develop"
echo ""

# Show latest commit per agent branch
echo "🤖 Agent Status (letzter Commit):"
echo "---"
echo "Backend:  $(git log agent/backend-calculation --oneline -1)"
echo "Frontend: $(git log agent/frontend-workflow --oneline -1)"
echo "UI:       $(git log agent/ui-specialist --oneline -1)"
echo "Main:     $(git log main --oneline -1)"
echo ""

# Show files changed on each agent branch (vs main)
echo "📊 Änderungen pro Agent (vs main):"
echo "---"
echo "Backend:  $(git diff --shortstat main..agent/backend-calculation)"
echo "Frontend: $(git diff --shortstat main..agent/frontend-workflow)"
echo "UI:       $(git diff --shortstat main..agent/ui-specialist)"
echo ""

echo "============================================================"
echo "✅ Activity Report Complete"
echo "============================================================"
```

**Ausführen:**

```bash
chmod +x scripts/show-activity.sh
./scripts/show-activity.sh
```

---

## 🎯 WARUM IST SPRINT_BOARD.md NICHT AKTUELL?

**Problem:**
- Du öffnest `06-sprints/SPRINT_BOARD.md` auf GitHub
- Du siehst alten Stand

**Grund:**
- Du schaust auf `main` Branch
- Sprint Board Updates sind auf `agent/ui-specialist` Branch!

**Lösung:**

**GitHub:**
```
1. Branch Dropdown → "agent/ui-specialist" wählen
2. 06-sprints/SPRINT_BOARD.md öffnen
3. Jetzt siehst du aktuellen Stand!
```

**Lokal:**
```bash
git checkout agent/ui-specialist
cat 06-sprints/SPRINT_BOARD.md
```

---

## 📌 QUICK REFERENCE

### "Ich will wissen was heute passiert ist"

```bash
# Terminal:
git log --all --since="today" --oneline --graph

# Oder Script:
./scripts/show-activity.sh
```

### "Ich will Sprint Board aktuell sehen"

```bash
# GitHub: Branch wählen → agent/ui-specialist → 06-sprints/SPRINT_BOARD.md

# Terminal:
git checkout agent/ui-specialist
cat 06-sprints/SPRINT_BOARD.md
git checkout main  # zurück
```

### "Ich will sehen was ein Agent gemacht hat"

```bash
# GitHub:
# → Commits → Branch: agent/backend-calculation → Filter nach [BACKEND]

# Terminal:
git log agent/backend-calculation --oneline --since="today"
git diff main..agent/backend-calculation --stat
```

### "Ich will Code von Agents sehen"

```bash
# Backend Code:
git checkout agent/backend-calculation
ls -la backend/

# Frontend Code:
git checkout agent/frontend-workflow
ls -la frontend/src/

# UI Components:
git checkout agent/ui-specialist
ls -la frontend/src/components/ui/

# Zurück:
git checkout main
```

---

## 🔧 WARUM DIESE STRUKTUR?

**Multi-Agent Parallel Development:**

```
✅ Vorteile:
- Agents arbeiten parallel (keine conflicts)
- Isolierte Entwicklung (eigener workspace)
- Main branch bleibt clean (nur stable releases)
- Easy rollback (jeder Agent branch separat)

❌ Nachteil:
- Du musst zwischen Branches wechseln um aktuellen Stand zu sehen
- Files sind auf verschiedenen Branches

🎯 Lösung:
- Integration Day (MORGEN, 2025-11-11)
- Alle Branches → develop
- Dann: develop → main (Release)
```

---

## 📊 MORGEN (INTEGRATION DAY)

**Was passiert:**

```
09:00-11:00  Review Agent Deliverables (auf agent branches)
11:00-13:00  Create develop branch & Merge all agents
13:00-15:00  Integration Testing (auf develop branch)
15:00-17:00  Quality Gate 1.5
17:00-18:00  Merge develop → main & Tag v0.1.0-alpha

NACH Integration:
→ Alle Files sind auf main branch
→ Sprint Board ist aktuell auf main
→ Code ist auf main
→ Du brauchst nicht mehr zwischen Branches wechseln
```

---

## 📝 ZUSAMMENFASSUNG

**Dein Problem:**
- Files auf main sind alt
- Aktuelle Entwicklung ist auf agent branches

**Deine Lösung:**

1. **GitHub:**
   - Branch Dropdown nutzen → agent/xxx wählen
   - Commits → "All branches" anzeigen
   - Network Graph ansehen

2. **Lokal:**
   - `git checkout agent/backend-calculation` (Code sehen)
   - `git checkout agent/ui-specialist` (Sprint Board sehen)
   - `git log --all --since="today"` (Change Log)
   - `./scripts/show-activity.sh` (Activity Report)

3. **Change Log:**
   - GitHub: Commits → All branches
   - Lokal: `git log --all --since="today"`
   - Script: `show-activity.sh` (wird erstellt)

**Ab Morgen:**
- Alles auf `main` nach Integration
- Keine Branch-Switches mehr nötig

---

**Erstellt:** 2025-11-10
**Von:** Governance Agent
**Für:** Project Owner (User)
