"""Database-aware service functions; wire them into your existing FastAPI routers."""
from __future__ import annotations
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import (AccountCombination, AccountMapping, AccountSegment,
    CrossValidationRule, JournalEntry, JournalLine, SegmentValue, ValueSet)
from .schemas import (CombinationCreate, CrossValidationRuleCreate, JournalCreate,
    SegmentCreate, SegmentValueCreate, ValueSetCreate)

NORMAL_BALANCE_BY_TYPE = {
    "ASSET": "DEBIT", "EXPENSE": "DEBIT", "LIABILITY": "CREDIT",
    "EQUITY": "CREDIT", "REVENUE": "CREDIT",
}

def create_segment(db: Session, payload: SegmentCreate) -> AccountSegment:
    found = db.scalar(select(AccountSegment).where(
        (AccountSegment.code == payload.code) | (AccountSegment.sequence == payload.sequence)))
    if found:
        raise HTTPException(409, "Segment code or sequence already exists")
    row = AccountSegment(**payload.model_dump())
    db.add(row)
    db.flush()
    return row

def create_value_set(db: Session, payload: ValueSetCreate) -> ValueSet:
    code = payload.code.upper()
    if db.scalar(select(ValueSet).where(ValueSet.code == code)):
        raise HTTPException(409, "Value set code already exists")
    row = ValueSet(**{**payload.model_dump(), "code": code})
    db.add(row)
    db.flush()
    return row

def _validate_value_set(value_set: Optional[ValueSet], code: str) -> None:
    if value_set is None:
        return
    if not value_set.active:
        raise HTTPException(422, "Value set is inactive")
    if value_set.min_length is not None and len(code) < value_set.min_length:
        raise HTTPException(422, "Value is shorter than the value-set minimum")
    if value_set.max_length is not None and len(code) > value_set.max_length:
        raise HTTPException(422, "Value exceeds the value-set maximum")
    if (value_set.numeric_only or value_set.value_type in {"INTEGER", "NUMERIC"}) and not code.isdigit():
        raise HTTPException(422, "This value set accepts digits only")

def create_segment_value(db: Session, payload: SegmentValueCreate) -> SegmentValue:
    segment = db.get(AccountSegment, payload.segment_id)
    if not segment or not segment.active:
        raise HTTPException(422, "Segment does not exist or is inactive")
    if len(payload.code) != segment.code_length:
        raise HTTPException(422, f"Code must be exactly {segment.code_length} characters")
    if db.scalar(select(SegmentValue).where(
        SegmentValue.segment_id == payload.segment_id, SegmentValue.code == payload.code)):
        raise HTTPException(409, "This code already exists in the segment")
    value_set = None
    if payload.value_set_id:
        value_set = db.get(ValueSet, payload.value_set_id)
        if not value_set:
            raise HTTPException(422, "Value set does not exist")
        _validate_value_set(value_set, payload.code)
    data = payload.model_dump()
    if data.get("account_type"):
        expected = NORMAL_BALANCE_BY_TYPE[data["account_type"]]
        if data.get("normal_balance") != expected:
            raise HTTPException(422, f"{data['account_type']} normally has {expected} balance")
    row = SegmentValue(**data)
    db.add(row)
    db.flush()
    return row

def _active_value(db: Session, value_id: Optional[int], required: bool = True) -> Optional[SegmentValue]:
    if value_id is None:
        if required:
            raise HTTPException(422, "Required segment value is missing")
        return None
    value = db.get(SegmentValue, value_id)
    if not value or not value.active:
        raise HTTPException(422, f"Segment value {value_id} is missing or inactive")
    if value.effective_from and value.effective_from > date.today():
        raise HTTPException(422, f"Segment value {value.code} is not yet effective")
    if value.effective_to and value.effective_to < date.today():
        raise HTTPException(422, f"Segment value {value.code} has expired")
    if not value.allow_posting:
        raise HTTPException(422, f"Segment value {value.code} does not allow posting")
    return value

def _check_cross_validation(db: Session, cost_center: SegmentValue, natural: SegmentValue) -> None:
    rules = db.scalars(select(CrossValidationRule).where(CrossValidationRule.active.is_(True))).all()
    for rule in rules:
        if rule.cost_center_code and rule.cost_center_code != cost_center.code:
            continue
        if rule.allowed_natural_account_codes:
            allowed = {item.strip() for item in rule.allowed_natural_account_codes.split(",") if item.strip()}
            if natural.code not in allowed:
                raise HTTPException(422, f"Combination rejected by rule: {rule.name}")

