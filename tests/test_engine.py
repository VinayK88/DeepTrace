import unittest

from deeptrace.engine import DeepTraceEngine
from deeptrace.fixtures import ITEMS
from deeptrace.report import build_report


class DeepTraceTests(unittest.TestCase):
    def test_expected_verdicts(self):
        engine = DeepTraceEngine()
        got = [engine.assess(item).verdict for item in ITEMS]
        expected = [item.expected_verdict for item in ITEMS]
        self.assertEqual(got, expected)

    def test_verified_requires_valid_trusted_provenance(self):
        engine = DeepTraceEngine()
        verified = engine.assess(ITEMS[0])
        self.assertEqual(verified.verdict, "VERIFIED")
        self.assertGreaterEqual(verified.confidence, 0.9)

    def test_manipulated_items_flagged(self):
        engine = DeepTraceEngine()
        self.assertEqual(engine.assess(ITEMS[2]).verdict, "LIKELY_MANIPULATED")
        self.assertEqual(engine.assess(ITEMS[3]).verdict, "LIKELY_MANIPULATED")

    def test_synthetic_items_flagged(self):
        engine = DeepTraceEngine()
        self.assertEqual(engine.assess(ITEMS[4]).verdict, "HIGH_RISK_SYNTHETIC")
        self.assertEqual(engine.assess(ITEMS[5]).verdict, "HIGH_RISK_SYNTHETIC")

    def test_campaign_detection(self):
        findings = DeepTraceEngine().detect_campaigns(ITEMS)
        self.assertGreaterEqual(len(findings), 2)
        self.assertTrue(all(x.coordination_score >= 0.62 for x in findings))

    def test_report_is_consistent(self):
        report = build_report()
        self.assertEqual(report["summary"]["expected_verdicts_matched"], 8)
        self.assertEqual(report["summary"]["risky_media_flagged"], 4)


if __name__ == "__main__":
    unittest.main()
