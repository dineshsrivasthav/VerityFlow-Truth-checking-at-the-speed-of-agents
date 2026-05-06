from __future__ import annotations

import re
from urllib.parse import urlparse


class URLValidator:

    SUSPICIOUS_TLDS = {
        ".xyz", ".top", ".biz", ".click", ".loan", ".gq"
    }

    @staticmethod
    def verify(url: str) -> float:
        try:
            parsed = urlparse(url)

            score = 1.0

            if parsed.scheme != "https":
                score -= 0.20

            domain = parsed.netloc

            if len(domain) > 50:
                score -= 0.10

            if domain.count("-") > 3:
                score -= 0.15

            for tld in URLValidator.SUSPICIOUS_TLDS:
                if domain.endswith(tld):
                    score -= 0.30

            if re.search(r"\d{4,}", domain):
                score -= 0.10

            return max(0.0, score)

        except Exception:
            return 0.0