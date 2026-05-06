from __future__ import annotations

import networkx as nx


class EvidenceGraphBuilder:

    @staticmethod
    def build(cluster, context):

        graph = nx.DiGraph()

        for article in cluster:
            graph.add_node(article.article_id)

        for a in cluster:
            for b in cluster:

                if a.article_id == b.article_id:
                    continue

                ai = context["article_index"][a.article_id]
                bi = context["article_index"][b.article_id]

                score = context["nli_matrix"][ai][bi]

                graph.add_edge(
                    a.article_id,
                    b.article_id,
                    weight=score
                )

        return graph