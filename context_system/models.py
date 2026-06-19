from __future__ import annotations

import warnings
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

warnings.filterwarnings("ignore", message='Field name "construct".*shadows an attribute')

Criticality = Literal["flexible", "hybrid", "controlled"]
Durability = Literal["ephemeral", "time_bound", "persistent"]
Provenance = Literal["original", "derived", "outcome", "observed"]
RecordStatus = Literal["draft", "proposed", "approved", "archived"]
RetrievalPolicy = Literal["connector_search", "hybrid", "deterministic"]


class Scope(BaseModel):
    company: Optional[str] = None
    brand: Optional[str] = None
    product: Optional[str] = None
    market: Optional[str] = None
    jurisdiction: Optional[str] = None
    audience: Optional[str] = None
    channel: Optional[str] = None
    campaign: Optional[str] = None
    asset: Optional[str] = None
    account: Optional[str] = None


class ScopeNode(BaseModel):
    id: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    name: str = Field(min_length=1)
    level: Literal["company", "brand", "product", "market", "campaign", "audience", "channel", "custom"]
    parent_id: Optional[str] = None
    order: int = Field(default=0, ge=0)


class SourceRef(BaseModel):
    id: str
    connector: Optional[str] = None
    url: Optional[str] = None


class GovernanceMetadata(BaseModel):
    construct: Optional[str] = None
    scope_id: Optional[str] = None
    durability: Optional[Durability] = None
    provenance: Optional[str] = None
    provenance_type: Optional[Provenance] = None
    criticality: Optional[Criticality] = None
    owner_role: Optional[str] = None
    read_roles: Optional[list[str]] = None
    edit_roles: Optional[list[str]] = None
    approver_role: Optional[str] = None
    status: Optional[RecordStatus] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    retrieval_policy: Optional[RetrievalPolicy] = None
    audit_required: Optional[bool] = None
    exact_language: Optional[bool] = None
    staleness_threshold_days: Optional[int] = Field(default=None, ge=1)
    date_verified: Optional[date] = None

    model_config = {"extra": "allow"}

    @model_validator(mode="after")
    def _validate_dates_and_controlled_context(self) -> "GovernanceMetadata":
        if self.durability == "time_bound" and (not self.valid_from or not self.valid_until):
            raise ValueError("time-bound context requires valid_from and valid_until")
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValueError("valid_until must be on or after valid_from")
        if self.criticality == "controlled" and not self.approver_role:
            raise ValueError("controlled context requires approver_role")
        return self


class ContextRecord(BaseModel):
    id: str
    title: str
    construct: str
    description: str = ""
    scope: Scope = Field(default_factory=Scope)
    scope_id: Optional[str] = None
    durability: Durability = "persistent"
    provenance: Optional[str] = None
    provenance_type: Provenance = "original"
    criticality: Criticality = "hybrid"
    owner_role: str
    read_roles: list[str] = Field(default_factory=list)
    edit_roles: list[str] = Field(default_factory=list)
    approver_role: Optional[str] = None
    status: RecordStatus = "approved"
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    source_refs: list[SourceRef] = Field(default_factory=list)
    retrieval_policy: RetrievalPolicy = "hybrid"
    precedence: list[str] = Field(default_factory=list)
    audit_required: bool = False
    exact_language: bool = False
    kb_glob: str = ""
    staleness_threshold_days: int = Field(default=90, ge=1)
    date_verified: Optional[date] = None
    checks: dict = Field(default_factory=dict)
    okf_type: str = "Marketing Context"
    resource: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_governance(self) -> "ContextRecord":
        if self.criticality == "controlled" and not self.approver_role:
            raise ValueError(f"controlled record {self.id} needs an approver_role")
        if self.criticality == "controlled":
            self.audit_required = True
        return self


class RuntimeRecord(BaseModel):
    id: str
    title: str
    construct: str
    durability: Durability
    provenance: Optional[str] = None
    criticality: Criticality
    retrieval_policy: RetrievalPolicy
    status: RecordStatus
    exact_language: bool
    kb_path: str
    content_hash: str
    staleness_threshold_days: int
    date_verified: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    owner_role: str
    approver_role: Optional[str] = None
    read_roles: list[str] = Field(default_factory=list)
    edit_roles: list[str] = Field(default_factory=list)
    scope: dict = Field(default_factory=dict)
    scope_id: Optional[str] = None
    checks: dict = Field(default_factory=dict)
    source_refs: list[dict] = Field(default_factory=list)
    okf: dict = Field(default_factory=dict)
    body: str = ""


class SearchPointer(BaseModel):
    record_id: str
    kb_path: str
    score: float
    construct: str


class StalenessFlag(BaseModel):
    record_id: str
    days_overdue: int
    message: str


class MissingContextBlock(BaseModel):
    construct: str
    reason: str
    blocks_workflow: bool = True


class ContextPackage(BaseModel):
    task: str
    records: list[dict] = Field(default_factory=list)
    exact_language_map: dict[str, str] = Field(default_factory=dict)
    search_pointers: list[SearchPointer] = Field(default_factory=list)
    staleness_flags: list[StalenessFlag] = Field(default_factory=list)
    missing_blocks: list[MissingContextBlock] = Field(default_factory=list)
    kb_git_sha: str = "uncommitted"

    @property
    def blocked(self) -> bool:
        return any(block.blocks_workflow for block in self.missing_blocks)

    def to_response(self) -> dict:
        data = self.model_dump()
        data["blocked"] = self.blocked
        return data

    def checks_for(self, construct: str, key: str) -> list:
        values: list = []
        for record in self.records:
            if record.get("construct") == construct:
                values.extend(record.get("checks", {}).get(key, []))
        return values
