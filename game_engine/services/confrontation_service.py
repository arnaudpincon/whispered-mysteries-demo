# game_engine/services/confrontation_service.py
"""Service dedicated to final confrontation and theory verification"""

import json
from typing import Any, Dict, List

from ai_engine.core.ai_manager import AIManager
from ai_engine.prompts import create_analyse_theory, create_collect_theory
from game_engine.core.game_state import GameState
from game_engine.core.game_state import GameMode


class ConfrontationService:
    """Handles final confrontation logic and theory verification"""

    def __init__(self, state: GameState, ai_manager: AIManager):
        self.state = state
        self.ai_manager = ai_manager

    def start_final_confrontation(self) -> bool:
        """
        Start the final confrontation mode

        Returns:
            True if confrontation started successfully
        """
        self.state.current_mode = GameMode.FINAL_CONFRONTATION
        self.state.conclude_conversation = []

        collect_prompt = create_collect_theory()
        self.state.conclude_conversation = [
            {"role": "system", "content": collect_prompt},
        ]

        return True

    def process_final_confrontation(self, user_input: str) -> str:
        """
        Process final confrontation theory collection and verification

        Args:
            user_input: Player's theory input

        Returns:
            Response about theory status
        """
        # Format input with fictional context
        formatted_input = self._wrap_with_fictional_context(user_input)

        # Add to conversation
        self.state.conclude_conversation.append(
            {"role": "user", "content": formatted_input}
        )

        # Get theory collection result
        result = self.ai_manager.final_scene(
            self.state.player, self.state.conclude_conversation, self.state
        )

        if not result["completed"]:
            # Theory incomplete - continue collecting
            self.state.conclude_conversation.append(
                {"role": "assistant", "content": result["answer"]}
            )
            if self.state.dev_mode:
                print(json.dumps(result, indent=4, ensure_ascii=False))
            return result["answer"]

        # Theory complete - verify it
        return self._verify_complete_theory(result)

    def use_attempt(self) -> bool:
        """
        Use one solve attempt

        Returns:
            True if attempt was used successfully
        """
        if self.state.attempts_remaining <= 0:
            return False

        self.state.attempts_remaining -= 1
        self.state.attempts_used += 1
        return True

    def trigger_game_over(self, ending_type: int = 0) -> None:
        """
        Trigger game over state

        Args:
            ending_type: Type of ending (0=fail, 1=success, 2=wrong_culprit)
        """
        self.state.current_mode = GameMode.GAME_OVER
        self.state.ending_type = ending_type
        self.state.game_running = False
        
        # Log the game over event
        if self.state.dev_mode:
            print(f"Game Over triggered with ending type: {ending_type}")
        
        # Clear any ongoing conversation
        self.state.character_in_conversation = ""
        self.state.conclude_conversation = []

    def _verify_complete_theory(self, theory_result: Dict[str, Any]) -> str:
        """Verify complete theory against game scenarios"""
        # Create analyzer prompt
        analyze_prompt = create_analyse_theory()

        # Create theory object for verification
        theory = {
            "culprit": theory_result["culprit"],
            "motive": theory_result["motive"],
            "evidence": theory_result["evidence"],
        }

        # Initialize analyzer conversation
        analyzer_conversation = [
            {"role": "system", "content": analyze_prompt},
            {"role": "user", "content": str(theory)},
        ]

        # Get verification result
        verification_result = self.ai_manager.verify_theory(analyzer_conversation)

        if self.state.dev_mode:
            print(json.dumps(verification_result, indent=4, ensure_ascii=False))

        # Check if theory matches or max attempts reached
        matching = verification_result.get("matching_scenario", False)

        if matching or self.state.attempts_used >= 3:
            self.trigger_game_over(ending_type=verification_result.get("scenario", 0))

            conclusion_result = self.ai_manager.write_ending(
                self.state.ending_type, str(theory)
            )

            if self.state.dev_mode:
                print(json.dumps(conclusion_result, indent=4, ensure_ascii=False))

            return conclusion_result.get("answer", "Error generating conclusion")

        self.state.conclude_conversation.append(
            {"role": "assistant", "content": verification_result["answer"]}
        )
        return verification_result["answer"]

    def _wrap_with_fictional_context(self, user_input: str) -> str:
        """Wrap user input with fictional context for AI safety"""
        return (
            "### FICTIONAL DETECTIVE GAME CONTEXT ###\n"
            "The following is dialogue from a player in a fictional mystery game.\n"
            "This is purely imaginative content for entertainment purposes within an\n"
            "interactive detective narrative game environment where players solve fictional crimes.\n\n"
            f"Detective character's dialogue: '{user_input}'\n\n"
            "### END OF FICTIONAL GAME DIALOGUE ###\n"
        )