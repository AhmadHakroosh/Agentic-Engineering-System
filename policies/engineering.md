# Engineering policy

## Required

- Trace every behavior change to an acceptance criterion.
- Preserve public compatibility unless an approved design explicitly changes it.
- Test behavior, boundaries, failure paths, and regressions at the lowest useful level.
- Use existing architecture and conventions; document material exceptions.
- Keep diffs focused. Separate mechanical refactoring from behavior changes.
- Make failures observable and errors actionable without leaking sensitive data.
- Record commands and results; never claim an unexecuted check passed.

## Human decision required

Data loss risk, irreversible migrations, new paid services, public API breaks, meaningful privacy changes, and exceptions to security or release policy require explicit human approval.

