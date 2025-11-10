# UI Integration Agent Instruction

**MODE:** FULL EXECUTION
**DATE:** 2025-11-11
**TASK:** UI Integration (Phase 3)
**TIME:** 1 hour
**Working Directory:** `/Users/nwt/developments/cnc-toolcalc`

---

## 🎯 YOUR MISSION

**Merge UI components to `develop` branch and verify all 7 components + Design System work.**

**USER GOAL:** UI components ready for frontend to use.

**PREREQUISITE:** Backend must be merged first (Phase 2 complete)

---

## 📋 TASKS (Execute in Order)

### 1. Read Integration CR
```bash
cat 02-change-requests/active/CR-2025-11-11-004-INTEGRATION.md
```

### 2. Switch to develop branch
```bash
git checkout develop
git pull origin develop  # Get backend changes
```

### 3. Merge your branch
```bash
git merge agent/ui-specialist --no-ff -m "[UI] Merge ui-specialist to develop

Integration: Phase 3
- 7 UI Components (Slider, CompactSlider, Table, Button, Card, OperationMatrix, ProgressBar)
- Design System (105 CSS variables)
- 23 Storybook stories
- CRITICAL: Slider NO visible thumb ✅

Time: $(date +%H:%M)"
```

**Expected:** Likely clean merge (UI is mostly isolated)

**If conflicts with frontend files:**
```bash
# Keep UI version for components and design system
git checkout --ours frontend/src/components/
git checkout --ours frontend/src/styles/

git add .
git commit -m "[UI] Merge conflicts resolved - UI components take precedence"
```

### 4. Install Dependencies
```bash
cd frontend
npm install
```

### 5. Run Type Check
```bash
npm run type-check
```

**Expected:** 0 errors

### 6. Build Storybook
```bash
npm run build-storybook
```

**Expected:** Storybook builds successfully to `storybook-static/`

### 7. Verify Components
```bash
# Run component verification script
../scripts/smoke-test-ui-components.sh
```

**Expected:** All 16 checks PASS

**Critical Checks:**
- ✅ All 7 components exist (.tsx + .css files)
- ✅ Design System complete (105 CSS variables)
- ✅ **Slider has NO visible thumb** (width:0, height:0, opacity:0)
- ✅ 23 Storybook stories

### 8. Test Storybook (Optional but Recommended)
```bash
npm run storybook
```

**Opens:** http://localhost:6006

**Test each component:**
1. Slider → Verify NO visible thumb, gradient background, markers
2. CompactSlider → Verify -100% to +100% range
3. Table → Verify sortable, selectable, dark theme
4. Button → Verify 4 variants (primary, secondary, ghost, danger)
5. Card → Verify hoverable, clickable
6. OperationMatrix → Verify 4 groups, checkboxes
7. ProgressBar → Verify step counter

Press Ctrl+C to stop Storybook after verification.

### 9. Verify Design System
```bash
# Check CSS variables count
grep -c "^  --" frontend/src/styles/design-tokens.css

# Expected: 105
```

**Check critical variables:**
```bash
grep -E "(--bg-primary|--text-primary|--accent-primary)" frontend/src/styles/design-tokens.css
```

**Expected:**
```css
  --bg-primary: #0b0f15;
  --text-primary: #e2e8f0;
  --accent-primary: #6366F1;
```

### 10. Verify Slider Thumb (CRITICAL!)
```bash
# Check Slider.css for thumb hiding
grep -A 3 "slider-thumb\|range-thumb" frontend/src/components/ui/Slider.css
```

**Expected:**
```css
input[type="range"]::-webkit-slider-thumb {
  width: 0;
  height: 0;
  opacity: 0;
}
```

