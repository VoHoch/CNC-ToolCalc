# 🚀 START INTEGRATION DAY - User Instructions

**Date:** 2025-11-11
**Goal:** Make CNC-ToolCalc app testable
**Timeline:** 7-8 hours
**Status:** READY TO START

---

## 📋 QUICK START GUIDE

### Step 1: Read the Integration CR
```bash
cat 02-change-requests/active/CR-2025-11-11-004-INTEGRATION.md
```

### Step 2: Start Agents (in order!)

**You need to start 3 separate Claude Code sessions, in this order:**

#### Session 1: Backend Agent (Start FIRST!)
```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/05-integration-backend-agent.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

TASK: Merge backend to develop, setup venv, run tests, start server.
GOAL: Server running on http://localhost:8000

Deadline: 1 hour
```

**Wait until:** Backend server is running (check terminal shows "Uvicorn running on http://127.0.0.1:8000")

---

#### Session 2: UI Agent (Start AFTER Backend)
```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/07-integration-ui-agent.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

TASK: Merge UI components to develop, verify all 7 components + Design System.
GOAL: Components ready for frontend integration.

Deadline: 1 hour
```

**Wait until:** UI agent reports "Integration complete"

---

#### Session 3: Frontend Agent (Start LAST!)
```
Bitte lies und führe aus:
/Users/nwt/developments/cnc-toolcalc/08-claude-prompts/06-integration-frontend-agent.md

Working Directory: /Users/nwt/developments/cnc-toolcalc

TASK: Merge frontend to develop, connect to backend, make app testable.
GOAL: App running on http://localhost:5173

PREREQUISITE: Backend server must be running!

Deadline: 2 hours
```

**Wait until:** Frontend server is running (check terminal shows "Local: http://localhost:5173/")

---

## ✅ VERIFICATION CHECKLIST

### After Backend Complete:
```bash
# Check backend is running
curl http://localhost:8000/health

# Expected: {"status": "healthy"}
```

### After UI Complete:
```bash
# Check UI components merged
ls -la frontend/src/components/ui/

# Expected: 7 components (.tsx + .css files)
```

### After Frontend Complete:
```bash
# Check frontend is running
curl http://localhost:5173

# Expected: HTML response

# Check it connects to backend
# Open browser console (F12) and check network tab
```

---

## 🎯 WHEN ALL AGENTS COMPLETE

### You Can Test the App!

**Open Browser:**
```
http://localhost:5173
```

**Test Workflow:**
1. Select a tool (e.g., "10mm End Mill")
2. Select material for this tool (e.g., "Aluminium")
3. Select operation (e.g., "SLOT")
4. Configure parameters
5. Click "Calculate"
6. Verify results displayed (vc, n, fz, vf, ae, ap)

**Expected:**
- ✅ App loads (dark theme)
- ✅ Navigation works (6 screens)
- ✅ Material selection works (per tool!)
- ✅ Calculate button works
- ✅ Results from backend displayed

---

## 📊 MONITORING PROGRESS

### Terminal Windows You Should Have:

**Terminal 1:** Backend Server
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Terminal 2:** Frontend Dev Server
```
  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

**Terminal 3:** Spare (for git commands, testing, etc.)

### Check Status Anytime:
```bash
# Backend health
curl http://localhost:8000/health

# Frontend running
curl http://localhost:5173

# Git status
git branch --show-current  # Should be "develop"
git log --oneline -5       # See recent integration commits
```

---

## ⏰ TIMELINE ESTIMATE

| Agent | Task | Time | Start | End |
|-------|------|------|-------|-----|
| Backend | Merge + Setup + Tests + Server | 1h | 09:30 | 10:30 |
| UI | Merge + Verify Components | 1h | 10:30 | 11:30 |
| Frontend | Merge + Connect + Build | 2h | 11:30 | 13:30 |
| **Your Testing** | Test app manually | 1h | 13:30 | 14:30 |

**Total:** ~5 hours (with 1 hour buffer)

---

## 🐛 TROUBLESHOOTING

### Problem: "Backend won't start"
```bash
# Check Python version
python3 --version  # Should be 3.11 or 3.12

# Check venv
cd backend
source venv/bin/activate
pip list  # Should show fastapi, uvicorn, etc.

# Try starting manually
uvicorn main:app --reload --port 8000
```

### Problem: "Frontend won't start"
```bash
# Check Node version
node --version  # Should be v18 or higher

# Clean install
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Problem: "CORS errors in browser"
```bash
# Backend needs CORS config
# Backend agent should handle this, but if not:
# Edit backend/main.py and add CORS middleware
```

### Problem: "Agents not responding"
- Check that each agent reads the correct prompt file
- Check that working directory is `/Users/nwt/developments/cnc-toolcalc`
- Check that agents are in FULL EXECUTION mode

---

## 📝 INTEGRATION REPORTS

**After each agent completes, check their reports:**

```bash
# Backend report
cat .agent-reports/backend-calculation/INTEGRATION_REPORT.md

# UI report
cat .agent-reports/ui-specialist/INTEGRATION_REPORT.md

# Frontend report
cat .agent-reports/frontend-workflow/INTEGRATION_REPORT.md
```

---

## 🎉 SUCCESS CRITERIA

**Integration is COMPLETE when:**

- [x] Backend server running on port 8000
- [x] Frontend dev server running on port 5173
- [x] You can open http://localhost:5173 in browser
- [x] You can complete workflow: Tool → Material → Calculate → Results
- [x] Backend API responds to requests
- [x] All 3 integration reports created
- [x] No critical errors in console or logs

**THEN:** ✅ **APP IS TESTABLE!**

---

## 📞 IF YOU NEED HELP

**Check Integration CR for details:**
```bash
cat 02-change-requests/active/CR-2025-11-11-004-INTEGRATION.md
```

**Check yesterday's completion report:**
```bash
cat .agent-reports/governance/FINAL_INTEGRATION_READINESS_REPORT.md
```

**Check agent instructions:**
```bash
# Backend
cat 08-claude-prompts/05-integration-backend-agent.md

# UI
cat 08-claude-prompts/07-integration-ui-agent.md

# Frontend
cat 08-claude-prompts/06-integration-frontend-agent.md
```

---

## ✅ READY TO START?

**Prerequisites:**
- [x] Git repository clean (no uncommitted changes)
- [x] All smoke tests passed yesterday (verified)
- [x] Integration CR created
- [x] Agent instructions ready

**Now:**

1. Start Backend Agent (Session 1)
2. Wait for backend to finish
3. Start UI Agent (Session 2)
4. Wait for UI to finish
5. Start Frontend Agent (Session 3)
6. Wait for frontend to finish
7. **TEST THE APP!** 🎉

---

**START TIME:** $(date +%H:%M)
**EXPECTED COMPLETION:** ~5 hours from now
**YOUR GOAL:** Test the working application!

**🚀 LET'S GO!**
