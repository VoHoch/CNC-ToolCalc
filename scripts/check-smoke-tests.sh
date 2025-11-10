#!/bin/bash
# Check Smoke Test Status for all Agents

set -e

echo "============================================================"
echo "🔥 Smoke Test Status Check"
echo "============================================================"
echo ""

# Fetch latest
echo "🔄 Fetching latest from GitHub..."
git fetch --all -q
echo ""

AGENTS=("backend-calculation" "frontend-workflow" "ui-specialist")
PASSED=0
FAILED=0
MISSING=0

echo "📊 Checking all 3 agents..."
echo ""

for AGENT in "${AGENTS[@]}"; do
    echo "---"
    echo "🤖 Agent: $AGENT"

    BRANCH="agent/$AGENT"

    # Check if branch exists
    if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
        echo "   ❌ Branch not found: $BRANCH"
        MISSING=$((MISSING + 1))
        continue
    fi

    # Check for smoke test task file
    TASK_FILE=".agent-reports/$AGENT/URGENT_SMOKE_TEST_TASK.md"
    if git show "$BRANCH:$TASK_FILE" >/dev/null 2>&1; then
        echo "   ✅ Task assigned: $TASK_FILE"
    else
        echo "   ❌ Task missing: $TASK_FILE"
        MISSING=$((MISSING + 1))
        continue
    fi

    # Check for smoke test report
    REPORT_FILE=".agent-reports/$AGENT/SMOKE_TEST_REPORT.md"
    if git show "$BRANCH:$REPORT_FILE" >/dev/null 2>&1; then
        echo "   ✅ Report found: $REPORT_FILE"

        # Check if report says PASS
        REPORT_CONTENT=$(git show "$BRANCH:$REPORT_FILE")
        if echo "$REPORT_CONTENT" | grep -q "Status:.*PASS"; then
            echo "   ✅ Status: PASS"
            PASSED=$((PASSED + 1))
        else
            echo "   ❌ Status: FAIL or UNKNOWN"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "   ⚠️  Report not yet created: $REPORT_FILE"
        echo "   📋 Agent still working on smoke tests..."
        MISSING=$((MISSING + 1))
    fi

    # Show latest commit
    LAST_COMMIT=$(git log "$BRANCH" --oneline -1)
    echo "   📝 Latest: $LAST_COMMIT"
    echo ""
done

echo "============================================================"
echo "📊 Summary"
echo "============================================================"
echo ""
echo "Total Agents:  3"
echo "✅ PASSED:     $PASSED / 3"
echo "❌ FAILED:     $FAILED / 3"
echo "⚠️  MISSING:    $MISSING / 3"
echo ""

if [ $PASSED -eq 3 ]; then
    echo "🎉 ALL SMOKE TESTS PASSED!"
    echo "✅ Ready for Integration Day (2025-11-11)"
    exit 0
elif [ $MISSING -gt 0 ]; then
    echo "⚠️  Some agents have not completed smoke tests yet."
    echo "⏰ Deadline: Today (2025-11-10) before 18:00"
    exit 1
else
    echo "❌ Some smoke tests FAILED!"
    echo "🔧 Agents need to fix issues and re-run tests."
    exit 1
fi
