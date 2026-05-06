from __future__ import annotations

from article_assurance.core.config import AssuranceConfig
from article_assurance.core.models import (
    ProvenanceOriginalityScore
)

from .temporal import TemporalScorer
from .lineage import LineageScorer
from .completeness import StructuralCompletenessScorer
from .originality import OriginalityScorer
from .scoring import ProvenanceScorer


class ProvenanceEngine:

    def _cluster(self, article, articles):
        return [
            a for a in articles
            if abs(
                (a.event_date - article.event_date).days
            ) <= 2
        ]

    def score(self, article, articles, context):

        cluster = self._cluster(article, articles)

        lineage = LineageScorer.score(article, cluster)

        temporal = TemporalScorer.score(article, cluster)

        originality = OriginalityScorer.score(
            article,
            cluster,
            context
        )

        completeness = StructuralCompletenessScorer.score(
            article
        )

        final = ProvenanceScorer.final_score(
            lineage,
            temporal,
            originality,
            completeness
        )

        return ProvenanceOriginalityScore(
            lineage_score=lineage,
            temporal_score=temporal,
            content_originality=originality,
            structural_completeness=completeness,
            score=final
        )