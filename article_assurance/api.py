from __future__ import annotations

from article_assurance.core.models import (
    AssuranceInput
)
from article_assurance.engine.assessor import (
    ArticleAssuranceEngine
)

from article_assurance.reputation.engine import ReputationEngine
from article_assurance.provenance.engine import ProvenanceEngine
from article_assurance.corroboration.engine import CorroborationEngine


class AssuranceService:

    def __init__(self):

        self.engine = ArticleAssuranceEngine(
            reputation_engine=ReputationEngine(),
            provenance_engine=ProvenanceEngine(),
            corroboration_engine=CorroborationEngine()
        )

    def assess(self, payload: dict):

        validated = AssuranceInput(**payload)

        result = self.engine.assess(validated)

        return result.dict()