import numpy as np

class ArticleRecommender(object):

    def __init__(self, match_affinity, other_articles):
        match_affinity = np.array(match_affinity)
        self.base_norm = match_affinity / np.linalg.norm(match_affinity)
        self.other_articles = other_articles

    def recommend(self, limit, exclude_ids=[]):
        ranked = [
            (self.similarity(article), article_id)
            for article_id, article in self.other_articles.items()
            if article_id not in exclude_ids
        ]
        return [
            pair[1]
            for pair in reversed(sorted(ranked))
        ][:10] #TODO inefficient

    def similarity(self, article):
        comp = np.array(article["classification"])
        comp = comp / np.linalg.norm(comp)
        return self.base_norm.dot(comp)
