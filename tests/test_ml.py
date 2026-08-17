import unittest

from deeptrace.fixtures import ITEMS
from deeptrace.ml import MODEL_NAME, cluster_campaigns, ml_summary


class DeepTraceMLTests(unittest.TestCase):
    def test_model_metadata(self):
        summary = ml_summary(ITEMS)
        self.assertEqual(summary["model"], MODEL_NAME)
        self.assertEqual(summary["clusterer"], "DBSCAN with cosine distance")

    def test_risky_narrative_variants_cluster(self):
        clusters = cluster_campaigns(ITEMS)
        groups = [set(cluster.content_ids) for cluster in clusters]
        self.assertIn({"m03", "m04"}, groups)
        self.assertIn({"m05", "m06"}, groups)

    def test_verified_news_repeat_is_not_flagged_as_campaign(self):
        clusters = cluster_campaigns(ITEMS)
        flagged = set().union(*(set(cluster.content_ids) for cluster in clusters))
        self.assertFalse({"m01", "m02"}.issubset(flagged))

    def test_clusters_are_explainable(self):
        clusters = cluster_campaigns(ITEMS)
        self.assertTrue(all(cluster.semantic_similarity >= 0.8 for cluster in clusters))
        self.assertTrue(all(cluster.risky_items >= 2 for cluster in clusters))
        self.assertTrue(all(len(cluster.accounts) >= 2 for cluster in clusters))

    def test_results_are_deterministic(self):
        first = [cluster.to_dict() for cluster in cluster_campaigns(ITEMS)]
        second = [cluster.to_dict() for cluster in cluster_campaigns(ITEMS)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
