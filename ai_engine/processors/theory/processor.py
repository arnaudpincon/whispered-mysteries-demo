"""
Main TheoryProcessor - Clean interface with refactored components
"""

import logging
from typing import Any, Dict, List

from ai_engine.processors.base_processor import BaseProcessor
from ai_engine.utils.constants import GameStateInput

from .factory import TheoryComponentFactory

logger = logging.getLogger(__name__)


class TheoryProcessor(BaseProcessor):
    """
    Refactored Theory Processor - Now acts as a lightweight coordinator
    
    Responsibilities:
    1. Coordinate theory processing components
    2. Provide backward-compatible interface
    3. Handle high-level theory flow
    """
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        super().__init__(api_service, cache, dev_mode)
        
        # Create theory components using factory
        (self.final_scene_handler,
         self.theory_verifier,
         self.ending_writer) = TheoryComponentFactory.create_standard_setup(
            api_service, cache, dev_mode
        )
        
        self._log_debug("TheoryProcessor initialized with refactored components")
    
    def get_processor_name(self) -> str:
        return "theory"

    def final_scene(
        self, player: Any, conversation: List[Dict[str, str]], game_state: GameStateInput
    ) -> Dict[str, Any]:
        """
        Assist the player in completing their murder theory.
        Now delegated to specialized component.

        Args:
            player: Player object
            conversation: Conversation history
            game_state: Current game state (GameState object or dictionary)

        Returns:
            Dictionary containing scene completion status and response
        """
        self._log_debug("Processing final scene interaction")
        
        try:
            # Validate and normalize state (for potential future use)
            ai_state = self._normalize_game_state(game_state)
            if ai_state is None:
                logger.warning("Invalid game state in final_scene, continuing anyway")

            return self.final_scene_handler.handle_final_scene(player, conversation, game_state)
            
        except Exception as e:
            self.logger.error(f"Error in final_scene: {e}")
            return {"completed": False, "answer": "Forgive me, detective, but the Almighty clouds my understanding of your theory. Could you repeat please ?"}

    def verify_theory(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Verifies the detective's theory against possible scenarios.
        Now delegated to specialized component.

        Args:
            conversation: The conversation history for the analyzer

        Returns:
            Dict containing verification result including validity and response
        """
        self._log_debug("Verifying detective theory")
        
        try:
            return self.theory_verifier.verify_theory(conversation)
            
        except Exception as e:
            self.logger.error(f"Error in verify_theory: {e}")
            return {
                "think": f"Error occurred: {str(e)}",
                "culprit_match": False,
                "motive_match": False,
                "evidence_match": False,
                "valid": False,
                "matching_scenario": None,
                "answer": "Forgive me, detective, but the Almighty clouds my understanding of your theory. Could you repeat please ?",
            }

    def write_ending(self, scenario: int, player_theory: str) -> Dict[str, Any]:
        """
        Generates the ending of the game based on the player's theory and the scenario.
        Now delegated to specialized component.

        Args:
            scenario: Scenario number for the ending
            player_theory: Player's theory about the murder

        Returns:
            Dictionary containing the generated ending
        """
        self._log_debug(f"Writing ending for scenario {scenario}")
        
        try:
            return self.ending_writer.write_ending(scenario, player_theory)
            
        except Exception as e:
            self.logger.error(f"Error in write_ending: {e}")
            return {
                "think": f"Error occurred: {str(e)}",
                "answer": "The truth reveals itself in ways beyond words...",
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of theory processor components"""
        return {
            "processor_name": self.get_processor_name(),
            "final_scene_handler": self.final_scene_handler is not None,
            "theory_verifier": self.theory_verifier is not None,
            "ending_writer": self.ending_writer is not None,
            "api_service": self.api_service is not None,
            "cache": self.cache is not None,
            "dev_mode": self.dev_mode
        }