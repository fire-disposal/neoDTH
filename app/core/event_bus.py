import asyncio
from typing import Callable, Dict, List, Any, Type

class EventBus:
    def __init__(self):
        # 支持事件类型为字符串或类
        self._subscribers: Dict[Any, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: Any, handler: Callable[[Any], None]):
        """订阅事件类型，可为字符串或类"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: Any, handler: Callable[[Any], None]):
        """取消订阅"""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h != handler
            ]
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]

    async def publish(self, event_type: Any, event: Any):
        """异步发布事件，支持并发执行所有 handler"""
        handlers = self._subscribers.get(event_type, [])
        tasks = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(event))
            else:
                # 同步 handler 包装为线程任务
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, handler, event))
        if tasks:
            await asyncio.gather(*tasks)

event_bus = EventBus()