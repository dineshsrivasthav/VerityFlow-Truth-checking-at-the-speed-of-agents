from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, HttpUrl, Field, validator


# ============================================================
# ENUMS
# ============================================================

class SourceType(str, Enum):
    NEWS = "news"
    GOVERNMENT = "government"
    TRADE_BODY = "trade_bodies"


class ValidationDecision(str, Enum):
    VALID = "valid"
    UNCERTAIN = "uncertain"
    INVALID = "invalid"


# ============================================================
# INPUT ARTICLE MODELS
# ============================================================

class BaseArticle(BaseModel):
    title: str
    event_date: date
    date_published: datetime
    content: str
    summary: str
    url: HttpUrl

    @validator("title", "content", "summary")
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class NewsArticle(BaseArticle):
    source: str


class GovernmentArticle(BaseArticle):
    issuer: str


class TradeBodyArticle(BaseArticle):
    organization: str


# ============================================================
# INPUT ROOT SCHEMA
# ============================================================

class AssuranceInput(BaseModel):
    query: str
    event_date: date
    news: List[NewsArticle] = Field(default_factory=list)
    government: List[GovernmentArticle] = Field(default_factory=list)
    trade_bodies: List[TradeBodyArticle] = Field(default_factory=list)

    @validator("query")
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


# ============================================================
# NORMALIZED ARTICLE
# ============================================================

class NormalizedArticle(BaseModel):
    article_id: str
    source_type: SourceType
    publisher: str

    title: str
    event_date: date
    date_published: datetime
    content: str
    summary: str
    url: HttpUrl


# ============================================================
# SCORE MODELS
# ============================================================

class PublisherReputationScore(BaseModel):
    url_verification: float
    domain_verification: float
    site_trustworthiness: float
    score: float


class ProvenanceOriginalityScore(BaseModel):
    lineage_score: float
    temporal_score: float
    content_originality: float
    structural_completeness: float
    score: float


class CrossSourceCorroborationScore(BaseModel):
    source_diversity: float
    inter_article_similarity: float
    nli_support: float
    graph_consensus: float
    score: float


# ============================================================
# FINAL REPORT
# ============================================================

class ArticleValidationReport(BaseModel):
    article_id: str
    source_type: SourceType

    publisher_reputation: PublisherReputationScore
    provenance_originality: ProvenanceOriginalityScore
    cross_source_corroboration: CrossSourceCorroborationScore

    final_trust_score: float
    decision: ValidationDecision
    is_valid: bool


class AssuranceOutput(BaseModel):
    query: str
    event_date: date
    validated_articles: List[ArticleValidationReport]