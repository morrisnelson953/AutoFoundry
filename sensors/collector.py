import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from .plc_adapter import PLCAdapter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SensorCollector:
    """
    Асинхронный сборщик данных с производственных сенсоров.
    """

    def __init__(self, plc_adapter: PLCAdapter, interval: float = 1.0):
        self.plc_adapter = plc_adapter
        self.interval = interval
        self.buffer: List[Dict[str, Any]] = []

    async def collect(self):
        """Цикл сбора данных."""
        logger.info("Starting sensor data collection loop...")
        while True:
            try:
                data = await self.plc_adapter.read_all()
                timestamped = {"timestamp": datetime.utcnow().isoformat(), **data}
                self.buffer.append(timestamped)
                if len(self.buffer) > 1000:
                    self.buffer = self.buffer[-1000:]
                logger.debug(f"Collected: {json.dumps(timestamped)}")
            except Exception as e:
                logger.error(f"Error during collection: {e}")
            await asyncio.sleep(self.interval)

    def get_latest(self, n: int = 10) -> List[Dict[str, Any]]:
        """Возвращает последние n записей."""
        return self.buffer[-n:]


async def main():
    plc = PLCAdapter(ip="192.168.0.10")
    collector = SensorCollector(plc)
    await collector.collect()


if __name__ == "__main__":
    asyncio.run(main())
