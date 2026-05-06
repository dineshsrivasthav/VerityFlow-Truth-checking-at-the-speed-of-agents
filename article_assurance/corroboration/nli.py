from __future__ import annotations


class NLIScorer:

    LABEL_MAP = {
        "LABEL_0": "contradiction",
        "LABEL_1": "neutral",
        "LABEL_2": "entailment"
    }

    @classmethod
    def article_score(cls, article, cluster, context):

        article_idx = context["article_index"][article.article_id]

        cluster_indices = [
            context["article_index"][a.article_id]
            for a in cluster
        ]

        scores = [
            context["nli_matrix"][article_idx][idx]
            for idx in cluster_indices
            if idx != article_idx
        ]

        if not scores:
            return 0.5

        avg = sum(scores) / len(scores)

        return round((avg + 1) / 2, 4)