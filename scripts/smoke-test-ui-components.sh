#!/bin/bash
#
# CNC-ToolCalc UI Components Smoke Test
# Agent: UI Specialist
# Date: 2025-11-10
# Deadline: 18:00
#

# set -e  # Disabled to see all results

echo "=========================================="
echo "🧪 UI Components Smoke Test"
echo "=========================================="
echo ""
echo "Agent: UI Specialist"
echo "Date: $(date)"
echo "Branch: agent/ui-specialist"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASS++))
}

fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAIL++))
}

warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((WARN++))
}

info() {
    echo -e "ℹ️  INFO: $1"
}

# Test 1: Component Files Exist
echo "=========================================="
echo "Test 1: Component Files Exist"
echo "=========================================="

COMPONENTS=(
    "Slider"
    "CompactSlider"
    "Table"
    "Button"
    "Card"
    "OperationMatrix"
    "ProgressBar"
)

for component in "${COMPONENTS[@]}"; do
    if [ -f "frontend/src/components/common/${component}.tsx" ] && \
       [ -f "frontend/src/components/common/${component}.css" ]; then
        pass "${component} files exist (.tsx + .css)"
    else
        fail "${component} files missing"
    fi
done

echo ""

# Test 2: Design System
echo "=========================================="
echo "Test 2: Design System Files"
echo "=========================================="

if [ -f "frontend/src/styles/design-tokens.css" ]; then
    pass "design-tokens.css exists"

    VAR_COUNT=$(grep -c "^\s*--" frontend/src/styles/design-tokens.css || echo "0")
    if [ "$VAR_COUNT" -ge 30 ]; then
        pass "CSS variables: $VAR_COUNT (target: ≥30)"
    else
        fail "CSS variables: $VAR_COUNT (target: ≥30)"
    fi
else
    fail "design-tokens.css missing"
fi

if [ -f "frontend/src/styles/fonts.css" ]; then
    pass "fonts.css exists"
else
    fail "fonts.css missing"
fi

echo ""

# Test 3: CRITICAL - Slider NO Visible Thumb
echo "=========================================="
echo "Test 3: 🚨 CRITICAL - Slider NO Visible Thumb"
echo "=========================================="

if grep -q "width: 0" frontend/src/components/common/Slider.css && \
   grep -q "height: 0" frontend/src/components/common/Slider.css && \
   grep -q "opacity: 0" frontend/src/components/common/Slider.css; then
    pass "Slider thumb INVISIBLE (width: 0, height: 0, opacity: 0)"
else
    fail "Slider thumb might be VISIBLE!"
fi

if grep -A 5 "::-webkit-slider-thumb" frontend/src/components/common/Slider.css | grep -q "width: 0"; then
    pass "Webkit slider thumb hidden"
else
    warn "Webkit slider thumb check"
fi

if grep -A 5 "::-moz-range-thumb" frontend/src/components/common/Slider.css | grep -q "width: 0"; then
    pass "Firefox slider thumb hidden"
else
    warn "Firefox slider thumb check"
fi

echo ""

# Test 4: TypeScript Exports
echo "=========================================="
echo "Test 4: TypeScript Exports"
echo "=========================================="

if [ -f "frontend/src/components/common/index.ts" ]; then
    pass "index.ts exists"

    EXPORT_COUNT=$(grep -c "export" frontend/src/components/common/index.ts || echo "0")
    info "Export count: $EXPORT_COUNT"
else
    fail "index.ts missing"
fi

echo ""

# Test 5: Storybook Stories
echo "=========================================="
echo "Test 5: Storybook Stories"
echo "=========================================="

STORY_COUNT=$(ls -1 frontend/src/components/common/*.stories.tsx 2>/dev/null | wc -l | tr -d ' ')
if [ "$STORY_COUNT" -ge 3 ]; then
    pass "Storybook stories: $STORY_COUNT files"
else
    warn "Storybook stories: $STORY_COUNT files"
fi

echo ""

# Test 6: Code Stats
echo "=========================================="
echo "Test 6: Code Statistics"
echo "=========================================="

TSX_LINES=$(cat frontend/src/components/common/*.tsx 2>/dev/null | wc -l | tr -d ' ')
CSS_LINES=$(cat frontend/src/components/common/*.css 2>/dev/null | wc -l | tr -d ' ')
TOTAL_LINES=$((TSX_LINES + CSS_LINES))

info "TypeScript: $TSX_LINES lines"
info "CSS: $CSS_LINES lines"
info "Total: $TOTAL_LINES lines"

if [ "$TOTAL_LINES" -ge 2000 ]; then
    pass "Code size: $TOTAL_LINES lines"
else
    warn "Code size: $TOTAL_LINES lines"
fi

echo ""

# Summary
echo "=========================================="
echo "📊 Test Summary"
echo "=========================================="
echo ""
echo -e "${GREEN}✅ PASSED:${NC} $PASS"
echo -e "${YELLOW}⚠️  WARNINGS:${NC} $WARN"
echo -e "${RED}❌ FAILED:${NC} $FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL CRITICAL TESTS PASSED!${NC}"
    echo ""
    echo "Status: ✅ READY FOR REVIEW"
    exit 0
else
    echo -e "${RED}⚠️  SOME TESTS FAILED${NC}"
    echo ""
    echo "Status: ❌ NEEDS FIXES"
    exit 1
fi
