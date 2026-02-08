# DeepLens UI Screenshots

## Web UI (Gradio Interface)

### Main Interface
The web UI provides tabbed access to all agents:

```
┌─────────────────────────────────────────────────────────────────────┐
│  🔬 DeepLens: Multi-Agent Research Analysis                        │
│  Looking deeply beyond the surface of research hype                 │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ 🌐 Translate │ 🔬 Analyze │ 👨‍🔬 Evaluate │ 📈 Assess Trends│ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─ Translation Mode ──────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  Research Text or Buzzword:                                  │  │
│  │  ┌────────────────────────────────────────────────────────┐ │  │
│  │  │ attention mechanism                                     │ │  │
│  │  │                                                          │ │  │
│  │  └────────────────────────────────────────────────────────┘ │  │
│  │                                                               │  │
│  │  ☐ Treat as single buzzword                                 │  │
│  │                                                               │  │
│  │  [🔍 Translate]                                              │  │
│  │                                                               │  │
│  │  Results:                                                     │  │
│  │  ┌────────────────────────────────────────────────────────┐ │  │
│  │  │ ## 🔍 Buzzword: attention mechanism                    │ │  │
│  │  │                                                          │ │  │
│  │  │ Attention mechanisms allow neural networks to focus... │ │  │
│  │  └────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  💡 Tips:                                                            │
│  • Use Translate to understand complex research papers              │
│  • Use Analyze to identify research maturity                        │
│  • Use Evaluate to understand researcher strategies                 │
│  • Use Trends to detect hype and find underexplored areas          │
└─────────────────────────────────────────────────────────────────────┘
```

## Interactive CLI (Terminal Interface)

### Welcome Screen
```
╔══════════════════════════════════════════════════════════════════╗
║  🔬 DeepLens Interactive CLI                                     ║
║                                                                  ║
║  Looking deeply beyond the surface of research hype             ║
║                                                                  ║
║  Available Commands:                                             ║
║  1. Translate - Simplify research jargon and buzzwords          ║
║  2. Analyze - Identify problems, stages, and demand             ║
║  3. Evaluate - Assess researcher patterns                       ║
║  4. Trends - Evaluate technical trends and hype                 ║
║  5. Help - Show this help message                               ║
║  6. Exit - Quit the application                                 ║
╚══════════════════════════════════════════════════════════════════╝
```

### Translation Mode
```
🌐 Translation Mode
Translate research text to plain language

Is this a single buzzword? [y/N]: y
Enter buzzword: transformer architecture

⠋ Translating...

╭─ 🔍 Translation ──────────────────────────────────────────────╮
│ Buzzword: transformer architecture                            │
│                                                                │
│ The transformer architecture is a type of neural network      │
│ that revolutionized natural language processing. Think of it  │
│ as a system that can pay attention to different parts of text │
│ simultaneously...                                              │
╰────────────────────────────────────────────────────────────────╯
```

### Analysis Mode with Progress
```
🔬 Analysis Mode
Analyze research stage and demand

Enter research text (press Ctrl+D when done):
We propose a novel neural architecture search method...
^D

⠙ Analyzing...

╭─ 📊 Research Analysis ───────────────────────────────────────╮
│ Fundamental Problem: Automating the design of neural        │
│ network architectures...                                     │
│                                                              │
│ Research Stage: Scaling                                      │
│                                                              │
│ Stage Reasoning: The core concept (architecture search) is  │
│ proven, but this work focuses on making it more efficient... │
╰──────────────────────────────────────────────────────────────╯
```

## Launcher Menu
```
============================================================
🔬 DeepLens: Multi-Agent Research Analysis System
============================================================

Choose an interface:
  1. Web UI (Gradio) - Recommended for most users
  2. Interactive CLI (Terminal)
  3. Exit

Enter your choice (1-3): 1

🚀 Launching DeepLens UI on port 7860...
📝 Make sure your OPENAI_API_KEY is set in .env file

Running on local URL:  http://0.0.0.0:7860
```

## Feature Highlights

### Web UI Features
✨ Clean, modern interface with tabs
✨ Real-time results with formatted markdown
✨ Example inputs for quick testing
✨ Progress indicators for long operations
✨ Responsive design works on mobile
✨ No installation beyond Python packages

### CLI Features
✨ Rich terminal colors and formatting
✨ Interactive prompts with validation
✨ Spinner animations for progress
✨ Clean, bordered output panels
✨ Keyboard shortcuts
✨ Works over SSH

### Launcher Features
✨ Simple menu-driven interface
✨ Command-line arguments for automation
✨ Port configuration
✨ Share option for public URLs
✨ Auto-detects missing API key

## Usage Examples

### Starting Web UI
```bash
python launch.py --ui
python launch.py --ui --port 8080
python launch.py --ui --share  # Create public link
```

### Starting Interactive CLI
```bash
python launch.py --cli
```

### Using the API (Programmatic)
```python
from deeplens import DeepLensOrchestrator

orchestrator = DeepLensOrchestrator()
result = await orchestrator.explain_buzzword("attention mechanism")
```
