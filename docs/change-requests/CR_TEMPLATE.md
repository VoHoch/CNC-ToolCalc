# Change Request Template

**CR-ID:** CR-YYYY-MM-DD-XXX
**Version:** vX.Y.Z → vX.Y.Z+1
**Agent:** [ui-specialist / frontend-workflow / backend-calculation]
**Status:** [DRAFT / IN_PROGRESS / TESTING / APPROVED / REJECTED]
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

---

## Summary

Brief description of the change (1-2 sentences).

---

## Type

- [ ] Feature (new functionality)
- [ ] Enhancement (improvement to existing feature)
- [ ] Bug Fix
- [ ] Refactoring (no functional change)
- [ ] Documentation
- [ ] Test

---

## Motivation

Why is this change needed?

---

## Detailed Description

What exactly is being changed?

---

## Implementation Details

### Files Changed
- `/path/to/file1.py` (new)
- `/path/to/file2.tsx` (modified)
- `/path/to/file3.css` (modified)

### Code Changes

```python
# Example code snippets
def new_function():
    pass
```

### Dependencies
- New packages: `package-name==version`
- Updated packages: `package-name: 1.0.0 → 2.0.0`

---

## Architecture Compliance

- [ ] Follows V1.0 Cleanroom principle (no V2.0 code)
- [ ] Implements Architecture Doc specifications
- [ ] API Contract adhered to
- [ ] Component Interface followed
- [ ] Dark Theme only
- [ ] Accessibility WCAG 2.1 AA

---

## Testing

### Unit Tests
- [ ] Tests written: X tests
- [ ] Coverage: X% (target: >90%)
- [ ] All tests passing

### Integration Tests
- [ ] Integration tests written
- [ ] All integration tests passing

### Smoke Test
- [ ] Smoke test executed
- [ ] Smoke test passed
- [ ] Smoke test script: `scripts/smoke-test-cr-xxx.sh`

**Smoke Test Results:**
```
✓ Feature X renders correctly
✓ API endpoint responds
✓ No console errors
```

---

## Quality Audit

### Code Quality
- [ ] Type safety: 100% (TypeScript/Pydantic)
- [ ] Linter: 0 errors
- [ ] Code duplication: <5%
- [ ] Cyclomatic complexity: <15

### Performance
- [ ] No performance regressions
- [ ] Meets performance budget
  - Calculation: <100ms
  - UI render: <16ms

### Security
- [ ] Input validation present
- [ ] No XSS vulnerabilities
- [ ] No SQL injection risks
- [ ] Secrets not in code

---

## User Acceptance Test (UAT)

**UAT Test Plan:**
1. Test scenario 1
2. Test scenario 2
3. ...

**UAT Results:**
- [ ] UAT completed by: [User Name]
- [ ] UAT date: YYYY-MM-DD
- [ ] UAT status: [PASSED / FAILED]

**User Feedback:**
```
User comments here...
```

---

## Rollback Plan

If this CR causes issues, how to rollback:
```bash
git revert <commit-hash>
# OR
git checkout <previous-tag>
```

---

## Related Change Requests

- Depends on: CR-YYYY-MM-DD-XXX
- Blocks: CR-YYYY-MM-DD-XXX
- Related: CR-YYYY-MM-DD-XXX

---

## Approval

- [ ] Agent self-review completed
- [ ] Governance Agent review completed
- [ ] Smoke test passed
- [ ] UAT passed
- [ ] Ready for merge

**Approved by:** Governance Agent
**Date:** YYYY-MM-DD

---

## Post-Merge

- [ ] Merged to `develop`
- [ ] Merged to `main`
- [ ] Tagged: `vX.Y.Z`
- [ ] Deployed to production
- [ ] Release notes updated
