"""
Theory verification component
"""

import logging
from typing import Any, Dict, List

from ai_engine.api.service import APIConfig
from ai_engine.utils.constants import ErrorMessages

from .interfaces import ITheoryVerifier

logger = logging.getLogger(__name__)


class TheoryVerifier(ITheoryVerifier):
    """Verifies detective theories against possible scenarios"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def verify_theory(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Verifies the detective's theory against possible scenarios.

        Args:
            conversation: The conversation history for the analyzer

        Returns:
            Dict containing verification result including validity and response
        """
        try:
            if self.dev_mode:
                print(f"🔍 THEORY VERIFICATION: Analyzing theory")
            
            # Check cache first
            conversation_key = str(hash(str(conversation)))
            cache_context = {
                "type": "theory_verification",
                "conversation_hash": conversation_key
            }
            
            cached_result = self.cache.get(
                conversation_key,
                {"temperature": 0.5, "format": "json"},
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print("🚀 CACHE HIT: Theory verification found in cache")
                return self.api_service.parse_json_response(
                    cached_result,
                    self._get_fallback_response()
                )
            
            # Make API call
            content = self.api_service.make_api_call(
                messages=conversation,
                max_tokens=APIConfig.MAX_TOKENS_XLARGE,
                response_format={"type": "json_object"},
            )

            if content is None:
                if self.dev_mode:
                    print("❌ THEORY VERIFICATION: API call failed")
                return self._get_fallback_response()
            
            # Parse response
            result = self.api_service.parse_json_response(content, self._get_fallback_response())
            
            # Store in cache
            self.cache.put(
                conversation_key,
                {"temperature": 0.5, "format": "json"},
                content,
                cache_context
            )
            
            if self.dev_mode:
                print("💾 CACHE MISS: Generated and cached theory verification")
            
            return result

        except Exception as e:
            logger.error(f"Error in verify_theory: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get fallback response for theory verification"""
        return {
            "think": "Error occurred during theory verification",
            "culprit_match": False,
            "motive_match": False,
            "evidence_match": False,
            "valid": False,
            "matching_scenario": None,
            "answer": ErrorMessages.THEORY_ERROR,
        }