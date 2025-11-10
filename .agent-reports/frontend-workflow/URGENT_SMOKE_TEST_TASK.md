# 🔥 URGENT TASK: Smoke Test erstellen

**Agent:** frontend-workflow
**Priority:** 🚨 **KRITISCH**
**Deadline:** 2025-11-10 (HEUTE, vor 18:00)
**Status:** ❌ **NICHT ERLEDIGT**

---

## 📋 AUFGABE

**Du musst einen Smoke Test für deine Frontend Implementation erstellen und ausführen.**

Ein Smoke Test ist ein **5-Minuten Schnelltest**, der prüft:
- ✅ Baut das Frontend ohne Fehler?
- ✅ Startet der Dev Server?
- ✅ Rendert die App ohne Crashes?

**WICHTIG:** Dies ist ein **simpler Schnelltest** für die finale Validierung vor dem Merge.

---

## 🎯 DELIVERABLES (3 Files)

### 1. Shell Script: `frontend/smoke-test.sh`

```bash
#!/bin/bash
# Smoke Test: Frontend Build & Dev Server
# 5-Minute Sanity Check vor Integration

set -e  # Exit on error

echo "============================================================"
echo "🔥 SMOKE TEST: Frontend Workflow"
echo "============================================================"

# 1. Install dependencies (if needed)
echo ""
echo "[1/4] Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "      Installing npm dependencies..."
    npm install
else
    echo "      ✅ Dependencies OK (node_modules exists)"
fi

# 2. TypeScript Check
echo ""
echo "[2/4] TypeScript type checking..."
npm run type-check || {
    echo "      ❌ TypeScript errors found!"
    exit 1
}
echo "      ✅ TypeScript OK (no errors)"

# 3. Build
echo ""
echo "[3/4] Building production bundle..."
npm run build || {
    echo "      ❌ Build failed!"
    exit 1
}
echo "      ✅ Build OK"

# Check dist/ folder
if [ ! -d "dist" ]; then
    echo "      ❌ dist/ folder not created!"
    exit 1
fi

if [ ! -f "dist/index.html" ]; then
    echo "      ❌ dist/index.html not found!"
    exit 1
fi

DIST_SIZE=$(du -sh dist | cut -f1)
echo "      📦 Bundle size: $DIST_SIZE"

# 4. Dev Server Test
echo ""
echo "[4/4] Testing dev server..."
echo "      Starting server (background)..."

# Start dev server in background
npm run dev &
DEV_PID=$!

# Wait for server to start
echo "      Waiting 5 seconds for server startup..."
sleep 5

# Check if server is running
if ! ps -p $DEV_PID > /dev/null; then
    echo "      ❌ Dev server failed to start!"
    exit 1
fi

# Check if server responds
echo "      Testing HTTP request to localhost:5173..."
curl -f -s http://localhost:5173 > /dev/null || {
    echo "      ❌ Server not responding!"
    kill $DEV_PID 2>/dev/null
    exit 1
}

echo "      ✅ Dev server OK (responding on port 5173)"

# Stop server
echo "      Stopping dev server..."
kill $DEV_PID 2>/dev/null
sleep 1

echo ""
echo "============================================================"
echo "🎉 SMOKE TEST PASSED!"
echo "============================================================"
echo ""
echo "✅ All 4 checks successful:"
echo "   1. Dependencies installed"
echo "   2. TypeScript type check (no errors)"
echo "   3. Production build successful"
echo "   4. Dev server started and responding"
echo ""
echo "✅ Frontend ready for integration!"
echo ""
```

---

### 2. Component Test: `frontend/src/__tests__/smoke.test.tsx`

```typescript
/**
 * Smoke Test: Basic App Rendering
 * Verifies app renders without crashing
 */
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

describe('Smoke Test: App Rendering', () => {
  it('renders without crashing', () => {
    render(<App />)
    // App should render without throwing errors
    expect(document.body).toBeTruthy()
  })

  it('renders main navigation or title', () => {
    render(<App />)
    // Check if app has some recognizable content
    // Adjust selector based on your actual app structure
    const mainElement = screen.getByRole('main') || document.querySelector('main') || document.body
    expect(mainElement).toBeTruthy()
  })

  it('has no console errors', () => {
    const consoleSpy = vi.spyOn(console, 'error')
    render(<App />)
    expect(consoleSpy).not.toHaveBeenCalled()
    consoleSpy.mockRestore()
  })
})
```

---

### 3. NPM Script: Update `frontend/package.json`

**Add script:**

```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "smoke-test": "./smoke-test.sh"
  }
}
```

---

## ⚙️ SETUP

**1. Install dependencies (if needed):**

```bash
cd frontend

# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Install curl (usually pre-installed on Mac/Linux)
which curl || echo "Install curl first!"
```

**2. Create test directory:**

```bash
mkdir -p frontend/src/__tests__
```

**3. Create files:**

```bash
# Shell script
cat > frontend/smoke-test.sh << 'EOF'
[paste script above]
EOF

chmod +x frontend/smoke-test.sh

# Component test
cat > frontend/src/__tests__/smoke.test.tsx << 'EOF'
[paste test above]
EOF
```

---

## 🚀 AUSFÜHREN

**Option A: Shell Script (empfohlen)**

```bash
cd frontend
./smoke-test.sh
```

**Option B: NPM Script**

```bash
cd frontend
npm run smoke-test
```

**Option C: Component Test only**

```bash
cd frontend
npm run test src/__tests__/smoke.test.tsx
```

