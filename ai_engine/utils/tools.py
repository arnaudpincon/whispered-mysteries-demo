def get_required_receipt_fields():
    return [
        "documentTitle",
        "hospitalName",
        "nameInKanji",
        "nameInKana",
        "speciality",
        "issueDate",
        "startDate",
        "endDate",
        "claimAmount",
        "hospitalPoints",
        "surgeryPoints",
        "dpcPoints",
    ]


def get_receipt_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "extract_receipt_fields",
                "description": "Extracts key fields from OCR data of Japanese medical documents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "docFields": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "documentTitle": {"type": "string"},
                                    "hospitalName": {"type": "string"},
                                    "nameInKanji": {"type": "string"},
                                    "nameInKana": {"type": "string"},
                                    "speciality": {"type": "string"},
                                    "issueDate": {"type": "string", "format": "date"},
                                    "startDate": {"type": "string", "format": "date"},
                                    "endDate": {"type": "string", "format": "date"},
                                    "claimAmount": {"type": "number"},
                                    "hospitalPoints": {"type": "number"},
                                    "surgeryPoints": {"type": "number"},
                                    "dpcPoints": {"type": "number"},
                                },
                                "required": get_required_receipt_fields(),
                            },
                        }
                    },
                    "required": ["docFields"],
                },
            },
        }
    ]


def get_conversation_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "format_conversation_response",
                "description": "Formats conversation agent response in required JSON structure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "think": {
                            "type": "string",
                            "description": "Your internal reasoning process about how to respond (not shown to the player)",
                        },
                        "answer": {
                            "type": "string",
                            "description": "Your actual response as character to Detective",
                        },
                        "action": {
                            "type": "string",
                            "description": "Mode to use based on conversation state",
                        },
                    },
                    "required": ["think", "answer", "action"],
                },
            },
        }
    ]


def get_collect_theory_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "format_collect_theory_response",
                "description": "Formats collect theory agent response in required JSON structure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "think": {
                            "type": "string",
                            "description": "Your internal analysis of the detective's statements, noting what they've provided so far",
                        },
                        "culprit": {
                            "type": ["string", "null"],
                            "description": "The name of the suspect identified by the detective (null if not yet provided)",
                        },
                        "motive": {
                            "type": ["string", "null"],
                            "description": "The motive explained by the detective (null if not yet provided)",
                        },
                        "evidence": {
                            "type": ["string", "null"],
                            "description": "The evidence presented by the detective (null if not yet provided)",
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "True if all three elements (culprit, motive, evidence) are provided, false otherwise",
                        },
                        "valid": {
                            "type": "null",
                            "description": "Always null (this will be determined by the verification agent)",
                        },
                        "answer": {
                            "type": "string",
                            "description": "What you actually say to the detective. Be immersive and engaging in your responses",
                        },
                    },
                    "required": [
                        "think",
                        "culprit",
                        "motive",
                        "evidence",
                        "completed",
                        "valid",
                        "answer",
                    ],
                },
            },
        }
    ]


def get_analyse_theory_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "format_analyse_theory_response",
                "description": "Formats analyse theory agent response in required JSON structure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "think": {
                            "type": "string",
                            "description": "Your internal analysis of the detective's theory versus the scenarios",
                        },
                        "culprit_match": {
                            "type": "boolean",
                            "description": "True if the culprit matches a scenario",
                        },
                        "motive_match": {
                            "type": "boolean",
                            "description": "True if the motive matches that culprit's scenario",
                        },
                        "evidence_match": {
                            "type": "boolean",
                            "description": "True if at least 2 key pieces of evidence match that culprit's scenario",
                        },
                        "valid": {
                            "type": "boolean",
                            "description": "True if all three elements match one scenario",
                        },
                        "matching_scenario": {
                            "type": ["boolean", "object"],
                            "description": "The matching scenario if valid is true, false otherwise",
                        },
                        "scenario": {
                            "type": "integer",
                            "description": "The scenario number (1-5) if matching_scenario is true, otherwise 0",
                        },
                        "answer": {
                            "type": "string",
                            "description": "Your response to the detective",
                        },
                    },
                    "required": [
                        "think",
                        "culprit_match",
                        "motive_match",
                        "evidence_match",
                        "valid",
                        "matching_scenario",
                        "scenario",
                        "answer",
                    ],
                },
            },
        }
    ]


