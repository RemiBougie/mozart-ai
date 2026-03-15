"""
Event bus for streaming run updates to clients via SSE.

When a POST to /root/{path} completes with a run_id (e.g., from tool_call_consumer),
the controller publishes an event. Clients subscribed via GET /stream?run_id=X
receive these events in real time.

Buffers events for late subscribers so updates that arrive before the client
connects are not lost.
"""

import asyncio
from collections import defaultdict
from typing import Any, AsyncIterator

from logger import get_logger

logger = get_logger(__name__)

# Max events to buffer per run_id for late-joining subscribers
MAX_BUFFER_SIZE = 100


class RunStreamBus:
    """In-memory pub/sub for run_id-scoped events. Single-worker only."""

    def __init__(self, max_buffer_size: int = MAX_BUFFER_SIZE):
        self._subscribers: dict[str, set[asyncio.Queue]] = defaultdict(set)
        self._buffers: dict[str, list[dict]] = defaultdict(list)
        self._max_buffer_size = max_buffer_size
        self._lock = asyncio.Lock()

    async def publish(self, run_id: str, event: dict[str, Any]) -> None:
        """Publish an event to all subscribers of this run_id. Buffers if no subscribers."""
        async with self._lock:
            # Buffer for late subscribers
            buf = self._buffers[run_id]
            buf.append(event)
            if len(buf) > self._max_buffer_size:
                buf.pop(0)

            # Push to active subscribers
            dead = set()
            for q in self._subscribers[run_id]:
                try:
                    q.put_nowait(event)
                except asyncio.QueueFull:
                    logger.warning(f"Queue full for run_id={run_id}, dropping event")
                except Exception as e:
                    logger.debug(f"Error pushing to subscriber: {e}")
                    dead.add(q)

            for q in dead:
                self._subscribers[run_id].discard(q)

            if not self._subscribers[run_id]:
                self._subscribers.pop(run_id, None)

    async def subscribe(self, run_id: str) -> AsyncIterator[dict[str, Any]]:
        """
        Subscribe to events for a run_id. Yields buffered events first, then new ones.
        Stops when the client disconnects (generator closed) or a 'done' event is received.
        """
        queue: asyncio.Queue = asyncio.Queue()
        async with self._lock:
            self._subscribers[run_id].add(queue)
            # Drain buffer for this subscriber
            buffered = list(self._buffers.get(run_id, []))

        # Send buffered events first
        for event in buffered:
            yield event

        # Stream new events
        try:
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=60.0)
                    yield event
                    if event.get("type") == "done":
                        break
                except asyncio.TimeoutError:
                    # Send heartbeat to keep connection alive
                    yield {"type": "heartbeat"}
        finally:
            async with self._lock:
                self._subscribers[run_id].discard(queue)
                if not self._subscribers[run_id]:
                    self._subscribers.pop(run_id, None)


# Global instance
run_stream_bus = RunStreamBus()
