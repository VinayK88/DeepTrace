import unittest

from deeptrace.evaluation import (
    adversarial_evaluation,
    evaluation_summary,
    narrative_drift_report,
    simulate_shifted_narratives,
)
from deeptrace.fixtures import ITEMS


class DeepTraceEvaluationTests(unittest.TestCase):
    def test_steady_state_has_no_drift(self):
        report = narrative_drift_report(list(ITEMS), list(ITEMS))
        self.assertFalse(report["drift_alert"])
        self.assertAlmostEqual(report["centroid_cosine_similarity"], 1.0, places=3)
        self.assertAlmostEqual(report["vocabulary_overlap"], 1.0, places=3)

    def test_shifted_narratives_trigger_drift(self):
        shifted = simulate_shifted_narratives(list(ITEMS))
        report = narrative_drift_report(list(ITEMS), shifted)
        self.assertTrue(report["drift_alert"])
        self.assertGreaterEqual(len(report["reasons"]), 1)

    def test_paraphrase_evaluation_runs(self):
        result = adversarial_evaluation()
        self.assertEqual(result["cases"], 4)
        self.assertTrue(0.0 <= result["synthetic_cluster_coverage"] <= 1.0)
        self.assertGreaterEqual(result["clusters_detected"], 1)

    def test_summary_contains_versioned_metadata(self):
        summary = evaluation_summary(list(ITEMS))
        self.assertEqual(summary["model_metadata"]["model_version"], "deeptrace-tfidf-dbscan-v1")
        self.assertEqual(summary["model_metadata"]["feature_schema_version"], "narrative-char-ngram-v1")


if __name__ == "__main__":
    unittest.main()
