# 🕵️‍♂️ AI Detective Game - Whispered Mysteries

**⚠️ Experimental Game - Work in Progress ⚠️**

An interactive detective game powered by Azure OpenAI where you solve a murder mystery at Blackwood Manor. Each character is AI-powered with unique personalities and memories.

_Note: This is an experimental project with ongoing development. You may encounter bugs and features are continuously being improved._

**Currently supports Azure OpenAI only.** Support for other AI providers (Claude, etc.) is planned for future releases.

## 🎮 Game Features

- **Free Investigation**: Explore rooms, interrogate suspects, collect clues
- **AI-Powered Characters**: Each NPC has unique personality, memory, and reactions
- **Dynamic Reputation System**: Your actions affect how characters perceive you
- **Multiple Endings**: Success depends on your theory and evidence
- **Save/Load System**: Save your progress and continue later
- **AI Multi-language**: AI characters respond in your preferred language
- **Responsive UI**: Desktop-optimized interface

## 🛠️ Quick Start

### Prerequisites

- Python 3.10+
- Azure OpenAI access (currently the only supported AI provider)

### Setup

1. **Clone and install**:

```bash
git clone <repository>
cd ai-detective-game
pip install -r requirements.txt
```

2. **Configure environment**:
   Create `.env` file:

```env
# Required - Azure OpenAI
AZURE_OPENAI_API_KEY="your-api-key"
AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment-name"
API_VERSION="2023-03-15-preview"

# Optional - Game Settings
LANGUAGE=english
DEV_MODE=false
AI_CACHE_ENABLED=true
TELEPORTATION_MODE=false
```

3. **Run the game**:

```bash
python main.py
```

Access at: http://localhost:7860

## 🎯 How to Play

1. **Start**: Enter your detective name
2. **Explore**: Navigate rooms using natural language ("go to kitchen", "examine table")
3. **Investigate**: Talk to characters, collect clues, analyze evidence
4. **Solve**: Present your theory with culprit, motive, and evidence
5. **Win**: Match the correct solution or get close enough!

### Game Commands

- `talk to [character]` - Start conversations
- `go to [room]` - Move between rooms
- `examine [object]` - Inspect items and clues
- `look around` - Describe current room
- `inventory` - Check collected evidence
- `solve case` - Present your final theory

## 🏗️ Architecture

```
ai-detective-game/
├── ai_engine/          # AI processing with Azure OpenAI
│   ├── processors/     # Specialized AI handlers (character, command, story, theory)
│   ├── cache/          # Session-based response caching
│   └── prompts/        # AI prompt templates
│
├── game_engine/        # Core game logic
│   ├── models/         # Game objects (Player, Character, Room, Clue)
│   ├── services/       # Business logic (GameService, ConversationService, etc.)
│   └── interfaces/     # GameFacade - main interface
│
├── frontend/           # Gradio web interface
│   ├── ui/             # UI components and styling
│   ├── handlers/       # Event handlers and state management
│   └── services/       # Frontend services (language, maps, images)
│
└── data/               # Game content
    ├── characters/     # Character definitions and prompts
    ├── rooms/          # Room descriptions and connections
    ├── clues/          # Evidence and collectibles
    └── narratives/     # Story documents and images
```

## 🔧 Configuration Options

### Development Mode

```bash
DEV_MODE=true python main.py --debug
```

- Enables detailed logging
- Shows AI reasoning process
- Displays cache hit/miss statistics

### Language Settings

AI responses can be in different languages via Settings menu:

```env
LANGUAGE=french  # english, french, spanish, german, etc.
```

_Note: Only AI-generated content (character dialogues, descriptions) is translated. UI elements remain in English._

### Performance Options

```env
AI_CACHE_ENABLED=true      # Cache AI responses for better performance
TELEPORTATION_MODE=true    # Allow movement to any room
```

## 💾 Save System

- **Manual Save**: Use Settings > Save/Load to export save files
- **Load Game**: Upload previous save files to continue
- **File Format**: JSON files with complete game state

## 🎨 Game Modes

1. **Exploration**: Navigate and investigate freely
2. **Conversation**: AI-powered character dialogues
3. **Final Confrontation**: Present your murder theory
4. **Game Over**: Multiple endings based on your performance

## 🤖 AI Features

- **Character Personalities**: Each NPC has distinct traits and responses
- **Memory System**: Characters remember your interactions
- **Reputation Tracking**: Your behavior affects how NPCs react
- **Dynamic Responses**: AI adapts to your investigation style
- **Multi-language AI**: AI responds in your preferred language (UI stays in English)

## 🐳 Docker Deployment

```bash
# Build and run
docker build -t ai-detective-game .
docker run -d -p 7860:7860 --env-file .env ai-detective-game
```

## 📝 API Endpoints

- `GET /` - Game interface
- `GET /health` - Health check
- `GET /api/status` - System status
- `GET /api/logs/status` - Logging info (dev mode)

## 🐛 Known Issues & Limitations

This is an **experimental game** under active development:

- **AI Responses**: Occasional inconsistencies or unexpected behavior
- **Performance**: May experience delays during AI processing
- **Save System**: Manual save/load only - no automatic progress saving
- **AI Provider**: Azure OpenAI only (Claude, OpenAI API support planned)
- **Language Support**: Partial - AI content only (inventory, menus stay in English)
- **UI**: Optimized for desktop browsers, mobile support limited
- **Stability**: Some edge cases may cause unexpected errors

## 🔍 Troubleshooting

**Game won't start**:

- Check Azure OpenAI credentials in `.env`
- Verify Python 3.10+ is installed
- Install requirements: `pip install -r requirements.txt`

**AI responses are slow**:

- Enable caching: `AI_CACHE_ENABLED=true`
- Check network connection to Azure

**Characters not responding**:

- Verify deployment name matches your Azure setup
- Check Azure OpenAI quotas and limits

## 🧩 Game Content

- **17 Rooms**: Full manor to explore
- **7 Characters**: Each with unique personality and secrets
- **15+ Clues**: Evidence to collect and analyze
- **5 Scenarios**: Multiple possible solutions
- **3 Attempts**: Limited chances to solve the case

## 💡 Tips for Players

1. **Talk to everyone**: Each character has valuable information
2. **Explore thoroughly**: Clues are hidden throughout the manor
3. **Take notes**: Remember conversations and evidence
4. **Watch your reputation**: Nonsense actions affect character reactions
5. **Think logically**: Motive, opportunity, and evidence must align

## 🎭 Character AI System

Each character has:

- **Personality Traits**: Authoritative, charming, nervous, etc.
- **Role-based Knowledge**: What they know about the murder
- **Memory System**: Remembers your conversations
- **Reputation Awareness**: Reacts to your behavior
- **Dynamic Responses**: AI-generated dialogue based on context

---

**Ready to solve the mystery at Blackwood Manor?** 🏚️🔍

_Experimental detective game - expect bugs and improvements along the way!_

Run `python main.py` and begin your investigation!
