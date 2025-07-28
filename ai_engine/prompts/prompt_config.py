import os


def get_current_language() -> str:
    """Get current language from service, fallback to environment, then default"""
    try:
        from frontend.services.language_service import get_current_language
        return get_current_language()
    except ImportError:
        # Fallback to environment variable if service not available
        return os.getenv('LANGUAGE', 'english')
    
def get_current_teleportation() -> bool:
    """Get current teleportation mode setting"""
    try:
        from frontend.services.game_option_service import get_current_teleportation
        return get_current_teleportation()
    except ImportError:
        # Fallback to environment variable if service not available
        import os
        return os.getenv('TELEPORTATION_MODE', 'false').lower() == 'true'

def get_rules_prompt() -> str:
    """Get language-specific rules prompt"""
    current_lang = get_current_language()
    return f"\n\nRespond in {current_lang.title()}.\n\n"

