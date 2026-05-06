from __future__ import annotations

from typing import List

from article_assurance.core.models import (
    AssuranceInput,
    AssuranceOutput,
    ValidationDecision,
    ArticleValidationReport
)
from article_assurance.core.context import SemanticContext
from article_assurance.core.normalizer import ArticleNormalizer
from article_assurance.core.config import AssuranceConfig


class ArticleAssuranceEngine:

    def __init__(
        self,
        reputation_engine,
        provenance_engine,
        corroboration_engine,
        config: AssuranceConfig = AssuranceConfig()
    ):
        self.reputation_engine = reputation_engine
        self.provenance_engine = provenance_engine
        self.corroboration_engine = corroboration_engine
        self.semantic_context = SemanticContext(config.EMBEDDING_MODEL, config.NLI_MODEL)
        self.config = config

    def _compute_final_score(self, pr, po, cs):
        return (
            pr.score * self.config.PUBLISHER_WEIGHT
            + po.score * self.config.PROVENANCE_WEIGHT
            + cs.score * self.config.CORROBORATION_WEIGHT
        )

    def _decision(self, score, pr, cs):

        if (
            score >= 0.68
            and pr.score >= 0.60
            and cs.score >= 0.45
        ):
            return ValidationDecision.VALID

        if score >= 0.50:
            return ValidationDecision.UNCERTAIN

        return ValidationDecision.INVALID

    def assess(self, payload: AssuranceInput) -> AssuranceOutput:
        normalized_articles = ArticleNormalizer.normalize(payload)
        reports = []
        context = self.semantic_context.build(normalized_articles)

        for article in normalized_articles:

            pr = self.reputation_engine.score(article)
            po = self.provenance_engine.score(article, normalized_articles, context)
            cs = self.corroboration_engine.score(article, normalized_articles, context)

            final_score = self._compute_final_score(pr, po, cs)
            decision = self._decision(final_score, pr, cs)

            reports.append(
                ArticleValidationReport(
                    article_id=article.article_id,
                    source_type=article.source_type,
                    publisher_reputation=pr,
                    provenance_originality=po,
                    cross_source_corroboration=cs,
                    final_trust_score=round(final_score, 4),
                    decision=decision,
                    is_valid=decision == ValidationDecision.VALID
                )
            )

        return AssuranceOutput(
            query=payload.query,
            event_date=payload.event_date,
            validated_articles=reports
        )