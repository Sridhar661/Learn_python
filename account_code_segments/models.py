"""SQLAlchemy 2.x models for a POS Chart of Accounts starter.
In an existing app, replace the Base declaration with your project's shared Base import.
"""
from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import (Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index,
    Integer, Numeric, String, Text, UniqueConstraint, func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Replace with the existing project's Base; do not create a second Base in production."""

class AccountSegment(Base):
    __tablename__ = "coa_segments"
    __table_args__ = (
        UniqueConstraint("code", name="uq_coa_segments_code"),
        UniqueConstraint("sequence", name="uq_coa_segments_sequence"),
        CheckConstraint("sequence > 0", name="ck_coa_segment_sequence"),
        CheckConstraint("code_length > 0", name="ck_coa_segment_code_length"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    code_length: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    qualifier: Mapped[str] = mapped_column(String(40), nullable=False, default="OTHER")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    values: Mapped[list["SegmentValue"]] = relationship(back_populates="segment")

class ValueSet(Base):
    __tablename__ = "coa_value_sets"
    __table_args__ = (UniqueConstraint("code", name="uq_coa_value_sets_code"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(60), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    value_type: Mapped[str] = mapped_column(String(20), nullable=False, default="STRING")
    min_length: Mapped[Optional[int]] = mapped_column(Integer)
    max_length: Mapped[Optional[int]] = mapped_column(Integer)
    numeric_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class SegmentValue(Base):
    __tablename__ = "coa_segment_values"
    __table_args__ = (
        UniqueConstraint("segment_id", "code", name="uq_coa_segment_value_code"),
        Index("ix_coa_segment_values_segment_active", "segment_id", "active"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    segment_id: Mapped[int] = mapped_column(ForeignKey("coa_segments.id"), nullable=False)
    value_set_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coa_value_sets.id"))
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    account_type: Mapped[Optional[str]] = mapped_column(String(20))
    normal_balance: Mapped[Optional[str]] = mapped_column(String(6))
    allow_posting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    effective_from: Mapped[Optional[date]] = mapped_column(Date)
    effective_to: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    segment: Mapped[AccountSegment] = relationship(back_populates="values")
    value_set: Mapped[Optional[ValueSet]] = relationship()

class AccountCombination(Base):
    __tablename__ = "coa_account_combinations"
    __table_args__ = (
        UniqueConstraint("combination_code", name="uq_coa_combination_code"),
        UniqueConstraint("company_value_id", "cost_center_value_id", "natural_account_value_id",
                         "sub_account_value_id", name="uq_coa_combination_segments"),
        Index("ix_coa_combinations_natural_account", "natural_account_value_id"),
        CheckConstraint("length(combination_code) > 0", name="ck_coa_combination_code"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_value_id: Mapped[int] = mapped_column(ForeignKey("coa_segment_values.id"), nullable=False)
    cost_center_value_id: Mapped[int] = mapped_column(ForeignKey("coa_segment_values.id"), nullable=False)
    natural_account_value_id: Mapped[int] = mapped_column(ForeignKey("coa_segment_values.id"), nullable=False)
    sub_account_value_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coa_segment_values.id"))
    combination_code: Mapped[str] = mapped_column(String(180), nullable=False)
    account_name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    company_value: Mapped[SegmentValue] = relationship(foreign_keys=[company_value_id])
    cost_center_value: Mapped[SegmentValue] = relationship(foreign_keys=[cost_center_value_id])
    natural_account_value: Mapped[SegmentValue] = relationship(foreign_keys=[natural_account_value_id])
    sub_account_value: Mapped[Optional[SegmentValue]] = relationship(foreign_keys=[sub_account_value_id])

class CrossValidationRule(Base):
    __tablename__ = "coa_cross_validation_rules"
    __table_args__ = (UniqueConstraint("code", name="uq_coa_cross_validation_rule_code"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(60), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    cost_center_code: Mapped[Optional[str]] = mapped_column(String(40))
    allowed_natural_account_codes: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AccountMapping(Base):
    __tablename__ = "coa_account_mappings"
    __table_args__ = (
        UniqueConstraint("event_code", "payment_method", name="uq_coa_mapping_event_payment"),
        Index("ix_coa_mapping_event_active", "event_code", "active"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_code: Mapped[str] = mapped_column(String(60), nullable=False)
    payment_method: Mapped[Optional[str]] = mapped_column(String(30))
    debit_combination_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coa_account_combinations.id"))
    credit_combination_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coa_account_combinations.id"))
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    debit_combination: Mapped[Optional[AccountCombination]] = relationship(foreign_keys=[debit_combination_id])
    credit_combination: Mapped[Optional[AccountCombination]] = relationship(foreign_keys=[credit_combination_id])

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    __table_args__ = (
        UniqueConstraint("source_type", "source_id", name="uq_journal_source"),
        Index("ix_journal_entries_posted_at", "posted_at"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_type: Mapped[str] = mapped_column(String(40), nullable=False)
    source_id: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="DRAFT")
    posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    lines: Mapped[list["JournalLine"]] = relationship(back_populates="entry", cascade="all, delete-orphan")

class JournalLine(Base):
    __tablename__ = "journal_lines"
    __table_args__ = (
        CheckConstraint("debit >= 0 AND credit >= 0", name="ck_journal_line_nonnegative"),
        CheckConstraint("NOT (debit > 0 AND credit > 0)", name="ck_journal_line_one_side"),
        Index("ix_journal_lines_combination", "account_combination_id"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), nullable=False)
    account_combination_id: Mapped[int] = mapped_column(ForeignKey("coa_account_combinations.id"), nullable=False)
    debit: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=Decimal("0.00"))
    credit: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=Decimal("0.00"))
    memo: Mapped[Optional[str]] = mapped_column(String(255))
    entry: Mapped[JournalEntry] = relationship(back_populates="lines")
    combination: Mapped[AccountCombination] = relationship()































# Integration reminders:
# Import the existing database Base rather than defining a second one.
# Review tenant scoping and authorization before exposing these functions.
# Use Alembic migrations; do not create production tables automatically.
# Test uniqueness, cross-validation, journal balance, and retry behavior.
# Confirm legal entity versus store/location semantics with the business.
# Configure tax and accounting mappings according to actual policy.
# Existing historical GL records must remain readable after deactivation.
# This starter has fixed combination roles; arbitrary segments need a child-row design.
# See README.md for integration steps and known limitations.
