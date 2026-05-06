from __future__ import annotations

import numpy as np


class OriginalityScorer:

    @staticmethod
    def score(article, cluster, context):

        article_idx = context["article_index"][article.article_id]

        cluster_indices = [
            context["article_index"][a.article_id]
            for a in cluster
        ]

        sims = context["similarity_matrix"][
            article_idx,
            cluster_indices
        ]

        sims = [
            s for idx, s in zip(cluster_indices, sims)
            if idx != article_idx
        ]

        if not sims:
            return 0.75

        mean_sim = np.mean(sims)

        if 0.75 <= mean_sim <= 0.92:
            return 1.0

        if mean_sim > 0.97:
            return 0.55

        if mean_sim < 0.55:
            return 0.40

        return 0.75