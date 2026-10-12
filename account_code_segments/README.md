# Account Code Segment — FastAPI POS starter

## Included
- `models.py`: SQLAlchemy 2.x models for segments, value sets, values, combinations, mappings, and journals.
- `schemas.py`: Pydantic v2 request/response validation.
- `service.py`: database-aware validation, combination creation, cross-validation, and balanced journal helpers.

## Install
Use versions compatible with your existing project:
```bash
pip install "SQLAlchemy>=2.0" "fastapi>=0.100" "pydantic>=2.0"
```
This code uses Pydantic v2. If your project uses Pydantic v1, schemas need adapting.

## Integration
1. Back up the code and database; use a feature branch.
2. Copy these files into a package such as `backend/app/accounting/coa/`.
3. In `models.py`, replace the sample `Base` class with your existing shared SQLAlchemy Base import. Do not define a second Base.
4. Update `service.py` relative imports to match the package.
5. Ensure Alembic imports these models when loading metadata.
6. Create and review an Alembic migration; apply it to a development database first.
7. Add endpoints in your existing FastAPI router and inject the current request-scoped DB session. Preserve authentication, tenant scoping, and RBAC.
8. Test duplicate codes, inactive values, incorrect segment roles, cross-validation, balanced/unbalanced journals, and repeated source IDs.
9. Only then connect the account mapping layer to real POS sales, payments, purchases, inventory, and tax flows.

## Minimal route example
```python
@router.post("/combinations", response_model=CombinationRead)
def add_combination(payload: CombinationCreate, db: Session = Depends(get_db)):
    row = create_combination(db, payload)
    commit_or_rollback(db)
    db.refresh(row)
    return row
```
Use your actual imports and route conventions. Add rollback handling consistently.

## Important limitations
- Starter code only; it has not been tested against your actual repository/database.
- The combination model currently has four roles (company, cost center, natural account, optional sub-account). Truly arbitrary segment counts require a normalized combination-child table and service redesign.
- Cross-validation is intentionally a small starter rule format, not a complete Oracle-equivalent rules engine.
- `create_balanced_journal` checks balance and duplicate source identifiers but production posting still needs tenant, currency, tax, period-lock, and concurrency controls.
- A unique `(source_type, source_id)` means one journal per source. Change this if your accounting design needs multiple journals per source.
- Store/location is not necessarily a legal entity. Do not use Chennai/Mumbai as separate balancing entities unless they represent separate legal/accounting entities.
- No existing POS files are overwritten by this ZIP.
