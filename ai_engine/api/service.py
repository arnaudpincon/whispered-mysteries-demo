import json
import logging
from typing import Any, Dict, List, Optional, Union

from openai import AzureOpenAI, OpenAIError
import httpx

from ai_engine.utils.tools import get_agent_tools

# Setup logging
logger = logging.getLogger(__name__)


class APIConfig:
    DEFAULT_TEMPERATURE = 0.7
    COMMAND_TEMPERATURE = 0.5
    ENDING_TEMPERATURE = 0.7
    MAX_TOKENS_SMALL = 100
    MAX_TOKENS_MEDIUM = 300
    MAX_TOKENS_LARGE = 800
    MAX_TOKENS_XLARGE = 1000
    MAX_TOKENS_XXLARGE = 1500
    API_TIMEOUT_SECONDS = 20.0


class APIService:
    """
    Centralized service for handling all OpenAI API interactions.
    Provides consistent error handling and response parsing with timeout support.
    """

    def __init__(self, client: AzureOpenAI, deployment_name: str) -> None:
        """
        Initialize the API service.
        Args:
            client: Configured Azure OpenAI client
            deployment_name: Model deployment name
        """
        self.client = client
        self.deployment_name = deployment_name
        
        # Configure timeout for the HTTP client
        if hasattr(self.client, '_client'):
            # Update the existing httpx client with timeout
            timeout = httpx.Timeout(APIConfig.API_TIMEOUT_SECONDS)
            self.client._client = httpx.Client(timeout=timeout)

    def make_api_call(
        self,
        messages: List[Dict[str, str]],
        system_content: Optional[str] = None,
        temperature: float = APIConfig.DEFAULT_TEMPERATURE,
        max_tokens: int = APIConfig.MAX_TOKENS_MEDIUM,
        tools: Optional[
            Union[List[Dict[str, Any]], str]
        ] = None,  # Can be agent_type string or tools list
        tool_choice: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        """
        Make an API call to the OpenAI service with error handling and timeout.
        Args:
            messages: List of message dictionaries for the conversation
            system_content: Optional system message content
            temperature: Sampling temperature for the model
            max_tokens: Maximum tokens in the response
            tools: Optional tools list OR agent_type string for auto JSON formatting
            tool_choice: Optional tool choice
            response_format: Optional response format specification
        Returns:
            API response content or None if error occurred
        """
        try:
            # Add system message if provided
            if system_content:
                messages = [{"role": "system", "content": system_content}] + messages

            # Convert tools if it's an agent_type string
            if isinstance(tools, str):
                agent_type = tools
                tools = get_agent_tools(agent_type)
                tool_name = tools[0]["function"]["name"]
                tool_choice = {"type": "function", "function": {"name": tool_name}}

            # Prepare API call parameters
            api_params = {
                "model": self.deployment_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "timeout": APIConfig.API_TIMEOUT_SECONDS,  # Add timeout parameter
            }

            # Add tools if provided
            if tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = tool_choice or "required"

            if response_format:
                api_params["response_format"] = response_format

            response = self.client.chat.completions.create(**api_params)

            # Handle tool calls if present (return JSON arguments)
            if (
                hasattr(response.choices[0].message, "tool_calls")
                and response.choices[0].message.tool_calls
            ):
                tool_call = response.choices[0].message.tool_calls[0]
                return tool_call.function.arguments  # Returns JSON string

            return response.choices[0].message.content

        except httpx.TimeoutException as e:
            logger.error(f"[API Timeout] Request timed out after {APIConfig.API_TIMEOUT_SECONDS} seconds: {e}")
            return None
        except httpx.ReadTimeout as e:
            logger.error(f"[API Read Timeout] Request read timed out: {e}")
            return None
        except httpx.ConnectTimeout as e:
            logger.error(f"[API Connect Timeout] Connection timed out: {e}")
            return None
        except OpenAIError as e:
            logger.error(f"[AI Refused] GPT rejected the prompt: {e}")
            return None
        except Exception as e:
            logger.error(f"[API Error] Unexpected error during API call: {e}")
            return None

    def parse_json_response(
        self, content: str, fallback_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse JSON responses with fallback handling.
        Args:
            content: JSON content string to parse
            fallback_response: Fallback response if parsing fails
        Returns:
            Parsed JSON dict or fallback response
        """
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {content}")
            return fallback_response