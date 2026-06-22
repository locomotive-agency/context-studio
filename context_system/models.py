from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

Criticality = Literal["flexible", "hybrid", "controlled"]
Durability = Literal["ephemeral", "time_bound", "persistent"]
RecordStatus = Literal["draft", "proposed", "approved", "archived"]


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


class GovernanceMetadata(BaseModel):
    type: Optional[str] = None
    scope_id: Optional[str] = None
    durability: Optional[Durability] = None
    provenance: Optional[str] = None
    criticality: Optional[Criticality] = None
    status: Optional[RecordStatus] = None
    valid_until: Optional[date] = None

    model_config = {"extra": "allow"}

    @model_validator(mode="after")
    def _validate_dates_and_controlled_context(self) -> "GovernanceMetadata":
        if self.durability == "time_bound" and not self.valid_until:
            raise ValueError("time-bound context requires valid_until")
        return self


class ContextRecord(BaseModel):
    id: str
    title: str
    type: str
    description: str = ""
    scope: Scope = Field(default_factory=Scope)
    scope_id: Optional[str] = None
    durability: Durability = "persistent"
    provenance: Optional[str] = None
    criticality: Criticality = "hybrid"
    status: RecordStatus = "approved"
    valid_until: Optional[date] = None
    precedence: list[str] = Field(default_factory=list)
    kb_glob: str = ""
    checks: dict = Field(default_factory=dict)
    resource: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    supporting_sources: dict[str, list[str]] = Field(default_factory=dict)


class RuntimeRecord(BaseModel):
    id: str
    title: str
    type: str
    durability: Durability
    provenance: Optional[str] = None
    criticality: Criticality
    status: RecordStatus
    kb_path: str
    content_hash: str
    valid_until: Optional[str] = None
    scope: dict = Field(default_factory=dict)
    scope_id: Optional[str] = None
    checks: dict = Field(default_factory=dict)
    okf: dict = Field(default_factory=dict)
    supporting_sources: dict[str, list[str]] = Field(default_factory=dict)
    links: list[dict] = Field(default_factory=list)
    external_links: list[dict] = Field(default_factory=list)
    citations: list[dict] = Field(default_factory=list)
    headings: list[dict] = Field(default_factory=list)
    body: str = ""


class SearchPointer(BaseModel):
    record_id: str
    kb_path: str
    score: float
    type: str
