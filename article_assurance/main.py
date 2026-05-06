from article_assurance.engine.assessor import ArticleAssuranceEngine

# engines implemented next
from article_assurance.reputation.engine import ReputationEngine
from article_assurance.provenance.engine import ProvenanceEngine
from article_assurance.corroboration.engine import CorroborationEngine


engine = ArticleAssuranceEngine(
    reputation_engine=ReputationEngine(),
    provenance_engine=ProvenanceEngine(),
    corroboration_engine=CorroborationEngine()
)