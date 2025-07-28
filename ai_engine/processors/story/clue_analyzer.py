"""
Clue analysis component
"""

import logging
from typing import Any, Optional, List

from ai_engine.api.service import APIConfig
from ai_engine.prompts import create_clue_analysis_prompt

from .interfaces import IClueAnalyzer

logger = logging.getLogger(__name__)


class ClueAnalyzer(IClueAnalyzer):
    """Analyzes clues and provides insights to the player"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def analyze_clue(self, clue: Any, collected_clues: Optional[List] = None) -> str:
        """
        Analyzes a clue and gives insights to the player.

        Args:
            clue: Clue to analyze
            collected_clues: Optional list of previously collected clues

        Returns:
            Analysis of the clue
        """
        try:
            prompt: str = create_clue_analysis_prompt(clue, collected_clues)
            
            # Check cache first
            cache_context = {
                "type": "clue_analysis",
                "clue": clue.name,
                "clues_count": len(collected_clues) if collected_clues else 0
            }
            
            cached_result = self.cache.get(
                prompt,
                {"temperature": 0.7},
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print(f"🚀 CACHE HIT: Clue analysis found in cache for {clue.name}")
                return cached_result
            
            messages = [{"role": "user", "content": prompt}]
            system_content = "You are a perceptive detective analyzing clues."

            content = self.api_service.make_api_call(
                messages=messages, 
                system_content=system_content, 
                max_tokens=APIConfig.MAX_TOKENS_SMALL,
            )

            # Always define result with a fallback
            if content:
                result = content
            else:
                result = "This clue seems significant, but its meaning eludes me for now."
            
            # Store in cache
            self.cache.put(
                prompt,
                {"temperature": 0.7},
                result,
                cache_context
            )

            if self.dev_mode:
                print(f"💾 CACHE MISS: Generated and cached clue analysis for {clue.name}")

            return result

        except Exception as e:
            logger.error(f"Error in analyze_clue: {e}")
            return "This clue seems significant, but its meaning eludes me for now."