def create_combination(db: Session, payload: CombinationCreate) -> AccountCombination:
    company = _active_value(db, payload.company_value_id)
    center = _active_value(db, payload.cost_center_value_id)
    natural = _active_value(db, payload.natural_account_value_id)
    sub = _active_value(db, payload.sub_account_value_id, required=False)
    if company.segment.qualifier not in {"PRIMARY_BALANCING", "OTHER"}:
        raise HTTPException(422, "Company value must use a primary-balancing segment")
    if center.segment.qualifier not in {"COST_CENTER", "OTHER"}:
        raise HTTPException(422, "Cost-center value must use a cost-center segment")
    if natural.segment.qualifier not in {"NATURAL_ACCOUNT", "OTHER"}:
        raise HTTPException(422, "Natural account value must use a natural-account segment")
    if sub and sub.segment_id in {company.segment_id, center.segment_id, natural.segment_id}:
        raise HTTPException(422, "Sub account must use a separate segment")
    _check_cross_validation(db, center, natural)
    values = [company, center, natural] + ([sub] if sub else [])
    code = "-".join(value.code for value in values)
    if db.scalar(select(AccountCombination).where(AccountCombination.combination_code == code)):
        raise HTTPException(409, "Account combination already exists")
    row = AccountCombination(
        company_value_id=company.id, cost_center_value_id=center.id,
        natural_account_value_id=natural.id, sub_account_value_id=sub.id if sub else None,
        combination_code=code, account_name=natural.name,
        description=payload.description, active=payload.active)
    db.add(row)
    db.flush()
    return row

def create_cross_validation_rule(db: Session, payload: CrossValidationRuleCreate) -> CrossValidationRule:
    data = payload.model_dump()
    allowed = data.pop("allowed_natural_account_codes")
    data["code"] = data["code"].upper()
    data["allowed_natural_account_codes"] = ",".join(sorted(set(allowed))) or None
    if db.scalar(select(CrossValidationRule).where(CrossValidationRule.code == data["code"])):
        raise HTTPException(409, "Cross-validation rule code already exists")
    row = CrossValidationRule(**data)
    db.add(row)
    db.flush()
    return row

def create_mapping(db: Session, event_code: str, payment_method: Optional[str],
                   debit_id: Optional[int], credit_id: Optional[int]) -> AccountMapping:
    if debit_id is None and credit_id is None:
        raise HTTPException(422, "At least one debit or credit account is required")
    for combination_id in (debit_id, credit_id):
        if combination_id is not None:
            combo = db.get(AccountCombination, combination_id)
            if not combo or not combo.active:
                raise HTTPException(422, f"Combination {combination_id} is missing or inactive")
    row = AccountMapping(event_code=event_code.upper(),
        payment_method=payment_method.upper() if payment_method else None,
        debit_combination_id=debit_id, credit_combination_id=credit_id, active=True)
    db.add(row)
    db.flush()
    return row

def create_balanced_journal(db: Session, payload: JournalCreate) -> JournalEntry:
    debit = sum((line.debit for line in payload.lines), Decimal("0.00"))
    credit = sum((line.credit for line in payload.lines), Decimal("0.00"))
    if debit != credit:
        raise HTTPException(422, "Journal debits and credits must balance")
    existing = db.scalar(select(JournalEntry).where(
        JournalEntry.source_type == payload.source_type, JournalEntry.source_id == payload.source_id))
    if existing:
        raise HTTPException(409, "A journal already exists for this source transaction")
    ids = {line.account_combination_id for line in payload.lines}
    active = db.scalars(select(AccountCombination).where(
        AccountCombination.id.in_(ids), AccountCombination.active.is_(True))).all()
    if len(active) != len(ids):
        raise HTTPException(422, "One or more account combinations are missing or inactive")
    entry = JournalEntry(source_type=payload.source_type, source_id=payload.source_id,
        description=payload.description, status="POSTED", posted_at=datetime.now(timezone.utc))
    for line in payload.lines:
        entry.lines.append(JournalLine(account_combination_id=line.account_combination_id,
            debit=line.debit, credit=line.credit, memo=line.memo))
    db.add(entry)
    db.flush()
    return entry

def commit_or_rollback(db: Session) -> None:
    """Call after service work at the API boundary; convert uniqueness races into HTTP 409."""
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "A conflicting accounting record already exists") from exc

def seed_basic_segments(db: Session) -> list[AccountSegment]:
    """Optional seed helper; only run when no matching segments already exist."""
    definitions = [
        ("COMPANY", "Company", 1, 3, "PRIMARY_BALANCING"),
        ("COST_CENTER", "Cost Center", 2, 3, "COST_CENTER"),
        ("NATURAL_ACCOUNT", "Natural Account", 3, 4, "NATURAL_ACCOUNT"),
        ("SUB_ACCOUNT", "Sub Account", 4, 3, "OTHER"),
    ]
    created = []
    for code, name, sequence, length, qualifier in definitions:
        if db.scalar(select(AccountSegment).where(AccountSegment.code == code)):
            continue
        row = AccountSegment(code=code, name=name, sequence=sequence, code_length=length,
            qualifier=qualifier, required=(code != "SUB_ACCOUNT"), active=True)
        db.add(row)
        created.append(row)
    db.flush()
    return created
