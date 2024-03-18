import unittest
import numpy as np
from packet_sniffer import extract_features, detect_anomalies

class TestPacketSniffer(unittest.TestCase):
    def test_detect_anomalies(self):
        # Define mock features for testing
        mock_features = np.array([[100], [200], [300], [400], [500]])

        # Assuming that the model will flag packets with size greater than 300 as anomalies
        mock_model = MockModel()

        # Test case 1: All packets are normal
        normal_labels = [0] * len(mock_features)
        anomalies = detect_anomalies(mock_model, mock_features)
        self.assertEqual(len(anomalies), len(mock_features))
        self.assertFalse(any(anomalies))  # No anomalies should be detected

        # Test case 2: All packets are anomalies
        anomaly_labels = [1] * len(mock_features)
        anomalies = detect_anomalies(mock_model, mock_features)
        self.assertEqual(len(anomalies), len(mock_features))
        self.assertTrue(all(anomalies))  # All packets should be detected as anomalies

        # Test case 3: Mixed normal and anomaly packets
        mixed_labels = [0, 0, 1, 1, 0]  # First two packets are normal, last three are anomalies
        anomalies = detect_anomalies(mock_model, mock_features)
        self.assertEqual(len(anomalies), len(mock_features))
        self.assertTrue(any(anomalies))  # Some anomalies should be detected

# This class simulates the behavior of our ML algorithm for testing purposes 
class MockModel:
    def predict(self, features):
        # Mock prediction: flag packets with size greater than 300 as anomalies
        return [1 if feature[0] > 300 else 0 for feature in features]

if __name__ == "__main__":
    unittest.main()
