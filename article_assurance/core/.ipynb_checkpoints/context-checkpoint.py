from __future__ import annotations

from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingContext:

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def build(self, articles):

        texts = [
            f"{a.title} {a.summary}"
            for a in articles
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        sim_matrix = cosine_similarity(embeddings)

        article_index = {
            article.article_id: idx
            for idx, article in enumerate(articles)
        }

        return {
            "embeddings": embeddings,
            "similarity_matrix": sim_matrix,
            "article_index": article_index
        }