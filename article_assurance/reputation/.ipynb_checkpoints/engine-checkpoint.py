async def _news_score_async(self, article):

    url_score = URLValidator.verify(str(article.url))
    domain_score = HeuristicDomainScorer.score(str(article.url))

    source_prior = 0.65

    base_trust = ReputationScorer.base_site_trust(
        url_score,
        domain_score,
        source_prior
    )

    api_score = None

    try:
        api_data = await self.client.check_domain(str(article.url))
        api_score = ReputationScorer.domain_verification_from_api(api_data)
    except APIVoidError:
        pass

    adjustment = ReputationScorer.api_adjustment(api_score)

    final = ReputationScorer.final_score(
        base_trust,
        adjustment
    )

    return PublisherReputationScore(
        url_verification=round(url_score, 4),
        domain_verification=round(domain_score, 4),
        site_trustworthiness=round(base_trust, 4),
        score=final
    )