from __future__ import annotations

import numpy as np


class SimilarityScorer:

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
            return 0.5

        mean_sim = np.mean(sims)

        # Optimal corroboration band
        if 0.78 <= mean_sim <= 0.92:
            return 1.0

        if mean_sim > 0.97:
            return 0.65

        if mean_sim < 0.60:
            return 0.35

        return 0.75