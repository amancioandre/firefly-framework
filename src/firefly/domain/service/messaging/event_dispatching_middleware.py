from __future__ import annotations

from dataclasses import is_dataclass, asdict
from typing import Callable

import firefly.domain as ffd

from .middleware import Middleware
from .system_bus import SystemBusAware


class EventDispatchingMiddleware(Middleware, SystemBusAware):
    _event_buffer: ffd.EventBuffer = None
    _message_factory: ffd.MessageFactory = None

    def __call__(self, message: ffd.Message, next_: Callable) -> ffd.Message:
        try:
            ret = next_(message)
            for event in self._event_buffer:
                data = event[1]
                if is_dataclass(data):
                    data = asdict(data)
                if isinstance(event, tuple):
                    self.dispatch(self._message_factory.event(event[0], data))
                else:
                    self.dispatch(event)
        finally:
            self._event_buffer.clear()

        return ret
