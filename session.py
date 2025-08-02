#!/usr/bin/env python3
import asyncio
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
SESSIONS = {}

async def cleanup_sessions():
    while True:
        now = datetime.now(timezone.utc)
        expired = [uid for uid, data in SESSIONS.items() if data["expires"] < now]

        for uid in expired:
            session = SESSIONS.pop(uid, None)
            if session:
                logger.info(f"🗑️ Session expired and removed for user_id={uid}")

        await asyncio.sleep(60)
