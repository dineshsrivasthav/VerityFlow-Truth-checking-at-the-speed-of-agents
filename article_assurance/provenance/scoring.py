from __future__ import annotations


class ProvenanceScorer:

    @staticmethod
    def final_score(
        lineage: float,
        temporal: float,
        originality: float,
        completeness: float
    ):

        return round(
            (0.30 * lineage)
            + (0.30 * temporal)
            + (0.25 * originality)
            + (0.15 * completeness),
            4
        )