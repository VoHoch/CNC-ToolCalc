# Frontend Integration Agent Instruction

**MODE:** FULL EXECUTION
**DATE:** 2025-11-11
**TASK:** Frontend Integration (Phase 4)
**TIME:** 2 hours
**Working Directory:** `/Users/nwt/developments/cnc-toolcalc`

---

## 🎯 YOUR MISSION

**Merge frontend code to `develop` branch, connect to backend, and make app testable.**

**USER GOAL:** User can open browser, use the app, and test calculations.

**PREREQUISITE:** Backend must be running on http://localhost:8000 (check with Backend Agent first!)

---

## 📋 TASKS (Execute in Order)

### 1. Read Integration CR
```bash
cat 02-change-requests/active/CR-2025-11-11-004-INTEGRATION.md
```

### 2. Verify Backend Running
```bash
curl http://localhost:8000/health
```

**Expected:** `{"status": "healthy"}` or similar

**If fails:** Wait for Backend Agent to complete first!

### 3. Switch to develop branch
```bash
git checkout develop
git pull origin develop  # Get backend changes
```

### 4. Merge your branch
```bash
git merge agent/frontend-workflow --no-ff -m "[FRONTEND] Merge frontend-workflow to develop

Integration: Phase 4
- 6 Screens (ToolSelection, MaterialSelection, OperationSelection, ParameterConfig, Results, Export)
- 5 Zustand Stores (tool, material, calculation, expertMode, export)
- API Client (all endpoints)
- Material selection PER TOOL

Time: $(date +%H:%M)"
```

**Expected Conflicts:**
- `frontend/src/components/` - KEEP UI VERSION (already merged by UI Agent)
- `frontend/src/stores/` - KEEP YOUR VERSION (5 Zustand stores)
- `frontend/src/screens/` - KEEP YOUR VERSION (6 screens)

**Conflict Resolution:**
```bash
# If conflicts occur:
git status  # See which files

# For components - keep UI version
git checkout --theirs frontend/src/components/

# For stores - keep your version
git checkout --ours frontend/src/stores/

# For screens - keep your version
git checkout --ours frontend/src/screens/

# After resolving all conflicts:
git add .
git commit -m "[FRONTEND] Merge conflicts resolved - UI components, screens integrated"
```

### 5. Update API Client Configuration
```bash
# Edit frontend/src/api/client.ts
# Make sure baseURL points to backend:

cat > frontend/src/api/client.ts << 'EOF'
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = {
  baseURL: API_BASE_URL,

  async get(endpoint: string) {
    const response = await fetch(`${this.baseURL}${endpoint}`);
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  },

  async post(endpoint: string, data: any) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  },
};
EOF
```

### 6. Install Dependencies
```bash
cd frontend
npm install
```

### 7. Configure Vite for CORS
```bash
# Edit frontend/vite.config.ts
cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
EOF
```

### 8. Run Type Check
```bash
npm run type-check
```

**Expected:** 0 errors

**If errors:** Fix TypeScript issues, then continue

### 9. Build Production
```bash
npm run build
```

**Expected:** Build completes successfully, creates `dist/` folder

### 10. Start Dev Server
```bash
npm run dev
```

**Keep server running!**

**Expected output:**
```
VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 11. Test in Browser

Open http://localhost:5173

**Test Workflow:**
1. Navigate to Tool Selection
2. Select a tool (e.g., "10mm End Mill")
3. Navigate to Material Selection
4. Select material for this tool (e.g., "Aluminium")
5. Navigate to Operation Selection
6. Select operation (e.g., "SLOT")
7. Navigate to Parameter Configuration
8. Verify default parameters loaded
9. Click "Calculate" button
10. Verify results displayed (vc, n, fz, vf, ae, ap)

**Check browser console:** Should be no errors

**Check backend logs:** Should show API requests

### 12. Test API Integration
```bash
# In browser console (F12):
fetch('http://localhost:8000/api/materials')
  .then(r => r.json())
  .then(console.log)

# Expected: Array of 8 materials
```

### 13. Create Integration Report
```bash
cat > .agent-reports/frontend-workflow/INTEGRATION_REPORT.md << 'EOF'
# Frontend Integration Report

**Date:** $(date +%Y-%m-%d)
**Time:** $(date +%H:%M)
**Status:** ✅ COMPLETE

