from __future__ import annotations


class ReputationScorer:

    @staticmethod
    def base_site_trust(
        url_score: float,
        domain_score: float,
        source_prior: float
    ) -> float:

        return round(
            (0.35 * url_score)
            + (0.40 * domain_score)
            + (0.25 * source_prior),
            4
        )

    @staticmethod
    def api_adjustment(api_score: float | None) -> float:
        if api_score is None:
            return 0.0

        if api_score >= 0.9:
            return 0.05

        if api_score >= 0.75:
            return 0.02

        if api_score >= 0.5:
            return -0.05

        return -0.15

    @staticmethod
    def final_score(
        base_score: float,
        api_adjustment: float
    ) -> float:

        return round(
            max(0.0, min(1.0, base_score + api_adjustment)),
            4
        )