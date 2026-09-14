import unittest
import pandas as pd
from mine_slot_omega import is_q_active, extract_carrier_from_aiin


class TestSlotOmegaLogic(unittest.TestCase):

    def test_q_active_detection(self):
        self.assertTrue(is_q_active("qokedy"))
        self.assertTrue(is_q_active("qotched"))
        self.assertTrue(is_q_active("qokaiin"))
        self.assertFalse(is_q_active("otcheody"))
        self.assertFalse(is_q_active("daiin"))

    def test_carrier_extraction(self):
        self.assertEqual(extract_carrier_from_aiin("otcheodaiin"), "otcheod")
        self.assertEqual(extract_carrier_from_aiin("chedain"), "ched")
        self.assertEqual(extract_carrier_from_aiin("qokedy"), "")

    def test_synthetic_frame_match(self):
        # Simulating a sequence: Q-ACTIVE -> OTCHEOD-AIIN -> Q-ACTIVE
        seq = ["qokedy", "otcheodaiin", "qotched"]
        is_match = is_q_active(seq[0]) and bool(extract_carrier_from_aiin(seq[1])) and is_q_active(seq[2])
        self.assertTrue(is_match)


if __name__ == "__main__":
    unittest.main()
