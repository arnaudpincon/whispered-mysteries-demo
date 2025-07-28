"""
Factory for creating command processing components
"""

from typing import Tuple

from .command_analyzer import CommandAnalyzer
from .command_executor import CommandExecutor
from .nonsense_handler import NonsenseHandler


class CommandComponentFactory:
    """Factory for creating command processing components"""
    
    @staticmethod
    def create_standard_setup(
        api_service, 
        cache, 
        dev_mode: bool = False
    ) -> Tuple[
        CommandAnalyzer,
        CommandExecutor,
        NonsenseHandler
    ]:
        """
        Create a standard command processing setup
        
        Args:
            api_service: API service instance
            cache: Cache manager instance
            dev_mode: Enable development mode features
            
        Returns:
            Tuple of all command processing components
        """
        
        # Create all components
        command_analyzer = CommandAnalyzer(api_service, cache, dev_mode)
        command_executor = CommandExecutor(api_service, cache, dev_mode)
        nonsense_handler = NonsenseHandler(api_service, cache, dev_mode)
        
        return command_analyzer, command_executor, nonsense_handler