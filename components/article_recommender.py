import numpy as np

class ArticleRecommender(object):

    def __init__(self, base_article, other_articles):
        self.base_article = base_article
        self.base_id = base_article["id"]
        self.base_norm = np.array(base_article["classification"])
        self.base_norm = self.base_norm / np.linalg.norm(self.base_norm)
        self.other_articles = other_articles

    def recommend(self, limit):
        ranked = [
            (self.similarity(article), article_id)
            for article_id, article in self.other_articles.items()
            if article_id != self.base_id
        ]
        return [
            pair[1]
            for pair in reversed(sorted(ranked))
        ][:10] #TODO inefficient

    def similarity(self, article):
        comp = np.array(article["classification"])
        comp = comp / np.linalg.norm(comp)
        return self.base_norm.dot(comp)
