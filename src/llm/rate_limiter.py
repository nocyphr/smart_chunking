import asyncio
from time import time
import logging
from typing import Tuple, Optional
import tiktoken
from dataclasses import dataclass


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


@dataclass
class RateLimitConfig:
    token_limit: int = 30000
    request_limit: int = 95
    time_window: float = 60.0


class RateLimiter:
    def __init__(self, config: RateLimitConfig):
        self.token_limit = config.token_limit
        self.request_limit = config.request_limit
        self.time_window = config.time_window
        self.request_times = []
        self.token_usage = []
        self.lock = asyncio.Lock()

    async def _cleanup_old_requests(self):
        now = time()
        cutoff = now - self.time_window

        total_tokens = sum(tokens for ts, tokens in self.token_usage)
        logging.info(f"Current token usage: {total_tokens}/{self.token_limit}, "
                     f"Requests: {len(self.request_times)}/{self.request_limit}")

        while self.token_usage and self.token_usage[0][0] < cutoff:
            self.token_usage.pop(0)

        while self.request_times and self.request_times[0] < cutoff:
            self.request_times.pop(0)

    async def acquire(self, tokens: int, progress_info: Optional[Tuple[int, int]] = None):
        while True:
            async with self.lock:
                await self._cleanup_old_requests()
                current_tokens = sum(tokens for ts, tokens in self.token_usage)
                progress_str = f" ({
                    progress_info[0]}/{progress_info[1]} sentences)" if progress_info else ""

                if len(self.request_times) < self.request_limit and current_tokens + tokens < self.token_limit:
                    now = time()
                    self.request_times.append(now)
                    self.token_usage.append((now, tokens))
                    logging.info(f"Acquired rate limit slot -{progress_str} "
                                 f"Requests: {
                                     len(self.request_times)}/{self.request_limit}, "
                                 f"Tokens: {current_tokens + tokens}/{self.token_limit}")
                    return

            wait_time = 1.0
            logging.info(f"Rate limit reached, waiting {wait_time}s -{progress_str} "
                         f"Requests: {len(self.request_times)
                                      }/{self.request_limit}, "
                         f"Tokens: {current_tokens}/{self.token_limit} (new: {tokens})")
            await asyncio.sleep(wait_time)
