from __future__ import annotations

import hashlib
from typing import List

from .models import (
    AssuranceInput,
    NormalizedArticle,
    SourceType
)


class ArticleNormalizer:

    @staticmethod
    def _generate_id(title: str, publisher: str) -> str:
        raw = f"{title}:{publisher}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @classmethod
    def normalize(cls, payload: AssuranceInput) -> List[NormalizedArticle]:
        normalized = []

        for article in payload.news:
            normalized.append(
                NormalizedArticle(
                    article_id=cls._generate_id(article.title, article.source),
                    source_type=SourceType.NEWS,
                    publisher=article.source,
                    **article.dict(exclude={"source"})
                )
            )

        for article in payload.government:
            normalized.append(
                NormalizedArticle(
                    article_id=cls._generate_id(article.title, article.issuer),
                    source_type=SourceType.GOVERNMENT,
                    publisher=article.issuer,
                    **article.dict(exclude={"issuer"})
                )
            )

        for article in payload.trade_bodies:
            normalized.append(
                NormalizedArticle(
                    article_id=cls._generate_id(article.title, article.organization),
                    source_type=SourceType.TRADE_BODY,
                    publisher=article.organization,
                    **article.dict(exclude={"organization"})
                )
            )

        return normalized