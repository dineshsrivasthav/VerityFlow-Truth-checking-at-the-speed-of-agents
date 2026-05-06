from __future__ import annotations


class SourceDiversityScorer:

    @staticmethod
    def score(cluster):

        unique_publishers = {
            a.publisher.lower()
            for a in cluster
        }

        diversity = len(unique_publishers) / max(len(cluster), 1)

        return round(min(diversity, 1.0), 4)