def get_write_ending_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "format_write_ending_response",
                "description": "Formats write ending agent response in required JSON structure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "think": {
                            "type": "string",
                            "description": "Your reasoning process and analysis of how to adapt the scenario",
                        },
                        "answer": {
                            "type": "string",
                            "description": "The final adapted narrative text that will be presented to the player",
                        },
                    },
                    "required": ["think", "answer"],
                },
            },
        }
    ]


def get_process_command_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "format_command_response",
                "description": "Formats the command processing response in required JSON structure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "think": {
                            "type": "string",
                            "description": "Your reasoning process, including: 1) Complete list of entities in game state, 2) language detection, 3) translation to English, 4) mapping of entity names to their canonical English versions, 5) verification that target exists in game state",
                        },
                        "valid": {
                            "type": "boolean",
                            "description": "Whether the command is valid and can be executed",
                        },
                        "action": {
                            "type": "string",
                            "enum": [
                                "speak",
                                "move",
                                "collect",
                                "look",
                                "help",
                                "conclude",
                            ],
                            "description": "Action name in English",
                        },
                        "target": {
                            "type": "string",
                            "description": "Action target using canonical English names that EXIST in game state",
                        },
                        "target_type": {
                            "type": "string",
                            "enum": [
                                "character",
                                "location",
                                "object",
                                "clue",
                                "inventory",
                                "unknown",
                            ],
                            "description": "Type of the target entity",
                        },
                        "alternatives": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Relevant suggestions for the current game state",
                        },
                        "message": {
                            "type": "string",
                            "description": "Brief message to display to the player",
                        },
                    },
                    "required": [
                        "think",
                        "valid",
                        "action",
                        "target",
                        "target_type",
                        "alternatives",
                        "message",
                    ],
                },
            },
        }
    ]

def get_character_pipeline_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "character_response_pipeline",
                "description": "Generate character response following the established 3-step pipeline",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "think": {
                            "type": "string",
                            "description": "Your internal reasoning process about how to respond (not shown to the player)"
                        },
                        "neutral_analysis": {
                            "type": "string",
                            "description": "Step 1: Your factual analysis of what the detective said"
                        },
                        "personality_enhancement": {
                            "type": "string",
                            "description": "Step 2: How you apply your personality traits to enhance the response"
                        },
                        "answer": {
                            "type": "string",
                            "description": "Step 3: Your final response as the character with full personality applied"
                        },
                        "action": {
                            "type": "string",
                            "enum": ["conversation", "exploration"],
                            "description": "Next game mode based on conversation state"
                        }
                    },
                    "required": ["think", "neutral_analysis", "personality_enhancement", "answer", "action"]
                }
            }
        }
    ]


def get_agent_tools(agent_type):
    """
    Retourne les outils appropriés selon le type d'agent

    Args:
        agent_type (str): Type d'agent ("conversation", "collect_theory", "analyse_theory", "write_ending", "process_command")

    Returns:
        list: Liste des outils pour le type d'agent spécifié
    """
    agent_tools = {
        "conversation": get_conversation_tools,
        "collect_theory": get_collect_theory_tools,
        "analyse_theory": get_analyse_theory_tools,
        "write_ending": get_write_ending_tools,
        "process_command": get_process_command_tools,
        "character_pipeline": get_character_pipeline_tools,
    }

    if agent_type in agent_tools:
        return agent_tools[agent_type]()
    else:
        raise ValueError(f"Type d'agent non supporté: {agent_type}")
