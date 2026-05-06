from __future__ import annotations

import re


class LineageScorer:

    DERIVATIVE_PATTERNS = [
        r"according to",
        r"as reported by",
        r"reported earlier by",
        r"via Reuters",
        r"via AP",
        r"citing"
    ]

    @classmethod
    def derivative_penalty(cls, text: str):

        lowered = text.lower()

        matches = sum(
            1 for pattern in cls.DERIVATIVE_PATTERNS
            if re.search(pattern, lowered)
        )

        return min(matches * 0.15, 0.45)

    @classmethod
    def score(cls, article, cluster):

        score = 1.0

        earliest = min(
            a.date_published
            for a in cluster
        )

        delay_hours = (
            article.date_published - earliest
        ).total_seconds() / 3600

        if delay_hours > 24:
            score -= 0.20
        elif delay_hours > 6:
            score -= 0.10

        derivative_penalty = cls.derivative_penalty(
            article.content
        )

        score -= derivative_penalty

        return max(0.0, round(score, 4))