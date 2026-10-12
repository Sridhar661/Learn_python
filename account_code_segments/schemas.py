"""Pydantic v2 request/response schemas for Account Code Segment APIs."""
from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ACCOUNT_TYPES = {"ASSET", "LIABILITY", "EQUITY", "REVENUE", "EXPENSE"}
NORMAL_BALANCES = {"DEBIT", "CREDIT"}
QUALIFIERS = {"PRIMARY_BALANCING", "COST_CENTER", "NATURAL_ACCOUNT",
              "INTERCOMPANY", "SECOND_BALANCING", "OTHER"}

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class SegmentCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40, pattern=r"^[A-Z0-9_]+$")
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    sequence: int = Field(ge=1, le=20)
    code_length: int = Field(ge=1, le=40)
    required: bool = True
    qualifier: str = "OTHER"
    active: bool = True

    @field_validator("code")
    @classmethod
    def uppercase_code(cls, value: str) -> str:
        return value.upper()

    @field_validator("qualifier")
    @classmethod
    def validate_qualifier(cls, value: str) -> str:
        value = value.upper()
        if value not in QUALIFIERS:
            raise ValueError(f"qualifier must be one of {sorted(QUALIFIERS)}")
        return value

class SegmentRead(ORMModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    sequence: int
    code_length: int
    required: bool
    qualifier: str
    active: bool

class ValueSetCreate(BaseModel):
    code: str = Field(min_length=1, max_length=60, pattern=r"^[A-Za-z0-9_]+$")
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    value_type: Literal["STRING", "INTEGER", "NUMERIC"] = "STRING"
    min_length: Optional[int] = Field(default=None, ge=1, le=180)
    max_length: Optional[int] = Field(default=None, ge=1, le=180)
    numeric_only: bool = False
    active: bool = True

    @model_validator(mode="after")
    def validate_lengths(self):
        if self.min_length and self.max_length and self.min_length > self.max_length:
            raise ValueError("min_length cannot exceed max_length")
        return self

class ValueSetRead(ORMModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    value_type: str
    min_length: Optional[int]
    max_length: Optional[int]
    numeric_only: bool
    active: bool

class SegmentValueCreate(BaseModel):
    segment_id: int = Field(gt=0)
    value_set_id: Optional[int] = Field(default=None, gt=0)
    code: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    account_type: Optional[str] = None
    normal_balance: Optional[str] = None
    allow_posting: bool = True
    active: bool = True
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None

    @field_validator("account_type")
    @classmethod
    def validate_account_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.upper()
            if value not in ACCOUNT_TYPES:
                raise ValueError(f"account_type must be one of {sorted(ACCOUNT_TYPES)}")
        return value

    @field_validator("normal_balance")
    @classmethod
    def validate_normal_balance(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.upper()
            if value not in NORMAL_BALANCES:
                raise ValueError("normal_balance must be DEBIT or CREDIT")
        return value

    @model_validator(mode="after")
    def validate_dates_and_account_type(self):
        if self.effective_from and self.effective_to and self.effective_from > self.effective_to:
            raise ValueError("effective_from cannot be after effective_to")
        if self.account_type and not self.normal_balance:
            raise ValueError("normal_balance is required when account_type is provided")
        return self

class SegmentValueRead(ORMModel):
    id: int
    segment_id: int
    value_set_id: Optional[int]
    code: str
    name: str
    description: Optional[str]
    account_type: Optional[str]
    normal_balance: Optional[str]
    allow_posting: bool
    active: bool
    effective_from: Optional[date]
    effective_to: Optional[date]

class CombinationCreate(BaseModel):
    company_value_id: int = Field(gt=0)
    cost_center_value_id: int = Field(gt=0)
    natural_account_value_id: int = Field(gt=0)
    sub_account_value_id: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = None
    active: bool = True

class CombinationRead(ORMModel):
    id: int
    company_value_id: int
    cost_center_value_id: int
    natural_account_value_id: int
    sub_account_value_id: Optional[int]
    combination_code: str
    account_name: str
    description: Optional[str]
    active: bool

class CrossValidationRuleCreate(BaseModel):
    code: str = Field(min_length=1, max_length=60)
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    cost_center_code: Optional[str] = Field(default=None, max_length=40)
    allowed_natural_account_codes: list[str] = Field(default_factory=list, max_length=200)
    active: bool = True

class AccountMappingCreate(BaseModel):
    event_code: str = Field(min_length=1, max_length=60)
    payment_method: Optional[str] = Field(default=None, max_length=30)
    debit_combination_id: Optional[int] = Field(default=None, gt=0)
    credit_combination_id: Optional[int] = Field(default=None, gt=0)
    active: bool = True

    @model_validator(mode="after")
    def require_side(self):
        if self.debit_combination_id is None and self.credit_combination_id is None:
            raise ValueError("At least one debit or credit combination is required")
        return self

class JournalLineInput(BaseModel):
    account_combination_id: int = Field(gt=0)
    debit: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=14, decimal_places=2)
    credit: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=14, decimal_places=2)
    memo: Optional[str] = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def exactly_one_side(self):
        if (self.debit > 0) == (self.credit > 0):
            raise ValueError("Exactly one of debit or credit must be greater than zero")
        return self

class JournalCreate(BaseModel):
    source_type: str = Field(min_length=1, max_length=40)
    source_id: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=255)
    lines: list[JournalLineInput] = Field(min_length=2, max_length=500)

    @model_validator(mode="after")
    def journal_balances(self):
        debit = sum((line.debit for line in self.lines), Decimal("0.00"))
        credit = sum((line.credit for line in self.lines), Decimal("0.00"))
        if debit != credit:
            raise ValueError(f"Journal is not balanced: debit={debit}, credit={credit}")
        return self
