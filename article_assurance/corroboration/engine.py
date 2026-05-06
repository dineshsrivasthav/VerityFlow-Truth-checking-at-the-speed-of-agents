from __future__ import annotations

from article_assurance.core.models import (
    CrossSourceCorroborationScore
)

from .diversity import SourceDiversityScorer
from .similarity import SimilarityScorer
from .nli import NLIScorer
from .graph_builder import EvidenceGraphBuilder
from .consensus import GraphConsensusScorer
from .scoring import CorroborationScorer


class CorroborationEngine:

    def _cluster(self, article, articles):
        return [
            a for a in articles
            if abs(
                (a.event_date - article.event_date).days
            ) <= 2
        ]

    def score(self, article, articles, context):

        cluster = self._cluster(article, articles)

        diversity = SourceDiversityScorer.score(cluster)

        similarity = SimilarityScorer.score(
            article,
            cluster,
            context
        )

        nli = NLIScorer.article_score(
            article,
            cluster,
            context
        )

        graph = EvidenceGraphBuilder.build(
            cluster,
            context
        )

        consensus = GraphConsensusScorer.score(
            article,
            graph
        )

        final = CorroborationScorer.final_score(
            diversity,
            similarity,
            nli,
            consensus
        )

        return CrossSourceCorroborationScore(
            source_diversity=diversity,
            inter_article_similarity=similarity,
            nli_support=nli,
            graph_consensus=consensus,
            score=final
        )