## Merge Status
- Branch merged: agent/frontend-workflow → develop
- Conflicts resolved:
  - Components: Used UI version (7 components)
  - Stores: Used Frontend version (5 stores)
  - Screens: Used Frontend version (6 screens)
- Merge commit: $(git log -1 --oneline)

## Build Status
- TypeScript check: ✅ 0 errors
- Production build: ✅ SUCCESS
- Dev server: ✅ Running on port 5173

## API Integration
- Backend connection: ✅ http://localhost:8000
- GET /api/materials: ✅ 8 materials loaded
- GET /api/operations: ✅ 13 operations loaded
- POST /api/calculate: ✅ Returns results

## Workflow Testing
- Tool Selection: ✅ Works
- Material Selection (PER TOOL): ✅ Works
- Operation Selection: ✅ Works
- Parameter Configuration: ✅ Works
- Calculate: ✅ Works
- Results Display: ✅ Works

## Issues Found
(list any issues, or "none")

## Browser Console
- Errors: 0
- Warnings: 0 (or list them)

## Next Steps
- User can test at http://localhost:5173
- Expert mode testing
- Export functionality testing

**Sign-off:** ✅ Frontend READY for User Testing
EOF
```

### 14. Commit & Push
```bash
git add .
git commit -m "[FRONTEND] Integration complete - App running on port 5173

Merge: frontend-workflow + ui-specialist integrated
Build: Production build successful
Server: http://localhost:5173
Backend: Connected to http://localhost:8000
Status: ✅ READY FOR USER TESTING

Workflows tested:
- Tool → Material → Operation → Calculate → Results ✅

Time: $(date +%H:%M)"

git push origin develop
```

### 15. Keep Dev Server Running
**IMPORTANT:** Leave dev server running for user testing!

---

## ✅ SUCCESS CRITERIA

- [x] Code merged to develop
- [x] Conflicts resolved (components from UI, stores/screens from frontend)
- [x] Dependencies installed
- [x] TypeScript 0 errors
- [x] Production build successful
- [x] Dev server running on port 5173
- [x] Backend API connected
- [x] At least 1 complete workflow tested
- [x] Integration report created
- [x] User can access http://localhost:5173

---

## 🐛 TROUBLESHOOTING

**Problem: "Backend not responding"**
```bash
# Check backend is running
curl http://localhost:8000/health

# If not running: Start backend first!
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Problem: "CORS errors in browser"**
```bash
# Backend needs CORS configuration
# Edit backend/main.py:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Problem: "Port 5173 already in use"**
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or use different port
npm run dev -- --port 5174
```

**Problem: "TypeScript errors"**
```bash
# Show all errors
npm run type-check

# Common fixes:
# - Missing types: npm install --save-dev @types/react @types/react-dom
# - Import errors: Check paths in tsconfig.json
```

**Problem: "Build fails"**
```bash
# Clean and rebuild
rm -rf dist node_modules
npm install
npm run build
```

---

## 📊 EXPECTED OUTPUT

**Browser (http://localhost:5173):**
- App loads
- Dark theme visible
- 6 screens navigable
- Calculations work
- Results display

**Browser Console:**
```
No errors
(might have some warnings - document them)
```

**Backend Logs (when using app):**
```
INFO:     127.0.0.1:xxxxx - "GET /api/materials HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /api/operations HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/calculate HTTP/1.1" 200 OK
```

---

## ⏰ TIME ESTIMATE

- Merge & resolve conflicts: 30 min
- Configure API client: 10 min
- Install deps: 10 min
- Type check & build: 15 min
- Start dev server: 5 min
- Test workflows: 30 min
- Create report: 15 min
- Commit & push: 5 min

**Total:** ~2 hours

---

## 📝 FINAL CHECKLIST

Before marking complete:

- [ ] Frontend running (check http://localhost:5173)
- [ ] Backend connected (check network tab in browser)
- [ ] At least 1 workflow tested
- [ ] No critical errors in console
- [ ] Integration report created
- [ ] Changes pushed to develop
- [ ] Dev server terminal still open (don't close!)
- [ ] Notify Governance: "Frontend integration complete, app testable at http://localhost:5173"

---

**START TIME:** $(date +%H:%M)
**EXPECTED END:** 2 hours from now
**STATUS:** Ready to execute

**🚀 EXECUTE NOW!**
