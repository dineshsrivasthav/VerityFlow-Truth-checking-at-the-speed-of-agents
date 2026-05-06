from __future__ import annotations

from datetime import datetime


class TemporalScorer:

    @staticmethod
    def score(article, cluster):

        score = 1.0

        # Published before event
        if article.date_published.date() < article.event_date:
            score -= 0.45

        # Compare temporal deviation from cluster
        cluster_times = [
            a.date_published.timestamp()
            for a in cluster
        ]

        if cluster_times:
            avg = sum(cluster_times) / len(cluster_times)

            deviation_hours = abs(
                article.date_published.timestamp() - avg
            ) / 3600

            if deviation_hours > 72:
                score -= 0.25
            elif deviation_hours > 24:
                score -= 0.10

        return max(0.0, round(score, 4))