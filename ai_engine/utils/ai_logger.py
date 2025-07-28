"""
AI Response Logger
Simple colored logging system for AI responses
"""

import json
from typing import Any, Dict, Optional
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)


class AIResponseLogger:
    """Simple logger for AI responses with colors and JSON formatting"""
    
    def __init__(self, enabled: bool = True):
        """
        Initialize the logger
        
        Args:
            enabled: Whether logging is active
        """
        self.enabled = enabled
    
    def log_response(self, 
                    response: Any, 
                    source: str = "AI", 
                    response_type: str = "text") -> None:
        """
        Log an AI response with appropriate formatting
        
        Args:
            response: The AI response (can be string, dict, etc.)
            source: Source of the response (e.g., "CharacterProcessor", "CommandProcessor")
            response_type: Type of response ("json", "text", "error")
        """
        if not self.enabled:
            return
            
        # Header with source
        print(f"\n{Fore.CYAN}🤖 {source} Response:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'=' * 50}{Style.RESET_ALL}")
        
        # Format based on type
        if response_type == "json" or self._is_json_string(response):
            self._log_json_response(response)
        elif response_type == "error":
            self._log_error_response(response)
        else:
            self._log_text_response(response)
        
        print(f"{Fore.BLUE}{'=' * 50}{Style.RESET_ALL}\n")
    
    def _is_json_string(self, response: Any) -> bool:
        """Check if response is a JSON string"""
        if not isinstance(response, str):
            return False
        try:
            json.loads(response)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    def _log_json_response(self, response: Any) -> None:
        """Log JSON response with syntax highlighting"""
        try:
            if isinstance(response, str):
                data = json.loads(response)
            else:
                data = response
            
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Simple syntax highlighting
            for line in formatted_json.split('\n'):
                if '"think"' in line or '"answer"' in line:
                    print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                elif '"action"' in line or '"valid"' in line:
                    print(f"{Fore.YELLOW}{line}{Style.RESET_ALL}")
                elif any(key in line for key in ['"culprit"', '"motive"', '"evidence"']):
                    print(f"{Fore.MAGENTA}{line}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{line}{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}Error formatting JSON: {e}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{response}{Style.RESET_ALL}")
    
    def _log_text_response(self, response: Any) -> None:
        """Log plain text response"""
        print(f"{Fore.WHITE}{response}{Style.RESET_ALL}")
    
    def _log_error_response(self, response: Any) -> None:
        """Log error response"""
        print(f"{Fore.RED}❌ {response}{Style.RESET_ALL}")


# Global logger instance
_ai_logger = AIResponseLogger()

def log_ai_response(response: Any, 
                   source: str = "AI", 
                   response_type: str = "text") -> None:
    """
    Convenience function to log AI responses
    
    Args:
        response: The AI response
        source: Source processor name
        response_type: Type of response ("json", "text", "error")
    """
    _ai_logger.log_response(response, source, response_type)

def enable_ai_logging() -> None:
    """Enable AI response logging"""
    _ai_logger.enabled = True

def disable_ai_logging() -> None:
    """Disable AI response logging"""
    _ai_logger.enabled = False