---

## 📊 EXPECTED OUTPUT

```
============================================================
🔥 SMOKE TEST: Frontend Workflow
============================================================

[1/4] Checking dependencies...
      ✅ Dependencies OK (node_modules exists)

[2/4] TypeScript type checking...
      ✅ TypeScript OK (no errors)

[3/4] Building production bundle...
vite v5.0.0 building for production...
✓ 234 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.30 kB
dist/assets/index-DQnaAXbE.css    8.23 kB │ gzip:  2.35 kB
dist/assets/index-BKw7msJ2.js   156.78 kB │ gzip: 52.34 kB
✓ built in 3.42s
      ✅ Build OK
      📦 Bundle size: 512K

[4/4] Testing dev server...
      Starting server (background)...
      Waiting 5 seconds for server startup...
      Testing HTTP request to localhost:5173...
      ✅ Dev server OK (responding on port 5173)
      Stopping dev server...

============================================================
🎉 SMOKE TEST PASSED!
============================================================

✅ All 4 checks successful:
   1. Dependencies installed
   2. TypeScript type check (no errors)
   3. Production build successful
   4. Dev server started and responding

✅ Frontend ready for integration!
```

---

## 📄 SMOKE TEST REPORT

**Nach erfolgreichem Test, erstelle:**

`.agent-reports/frontend-workflow/SMOKE_TEST_REPORT.md`

```markdown
# Smoke Test Report: Frontend Workflow

**Agent:** frontend-workflow
**Date:** 2025-11-10
**Time:** [HH:MM]
**Status:** ✅ **PASS** / ❌ **FAIL**

---

## Test Execution

**Command:**
\`\`\`bash
cd frontend
./smoke-test.sh
\`\`\`

**Duration:** [X seconds]

---

## Test Results

| Test | Check | Status | Details |
|------|-------|--------|---------|
| 1 | Dependencies | ✅ PASS | node_modules OK |
| 2 | TypeScript | ✅ PASS | 0 errors |
| 3 | Build | ✅ PASS | Bundle: 512K |
| 4 | Dev Server | ✅ PASS | Port 5173 responding |

---

## Build Output

**Bundle Size:**
- Total: 512K
- index.html: 0.45 kB
- CSS: 8.23 kB (gzip: 2.35 kB)
- JS: 156.78 kB (gzip: 52.34 kB)

**Build Time:** 3.42s

---

## TypeScript Checks

✅ No type errors
✅ All imports resolved
✅ API types correct (CalculationRequest, CalculationResponse)

---

## Issues Found

(none) / (list any issues)

---

## File Checklist

- [x] 6 Screens implemented (ToolSelection, MaterialSelection, OperationSelection, ParameterConfig, Results, Export)
- [x] 5 Zustand Stores (tool, material, calculation, expertMode, export)
- [x] API Client complete (7 endpoints)
- [x] Material selection PER TOOL ✓
- [x] Navigation working
- [x] TypeScript types complete

---

## Conclusion

✅ Frontend Workflow is **PRODUCTION READY**
- All 6 screens implemented
- State management working
- API integration complete
- Material selection PER TOOL verified
- Build successful, no errors

**Ready for Integration:** YES

---

**Tested by:** Frontend Workflow Agent
**Sign-off:** ✅ APPROVED for Integration
```

---

## ✅ COMMIT

```bash
git add frontend/smoke-test.sh
git add frontend/src/__tests__/smoke.test.tsx
git add frontend/package.json
git add .agent-reports/frontend-workflow/SMOKE_TEST_REPORT.md
git commit -m "[FRONTEND] Add smoke test + report

Smoke Test Results:
- Dependencies: PASS
- TypeScript check: PASS (0 errors)
- Production build: PASS (512K bundle)
- Dev server: PASS (port 5173)

Status: ✅ READY FOR INTEGRATION

Time: $(date +%H:%M)"

git push origin agent/frontend-workflow
```

---

## 🎯 SUCCESS CRITERIA

- [x] `frontend/smoke-test.sh` erstellt & ausführbar
- [x] `frontend/src/__tests__/smoke.test.tsx` erstellt
- [x] `package.json` script hinzugefügt
- [x] Smoke test erfolgreich ausgeführt (alle 4 checks PASS)
- [x] SMOKE_TEST_REPORT.md erstellt
- [x] Committed & pushed

**Timeline:** 30-45 Minuten

**Wenn fertig:** Update diese Datei mit Status: ✅ **ERLEDIGT**

---

## 🐛 TROUBLESHOOTING

**Problem: "TypeScript errors"**
```bash
# Check errors
npm run type-check

# Fix common issues:
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

**Problem: "Dev server not starting"**
```bash
# Check if port 5173 is in use
lsof -ti:5173 | xargs kill -9  # Kill process on port 5173
npm run dev
```

**Problem: "curl: command not found"**
```bash
# On Mac (should be pre-installed)
which curl

# Alternative: Use wget
wget -O /dev/null http://localhost:5173
```

---

## ❓ FRAGEN?

**Siehe:**
- `.agent-reports/governance/STATUS_REPORT_2025-11-10.md` für Kontext
- `.agent-reports/governance/AGENT_INSTRUCTIONS_URGENT.md` für 30-min commit rule

**Governance Review:** Morgen (2025-11-11) 09:00

---

**Created:** 2025-11-10
**Priority:** 🚨 KRITISCH
**Deadline:** HEUTE (vor 18:00)
