"""
Ending Writer Agent
Generates game endings based on player theory and scenario
"""

from ai_engine.prompts.prompt_config import get_rules_prompt


def create_write_ending(scenario: str, player_theory: str):
    """
    Generate ending prompt with dynamic language support and enforced JSON output
    
    Args:
        scenario: Scenario text content
        player_theory: Player's theory about the murder
        
    Returns:
        Formatted prompt for ending generation
    """
    rules_prompt = get_rules_prompt()
    
    scenario_instructions = _get_scenario_instructions(scenario, player_theory, rules_prompt)
    output_requirements = _get_output_requirements()
    json_structure = _get_json_structure()
    formatting_rules = _get_formatting_rules()
    
    return f"""# Final Confrontation - Game Master's Guide
        
        {scenario_instructions}
        
        {output_requirements}
        
        {json_structure}
        
        {formatting_rules}"""


def _get_scenario_instructions(scenario: str, player_theory: str, rules_prompt: str) -> str:
    """Build scenario adaptation instructions"""
    return f"""## Scenario Information
        {scenario}
        
        ## Player's Theory
        {player_theory}
        
        ## Instructions for the AI
        You must reproduce the scenario text almost exactly as it is, with only slight adaptations:
        1. Fully preserve the structure and essence of the original text
        2. Maintain the same culprit and primary motive
        3. Make only minor modifications to incorporate relevant elements from the player's theory
        4. Remove any lore elements or background details that are not mentioned in the player's theory
        5. {rules_prompt}
       
        IMPORTANT: The final text should be nearly identical to the original scenario, with only minor adjustments."""


def _get_output_requirements() -> str:
    """Get critical output requirements"""
    return """## CRITICAL OUTPUT REQUIREMENTS
        YOUR RESPONSE MUST BE VALID JSON FORMAT ONLY. No other text before or after the JSON."""


def _get_json_structure() -> str:
    """Get mandatory JSON structure"""
    return """## Mandatory JSON Structure
        You MUST provide your response as a JSON object with EXACTLY these two keys and NO OTHER KEYS:
        {
            "think": "Your detailed reasoning process and analysis of how to adapt the scenario. Include your thought process, what changes you're making and why, and how you're incorporating the player's theory while preserving the original scenario.",
            "answer": "The final adapted narrative text that will be presented to the player. This should be the complete story text with the minor adaptations applied."
        }
        
        ## FORBIDDEN STRUCTURES
        DO NOT create nested objects or additional keys such as:
        - "answer": {"text": "..."} ← WRONG
        - "answer": {"content": "..."} ← WRONG  
        - "answer": {"story": "..."} ← WRONG
        - Any other nested structure ← WRONG
        
        The "answer" value must be a STRING, not an object with sub-keys."""


def _get_formatting_rules() -> str:
    """Get JSON formatting rules"""
    return """## JSON Formatting Rules
        - Start your response with { and end with }
        - Use proper JSON escaping for quotes (use \\" for quotes within strings)
        - Ensure all text is properly formatted as JSON strings
        - Do not include any text outside the JSON structure
        - Validate that your response is parseable JSON before submitting
        
        REMINDER: Your entire response must be valid JSON with ONLY the "think" and "answer" keys. The "answer" must be a direct string value, NOT an object with nested keys like "text" or "content". No exceptions."""