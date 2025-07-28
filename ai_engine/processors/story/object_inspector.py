"""
Object inspection component for non-clue items
"""

import logging

from ai_engine.api.service import APIConfig
from ai_engine.prompts import create_inspect_object_prompt

from .interfaces import IObjectInspector

logger = logging.getLogger(__name__)


class ObjectInspector(IObjectInspector):
    """Handles inspection of useless/non-clue objects"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def inspect_object(self, object_name: str) -> str:
        """
        Give a simple answer for a useless object
        
        Args:
            object_name: Name of the object to inspect
            
        Returns:
            Simple response about the object
        """
        try:
            prompt: str = create_inspect_object_prompt(object_name)
            
            # Check cache first
            cache_context = {
                "type": "useless_object",
                "object": str(object_name)
            }
            
            cached_result = self.cache.get(
                prompt,
                {"temperature": 0.5},
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print(f"🚀 CACHE HIT: Object inspection found in cache for {object_name}")
                return cached_result
            
            messages = [{"role": "system", "content": prompt}]
            system_content = "You are a perceptive detective analyzing objects."

            content = self.api_service.make_api_call(
                messages=messages, 
                system_content=system_content, 
                max_tokens=APIConfig.MAX_TOKENS_SMALL,
            )

            # Always define result with a fallback
            if content:
                result = content
            else:
                result = "There is nothing special."
            
            # Store in cache
            self.cache.put(
                prompt,
                {"temperature": 0.5},
                result,
                cache_context
            )

            if self.dev_mode:
                print(f"💾 CACHE MISS: Generated and cached object inspection for {object_name}")

            return result

        except Exception as e:
            logger.error(f"Error in inspect_object: {e}")
            return "There is nothing special."