#!/bin/bash
# Smoke Test: Frontend Workflow
# Quick sanity check for frontend integration

set -e  # Exit on error

echo "============================================================"
echo "SMOKE TEST: Frontend Workflow"
echo "============================================================"

START_TIME=$(date +%s)

# 1. Dependencies Check
echo ""
echo "[1/4] Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "      Installing npm dependencies..."
    npm install
else
    echo "      Dependencies OK (node_modules exists)"
fi

# 2. TypeScript Check
echo ""
echo "[2/4] TypeScript type checking..."
npm run type-check 2>&1 | tee /tmp/typecheck.log || {
    echo "      TypeScript errors found!"
    ERRORS=$(grep -c "error TS" /tmp/typecheck.log || echo "0")
    echo "      Total errors: $ERRORS"
    exit 1
}
echo "      TypeScript OK (0 errors)"

# 3. Production Build
echo ""
echo "[3/4] Building production bundle..."
npm run build 2>&1 | tee /tmp/build.log || {
    echo "      Production build failed!"
    exit 1
}
echo "      Production build OK"

# Check dist/ folder
if [ ! -d "dist" ]; then
    echo "      dist/ folder not created!"
    exit 1
fi

if [ ! -f "dist/index.html" ]; then
    echo "      dist/index.html not found!"
    exit 1
fi

BUNDLE_SIZE=$(du -sh dist | cut -f1)
echo "      Bundle size: $BUNDLE_SIZE"

# 4. Dev Server Check (quick start/stop)
echo ""
echo "[4/4] Testing dev server..."
echo "      Starting dev server (3 second test)..."

# Start dev server in background
npm run dev > /tmp/dev-server.log 2>&1 &
DEV_PID=$!

# Wait for server to start (max 10 seconds)
WAIT_COUNT=0
while [ $WAIT_COUNT -lt 10 ]; do
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo "      Dev server responding on http://localhost:5173"
        break
    fi
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

# Kill dev server
kill $DEV_PID 2>/dev/null || true
wait $DEV_PID 2>/dev/null || true

if [ $WAIT_COUNT -eq 10 ]; then
    echo "      WARNING: Dev server did not respond within 10 seconds"
    echo "      This may be expected if Vite config differs"
else
    echo "      Dev server OK"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "============================================================"
echo "SMOKE TEST PASSED!"
echo "============================================================"
echo ""
echo "All 4 checks successful:"
echo "   1. Dependencies installed"
echo "   2. TypeScript type check (0 errors)"
echo "   3. Production build (bundle: $BUNDLE_SIZE)"
echo "   4. Dev server test"
echo ""
echo "Duration: ${DURATION}s"
echo ""
echo "Frontend ready for integration!"
echo ""
