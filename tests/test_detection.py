from pathlib import Path
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"

class DetectionPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(OUTPUT / "scored_events.csv")

    def test_required_output_columns(self):
        required = {
            "event_id", "user_id", "risk_score", "severity",
            "alert", "reason", "label"
        }
        self.assertTrue(required.issubset(self.df.columns))

    def test_risk_score_range(self):
        self.assertTrue(self.df["risk_score"].between(0, 100).all())

    def test_unique_event_ids(self):
        self.assertTrue(self.df["event_id"].is_unique)

    def test_four_planted_events(self):
        self.assertEqual(int(self.df["label"].sum()), 4)

    def test_alert_reasons_exist(self):
        alerts = self.df[self.df["alert"].astype(bool)]
        self.assertTrue(alerts["reason"].notna().all())
        self.assertTrue((alerts["reason"].str.len() > 0).all())

if __name__ == "__main__":
    unittest.main()
    