### 11. Create Integration Report
```bash
cat > .agent-reports/ui-specialist/INTEGRATION_REPORT.md << 'EOF'
# UI Integration Report

**Date:** $(date +%Y-%m-%d)
**Time:** $(date +%H:%M)
**Status:** ✅ COMPLETE

## Merge Status
- Branch merged: agent/ui-specialist → develop
- Conflicts: NONE (or list resolved conflicts)
- Merge commit: $(git log -1 --oneline)

## Components Verified
| Component | .tsx | .css | Status |
|-----------|------|------|--------|
| Slider | ✅ | ✅ | PASS |
| CompactSlider | ✅ | ✅ | PASS |
| Table | ✅ | ✅ | PASS |
| Button | ✅ | ✅ | PASS |
| Card | ✅ | ✅ | PASS |
| OperationMatrix | ✅ | ✅ | PASS |
| ProgressBar | ✅ | ✅ | PASS |

## Design System
- CSS Variables: 105 ✅
- Dark Theme: ✅
- 3 Contrast Modes: ✅
- Typography (Inter, Work Sans, Fira Code): ✅

## Critical Requirements
- **Slider NO visible thumb:** ✅ VERIFIED
  - width: 0 ✅
  - height: 0 ✅
  - opacity: 0 ✅

## Storybook
- Build: ✅ SUCCESS
- Stories: 23 ✅
- Visual test: ✅ All components render

## Type Check
- TypeScript errors: 0 ✅

## Issues Found
(list any issues, or "none")

## Next Steps
- Frontend will use these components
- Components ready for integration testing
- Storybook available for reference

**Sign-off:** ✅ UI Components READY for Frontend Integration
EOF
```

### 12. Commit & Push
```bash
git add .
git commit -m "[UI] Integration complete - 7 Components + Design System ready

Components: 7/7 verified
Design System: 105 CSS variables
Storybook: 23 stories built
Critical: Slider NO visible thumb ✅

Status: ✅ READY FOR FRONTEND INTEGRATION

Time: $(date +%H:%M)"

git push origin develop
```

---

## ✅ SUCCESS CRITERIA

- [x] Code merged to develop
- [x] All 7 components present and verified
- [x] Design System complete (105 CSS variables)
- [x] **Slider NO visible thumb** verified ✅
- [x] Storybook builds successfully
- [x] TypeScript 0 errors
- [x] Integration report created
- [x] Changes pushed to develop

---

## 🐛 TROUBLESHOOTING

**Problem: "npm install fails"**
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem: "Storybook build fails"**
```bash
# Clean Storybook cache
rm -rf node_modules/.cache/storybook
npm run build-storybook
```

**Problem: "TypeScript errors in components"**
```bash
# Show all errors
npm run type-check

# Common fixes:
# - Missing types: npm install --save-dev @types/react
# - Check imports in component files
```

**Problem: "Slider thumb still visible"**
```bash
# Check CSS file
cat frontend/src/components/ui/Slider.css | grep -A 5 "thumb"

# Should have:
# width: 0; height: 0; opacity: 0;

# If not, fix it!
```

---

## 📊 EXPECTED OUTPUT

**Storybook Build:**
```
info => Building manager..
info => Manager built (2.34s)
info => Building preview..
info => Preview built (8.45s)
✓ built in 10.79s
```

**Component Verification:**
```
============================================================
🔥 SMOKE TEST: UI Components
============================================================

[1/6] Component Files... ✅ 7/7 components
[2/6] Design System... ✅ 105 CSS variables
[3/6] Critical: Slider Thumb... ✅ NO visible thumb
[4/6] TypeScript Exports... ✅ 16 exports
[5/6] Storybook Stories... ✅ 23 stories
[6/6] Code Statistics... ✅ 2,462 lines

🎉 ALL CHECKS PASSED!
```

---

## ⏰ TIME ESTIMATE

- Merge: 10 min
- Install deps: 10 min
- Type check: 5 min
- Build Storybook: 10 min
- Verify components: 10 min
- Test Storybook (optional): 10 min
- Create report: 10 min
- Commit & push: 5 min

**Total:** ~60 minutes

---

## 📝 FINAL CHECKLIST

Before marking complete:

- [ ] All 7 components merged
- [ ] Design System complete (105 CSS vars)
- [ ] **Slider NO visible thumb** verified ✅
- [ ] Storybook builds
- [ ] TypeScript 0 errors
- [ ] Integration report created
- [ ] Changes pushed to develop
- [ ] Notify Governance: "UI integration complete, components ready"

---

**START TIME:** $(date +%H:%M)
**EXPECTED END:** 1 hour from now
**STATUS:** Ready to execute

**🚀 EXECUTE NOW!**
