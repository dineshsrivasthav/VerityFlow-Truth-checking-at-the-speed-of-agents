from __future__ import annotations

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


class SemanticContext:

    def __init__(
        self,
        embedding_model: str,
        nli_model: str
    ):
        self.embedding_model = SentenceTransformer(
            embedding_model
        )

        self.nli = pipeline(
            "text-classification",
            model=nli_model
        )

    def build(self, articles):

        texts = [
            f"{a.title} {a.summary}"
            for a in articles
        ]

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True
        )

        sim_matrix = cosine_similarity(
            embeddings
        )

        article_index = {
            article.article_id: idx
            for idx, article in enumerate(articles)
        }

        nli_matrix = self._build_nli_matrix(
            articles
        )

        return {
            "embeddings": embeddings,
            "similarity_matrix": sim_matrix,
            "article_index": article_index,
            "nli_matrix": nli_matrix
        }

    def _build_nli_matrix(self, articles):

        n = len(articles)

        matrix = [[0.0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):

                if i == j:
                    continue

                result = self.nli(
                    f"{articles[i].summary} [SEP] {articles[j].summary}"
                )

                scores = {}
                for r in result:
                    label = r["label"]

                    if label == "LABEL_0":
                        mapped = "contradiction"
                    elif label == "LABEL_2":
                        mapped = "entailment"
                    else:
                        mapped = "neutral"

                    scores[mapped] = r["score"]

                entailment = scores.get("entailment", 0)
                contradiction = scores.get("contradiction", 0)

                matrix[i][j] = entailment - contradiction

        return matrix