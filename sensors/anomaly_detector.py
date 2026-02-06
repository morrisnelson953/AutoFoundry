
























































import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Простая модель детектирования аномалий по z-score.
    """

    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.history: Dict[str, List[float]] = {}

    def update(self, readings: Dict[str, float]) -> bool:
        anomalies = []
        for k, v in readings.items():
            values = self.history.setdefault(k, [])
            values.append(v)
            if len(values) > 200:
                values.pop(0)

            if len(values) > 10:
                z = self._z_score(values)
                if abs(z[-1]) > self.threshold:
                    anomalies.append((k, v, round(z[-1], 2)))

        if anomalies:
            for key, val, score in anomalies:
                logger.warning(f"Anomaly detected in {key}: {val} (z={score})")
            return True
        return False

    @staticmethod
    def _z_score(values: List[float]) -> np.ndarray:
        arr = np.array(values)
        mean = np.mean(arr)
        std = np.std(arr) or 1e-6
        return (arr - mean) / std
