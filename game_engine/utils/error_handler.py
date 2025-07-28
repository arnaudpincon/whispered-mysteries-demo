"""Unified error handling for the game engine"""

import traceback
from typing import Any, Dict


class GameErrorHandler:
    """Centralized error handling for game operations"""

    @staticmethod
    def handle_command_error(error: Exception, command: str, context: str = "") -> Dict[str, Any]:
        """
        Handle errors during command processing
        
        Args:
            error: The exception that occurred
            command: The command that caused the error
            context: Additional context about where the error occurred
            
        Returns:
            Error response dictionary
        """
        error_message = f"An error occurred while processing your command: '{command}'"
        
        if context:
            error_message += f" (Context: {context})"
        
        # Log the full error for debugging
        print(f"ERROR in {context}: {str(error)}")
        print(f"   Command: {command}")
        if hasattr(error, '__traceback__'):
            print(f"   Traceback: {traceback.format_exc()}")
        
        return {
            "message": error_message,
            "error": True,
            "error_type": type(error).__name__,
            "command": command,
            "context": context
        }

    @staticmethod
    def handle_ai_error(error: Exception, context: str = "AI processing") -> str:
        """
        Handle AI-related errors gracefully
        
        Args:
            error: The AI-related exception
            context: Context of the AI operation
            
        Returns:
            User-friendly error message
        """
        print(f"AI ERROR in {context}: {str(error)}")
        
        # Return user-friendly message
        return "I'm having trouble understanding that right now. Could you try rephrasing your request?"

    @staticmethod
    def handle_state_error(error: Exception, operation: str) -> None:
        """
        Handle game state related errors
        
        Args:
            error: The state-related exception
            operation: The state operation that failed
        """
        print(f"STATE ERROR in {operation}: {str(error)}")
        print(f"Traceback: {traceback.format_exc()}")
