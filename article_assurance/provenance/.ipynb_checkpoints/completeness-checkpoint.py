from __future__ import annotations


class StructuralCompletenessScorer:

    @staticmethod
    def score(article):

        score = 1.0

        if len(article.content.strip()) < 400:
            score -= 0.25

        if len(article.summary.strip()) < 80:
            score -= 0.20

        if len(article.title.strip()) < 15:
            score -= 0.10

        return max(0.0, round(score, 4))