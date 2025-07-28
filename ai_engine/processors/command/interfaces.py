"""
Abstract interfaces for command processing components
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class ICommandAnalyzer(ABC):
    """Interface for analyzing and understanding player commands"""
    
    @abstractmethod
    def analyze_command(self, command: str, game_state: Any) -> Dict[str, Any]:
        """Analyze player command and extract intent, targets, and validation"""
        pass


class ICommandExecutor(ABC):
    """Interface for executing validated commands"""
    
    @abstractmethod
    def execute_command(self, reasoning_result: Dict[str, Any], game_state: Any) -> Dict[str, Any]:
        """Execute command based on analysis results"""
        pass


class INonsenseHandler(ABC):
    """Interface for handling nonsensical or inappropriate actions"""
    
    @abstractmethod
    def handle_nonsense(self, command: str, game_state: Any) -> Dict[str, Any]:
        """Generate reaction to nonsense actions with humor and realism"""
        pass