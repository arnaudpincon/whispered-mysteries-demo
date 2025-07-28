# === base_transition.py ===
"""Base class for all transition handlers"""

from abc import ABC, abstractmethod
from typing import Any

from ...core.types import OptionalFacade


class BaseTransitionHandler(ABC):
    """Base interface for transition handlers"""

    @abstractmethod
    def can_handle(self, facade: OptionalFacade) -> bool:
        """Check if this handler can process the transition"""

    @abstractmethod
    def execute(self, facade: OptionalFacade) -> Any:
        """Execute the transition"""
