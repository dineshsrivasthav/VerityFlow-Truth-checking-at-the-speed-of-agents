from __future__ import annotations

from urllib.parse import urlparse


class HeuristicDomainScorer:

    TRUSTED_PATTERNS = [
        ".gov",
        ".gov.in",
        ".edu",
        ".org"
    ]

    @staticmethod
    def score(url: str) -> float:
        domain = urlparse(url).netloc.lower()

        score = 0.65

        for pattern in HeuristicDomainScorer.TRUSTED_PATTERNS:
            if domain.endswith(pattern):
                score += 0.20

        if "news" in domain:
            score += 0.05

        if domain.count(".") > 4:
            score -= 0.10

        return max(0.0, min(1.0, score))