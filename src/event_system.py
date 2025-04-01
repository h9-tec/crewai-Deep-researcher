from typing import Dict, Any, Callable, List
from datetime import datetime

class EventSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize event handlers"""
        self._step_handlers: List[Callable] = []
        self._citation_handlers: List[Callable] = []
        self._message_handlers: List[Callable] = []

    def subscribe_to_step(self, handler: Callable[[str, str, str, str], None]):
        """Subscribe to step updates"""
        self._step_handlers.append(handler)

    def subscribe_to_citation(self, handler: Callable[[str, str, str], None]):
        """Subscribe to citation updates"""
        self._citation_handlers.append(handler)

    def subscribe_to_message(self, handler: Callable[[str, str], None]):
        """Subscribe to message updates"""
        self._message_handlers.append(handler)

    def notify_step(self, thought: str, action: str, input_data: str, observation: str):
        """Notify all step handlers"""
        for handler in self._step_handlers:
            handler(thought, action, input_data, observation)

    def notify_citation(self, title: str, url: str, content: str):
        """Notify all citation handlers"""
        for handler in self._citation_handlers:
            handler(title, url, content)

    def notify_message(self, role: str, content: str):
        """Notify all message handlers"""
        for handler in self._message_handlers:
            handler(role, content)

# Create a singleton instance
event_system = EventSystem() 