from __future__ import annotations

import asyncio

from article_assurance.core.models import (
    PublisherReputationScore,
    SourceType
)
from article_assurance.core.config import AssuranceConfig

from .apivoid_client import APIVoidClient, APIVoidError
from .url_validator import URLValidator
from .fallback import HeuristicDomainScorer
from .scoring import ReputationScorer


class ReputationEngine:

    def __init__(self, config: AssuranceConfig = AssuranceConfig()):
        self.config = config
        self.client = APIVoidClient(config.APIVOID_API_KEY)

    def _government_score(self, article):
        return PublisherReputationScore(
            url_verification=1.0,
            domain_verification=0.95,
            site_trustworthiness=0.95,
            score=0.96
        )

    def _trade_body_score(self, article):
        return PublisherReputationScore(
            url_verification=0.95,
            domain_verification=0.85,
            site_trustworthiness=0.88,
            score=0.89
        )

    async def _news_score_async(self, article):

        url_score = URLValidator.verify(str(article.url))
        domain_score = HeuristicDomainScorer.score(str(article.url))

        source_prior = 0.65

        base_trust = ReputationScorer.base_site_trust(
            url_score,
            domain_score,
            source_prior
        )

        api_score = None

        try:
            api_data = await self.client.check_domain(str(article.url))
            api_score = ReputationScorer.domain_verification_from_api(api_data)
        except APIVoidError:
            pass

        adjustment = ReputationScorer.api_adjustment(api_score)

        final = ReputationScorer.final_score(
            base_trust,
            adjustment
        )

        return PublisherReputationScore(
            url_verification=round(url_score, 4),
            domain_verification=round(domain_score, 4),
            site_trustworthiness=round(base_trust, 4),
            score=final
        )

    def score(self, article):

        if article.source_type == SourceType.GOVERNMENT:
            return self._government_score(article)

        if article.source_type == SourceType.TRADE_BODY:
            return self._trade_body_score(article)

        return asyncio.run(self._news_score_async(article))