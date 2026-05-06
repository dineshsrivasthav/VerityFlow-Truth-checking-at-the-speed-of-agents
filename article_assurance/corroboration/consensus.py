from __future__ import annotations


class GraphConsensusScorer:

    @staticmethod
    def score(article, graph):

        incoming = graph.in_edges(
            article.article_id,
            data=True
        )

        if not incoming:
            return 0.5

        weights = [
            edge[2]["weight"]
            for edge in incoming
        ]

        avg = sum(weights) / len(weights)

        return round((avg + 1) / 2, 4)