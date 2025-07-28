import os
from ai_engine.api.client import create_azure_client
from ai_engine.api.service import APIService
from ai_engine.cache.cache_decorators import get_ai_cache
from ai_engine.cache.session_cache_manager import get_cache_for_session
from ai_engine.processors.character.processor import CharacterProcessor
from game_engine.core.game_state import GameState
from game_engine.models.room import Room
from ..processors import CommandProcessor, StoryProcessor, TheoryProcessor


class AIManager:
    def __init__(self, api_key, endpoint, deployment_name, api_version, session_id: str = None):
        # Setup API
        client = create_azure_client(api_key, endpoint, api_version)
        self.api_service = APIService(client, deployment_name)
        self.dev_mode = os.getenv("DEV_MODE", "False").lower() == "true"
        
        # Get session-specific cache
        self.session_id = session_id
        if session_id:
            self.cache = get_cache_for_session(session_id)
            print(f"🔧 AIManager using session cache: {session_id}")
        else:
            # Fallback to default cache (for backwards compatibility)
            from ai_engine.cache.cache_decorators import get_ai_cache
            self.cache = get_ai_cache()
            print("⚠️ AIManager using default cache (no session ID provided)")
        
        # Créer les processors avec le cache de session
        self.command_processor = CommandProcessor(self.api_service, self.cache, self.dev_mode)
        self.character_processor = CharacterProcessor(self.api_service, self.cache, self.dev_mode)
        self.story_processor = StoryProcessor(self.api_service, self.cache, self.dev_mode)
        self.theory_processor = TheoryProcessor(self.api_service, self.cache, self.dev_mode)
    
    # Command processor
    def process_command(self, command: str, game_state):
        return self.command_processor.process_command(command, game_state)
    
    # Character processor
    def play_character(self, character, player, topic: str, game_state):
        return self.character_processor.play_character(character, player, topic, game_state)

    def conversation_summary(self, character, player) -> str:
        return self.character_processor.conversation_summary(character, player)

    def generate_character_description(self, character, room) -> str:
        return self.story_processor.generate_character_description(character, room)

    # Story processor  
    def generate_room_description(self, room, game_state: GameState, action: str) -> str:
        return self.story_processor.generate_room_description(room, game_state, action)

    def analyze_clue(self, clue, collected_clues=None) -> str:
        return self.story_processor.analyze_clue(clue, collected_clues)

    def give_useless_answer(self, object) -> str:
        return self.story_processor.give_useless_answer(object)

    # Theory processor
    def final_scene(self, player, conversation, game_state):
        return self.theory_processor.final_scene(player, conversation, game_state)

    def verify_theory(self, conversation):
        return self.theory_processor.verify_theory(conversation)

    def write_ending(self, scenario: int, player_theory: str):
        return self.theory_processor.write_ending(scenario, player_theory)
    
    def nonsense_reaction(self, command: str, game_state):
        """
        Generate reaction to nonsense actions with reputation awareness
        
        Args:
            command: Player's nonsense command
            game_state: Current game state (includes reputation data)
            
        Returns:
            Reaction considering reputation escalation
        """
        return self.command_processor.nonsense_reaction(command, game_state)