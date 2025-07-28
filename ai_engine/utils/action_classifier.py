from enum import Enum
from typing import Dict, List
import re

class ActionSeverity(Enum):
    IMPROMPTU = "impromptu"
    AWKWARD = "awkward"  
    DANGEROUS = "dangerous"
    UNKNOWN = "unknown"

class ActionClassifier:
    """Classifie automatiquement les actions nonsense selon leur gravité"""
    
    # Patterns d'actions par catégorie
    IMPROMPTU_PATTERNS = [
        r"fart|burp|hiccup|belch",
        r"trip|stumble|slip", 
        r"sneeze|cough|yawn",
        r"minor.*social|small.*mistake|awkward.*silence"
    ]
    
    AWKWARD_PATTERNS = [
        r"sing|dance|shout|scream|yell",
        r"jump|crawl|roll|throw.*self",
        r"revolution|strange.*ritual|weird.*ceremony",
        r"strip|undress|inappropriate.*touch",
        r"propose.*marriage|declare.*love"
    ]
    
    DANGEROUS_PATTERNS = [
        r"hit|punch|slap|kick|attack|strike|beat",
        r"kill|murder|strangle|choke",
        r"destroy|break|smash|burn|vandalize",
        r"poison|deadly|lethal|dangerous.*substance",
        r"hate|racist|violent.*threat"
    ]
    
    @classmethod
    def classify_action(cls, command: str) -> ActionSeverity:
        """
        Classifie une action selon sa gravité
        
        Args:
            command: Commande du joueur
            
        Returns:
            ActionSeverity correspondante
        """
        command_lower = command.lower()
        
        # Vérifier les patterns dangereux en premier
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, command_lower):
                return ActionSeverity.DANGEROUS
        
        # Puis les patterns awkward
        for pattern in cls.AWKWARD_PATTERNS:
            if re.search(pattern, command_lower):
                return ActionSeverity.AWKWARD
        
        # Puis les patterns impromptu
        for pattern in cls.IMPROMPTU_PATTERNS:
            if re.search(pattern, command_lower):
                return ActionSeverity.IMPROMPTU
        
        # Par défaut, considérer comme awkward si non classifié
        return ActionSeverity.AWKWARD