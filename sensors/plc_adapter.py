import asyncio
import random
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class PLCAdapter:
    """
    Эмулятор подключения к промышленному ПЛК.
    В реальном проекте — реализация через OPC UA, Modbus или Profinet.
    """

    def __init__(self, ip: str):
        self.ip = ip
        self.connected = False

    async def connect(self):
        logger.info(f"Connecting to PLC at {self.ip}...")
        await asyncio.sleep(0.5)
        self.connected = True
        logger.info("PLC connection established.")

    async def read_all(self) -> Dict[str, Any]:
        if not self.connected:
            await self.connect()
        # Симуляция чтения данных
        await asyncio.sleep(0.05)
        return {
            "temperature": round(random.uniform(60, 90), 2),
            "vibration": round(random.uniform(0.1, 1.5), 2),
            "pressure": round(random.uniform(1.0, 2.5), 2),
        }

    async def write(self, variable: str, value: Any):
        if not self.connected:
            await self.connect()
        logger.info(f"Writing {variable}={value} to PLC at {self.ip}")
        await asyncio.sleep(0.1)
