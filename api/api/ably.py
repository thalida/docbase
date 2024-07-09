import os

from ably.sync import AblyRestSync

ABLY_API_KEY = os.getenv("ABLY_API_KEY")
ably_client = AblyRestSync(key=ABLY_API_KEY)
