"""
Ending writing component
"""

import logging
from typing import Any, Dict

from ai_engine.api.service import APIConfig
from ai_engine.prompts import create_write_ending
from utils.markdown_utils import read_markdown_file

from .interfaces import IEndingWriter

logger = logging.getLogger(__name__)


class EndingWriter(IEndingWriter):
    """Generates game endings based on player theory and scenario"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def write_ending(self, scenario: int, player_theory: str) -> Dict[str, Any]:
        """
        Generates the ending of the game based on the player's theory and the scenario.

        Args:
            scenario: Scenario number for the ending
            player_theory: Player's theory about the murder

        Returns:
            Dictionary containing the generated ending
        """
        try:
            if self.dev_mode:
                print(f"📝 ENDING WRITER: Creating ending for scenario {scenario}")
            
            # Read the ending file
            try:
                text_ending: str = read_markdown_file(
                    f"data/narratives/documents/ending{scenario}.md"
                )
            except Exception as e:
                logger.error(f"Error reading ending file: {e}")
                return self._get_file_error_response()

            # Check cache first
            cache_key = f"ending_{scenario}_{hash(player_theory)}"
            cache_context = {
                "type": "ending",
                "scenario": scenario,
                "theory_hash": hash(player_theory)
            }
            
            cached_result = self.cache.get(
                cache_key,
                {"temperature": APIConfig.ENDING_TEMPERATURE, "format": "json"},
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print("🚀 CACHE HIT: Ending found in cache")
                return self.api_service.parse_json_response(
                    cached_result,
                    self._get_fallback_response(text_ending)
                )

            # Create prompt and make API call
            prompt: str = create_write_ending(text_ending, player_theory)
            messages = [{"role": "user", "content": prompt}]
            system_content = (
                "You are a game writer creating an ending for a detective game."
            )

            content = self.api_service.make_api_call(
                messages=messages,
                system_content=system_content,
                temperature=APIConfig.ENDING_TEMPERATURE,
                max_tokens=APIConfig.MAX_TOKENS_XLARGE,
                response_format={"type": "json_object"},
            )

            if content is None:
                if self.dev_mode:
                    print("❌ ENDING WRITER: API call failed")
                return self._get_fallback_response(text_ending)
            
            # Parse response
            result = self.api_service.parse_json_response(
                content, 
                self._get_fallback_response(text_ending)
            )
            
            # Store in cache
            self.cache.put(
                cache_key,
                {"temperature": APIConfig.ENDING_TEMPERATURE, "format": "json"},
                content,
                cache_context
            )
            
            if self.dev_mode:
                print("💾 CACHE MISS: Generated and cached ending")
            
            return result

        except Exception as e:
            logger.error(f"Error in write_ending: {e}")
            return {
                "think": f"Error occurred: {str(e)}",
                "answer": "The truth reveals itself in ways beyond words...",
            }
    
    def _get_fallback_response(self, text_ending: str) -> Dict[str, Any]:
        """Get fallback response with original text"""
        return {
            "think": "The model censored the ending. Displaying the document content.",
            "answer": text_ending,
        }
    
    def _get_file_error_response(self) -> Dict[str, Any]:
        """Get fallback response for file errors"""
        return {
            "think": "Error reading ending file",
            "answer": "The truth reveals itself in ways beyond words...",
        }