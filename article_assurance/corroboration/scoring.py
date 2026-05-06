from __future__ import annotations


class CorroborationScorer:

    @staticmethod
    def final_score(
        diversity,
        similarity,
        nli,
        consensus
    ):

        return round(
            (0.20 * diversity)
            + (0.20 * similarity)
            + (0.35 * nli)
            + (0.25 * consensus),
            4
        )