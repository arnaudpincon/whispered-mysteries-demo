from typing import List

from .base_handler import BaseChatHandler
from .conversation_handler import ConversationHandler
from .exploration_handler import ExplorationHandler
from .initialization_handler import InitializationHandler


class ChatHandlerFactory:
    """Factory for creating appropriate chat handlers"""

    def __init__(self):
        self.handlers: List[BaseChatHandler] = [
            InitializationHandler(),
            ConversationHandler(),  # Check before exploration
            ExplorationHandler(),
        ]

    def get_handler(self, chat: str, history, facade) -> BaseChatHandler:
        """Get the appropriate handler for the request"""
        for handler in self.handlers:
            if handler.can_handle(chat, history, facade):
                return handler

        # Fallback to exploration handler
        return self.handlers[-1]
