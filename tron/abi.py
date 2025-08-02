#!/usr/bin/env python3
import json
import logging

logger = logging.getLogger(__name__)

logger.debug("📥 Загрузка ABI для контракта Stake2.0...")

STAKE20_ABI = json.loads(""" 
[
  {
    "inputs": [
      {"name": "fromAddress", "type": "address"},
      {"name": "receiverAddress", "type": "address"},
      {"name": "balance", "type": "uint256"},
      {"name": "resource", "type": "uint256"}
    ],
    "name": "delegateResource",
    "outputs": [],
    "stateMutability": "NonPayable",
    "type": "Function"
  }
]
""")

logger.debug("✅ ABI успешно загружен.")
