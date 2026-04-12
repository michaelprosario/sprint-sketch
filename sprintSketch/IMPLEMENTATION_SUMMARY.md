# Story Sketcher Implementation Summary

## ✅ What Was Created

A complete, professional **story-sketcher** console application that:

1. **Reads project scope** from a markdown file (e.g., `scope.md`)
2. **Generates INVEST-compliant user stories** using Claude AI
3. **Outputs structured markdown** with user stories and acceptance criteria
4. **Follows clean architecture** with clear separation of concerns
5. **Uses LLM prompt design** with three-layer prompting (system/developer/user)

## 📁 File Structure

```
sprintSketch/
├── story_sketcher.py              # Main console application
├── requirements.txt               # Python dependencies
├── scope.md                       # Sample scope file (E-Learning MVP)
├── sample_output.md               # Sample generated output
├── README_STORY_SKETCHER.md       # Complete documentation
│
├── core/                          # Core Layer (Business Logic)
│   ├── __init__.py
│   ├── models.py                  # Domain models (Scope, UserStory, etc.)
│   └── services.py                # Application service (StoryGenerationService)
│
└── infra/                         # Infrastructure Layer
    ├── __init__.py
    ├── llm_provider.py            # Claude API implementation
    └── file_provider.py           # Markdown file I/O
```

## 🎯 Key Features

### Clean Architecture Compliance
- **Dependency Inversion**: Core depends on interfaces (`ILLMProvider`, `IFileProvider`)
- **Layered Structure**: Clear separation between Core, Infrastructure, and UI
- **Minimal Dependencies**: Core has no external framework dependencies
- **Result Objects**: `StoryGenerationResult` reports success/failure/errors
- **Command/Query Pattern**: Services use structured input/output objects

### LLM Prompt Design Compliance
**Three-layer prompt architecture:**
- **Layer 1 (System)**: Defines AI role, INVEST principles, output format
- **Layer 2 (Developer)**: Injects project scope, goals, constraints
- **Layer 3 (User)**: Simple request for N user stories

### INVEST Principles Compliance
All generated user stories follow:
- **Independent**: Stories are deliverable independently
- **Negotiable**: Details are conversation starters
- **Valuable**: Clear user/business value
- **Estimable**: Reasonable scope for sizing
- **Small**: Fit within a sprint
- **Testable**: Clear acceptance criteria

## 🚀 Quick Start

### 1. Install dependencies
```bash
cd sprintSketch
pip install -r requirements.txt
```

### 2. Set your API key
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run the program
```bash
python story_sketcher.py
```

### 4. Follow the prompts
- Enter scope file path (default: `scope.md`)
- Enter number of stories (default: 5)
- Enter output file path (default: `output.md`)

### Example Output
The program generates markdown with:
- Project scope and goals
- Number of user stories with clear titles
- "As a... I want... so that..." format
- 3-5 testable acceptance criteria per story
- INVEST compliance callout

See `sample_output.md` for a complete example.

## 📋 Use Cases

### Agile Project Planning
- Generate initial backlog from project scope
- Use stories as conversation starters for refinement
- Validate scope and break down into deliverable increments

### Rapid Sprint Planning
- Load scope, generate stories in minutes
- Reduce manual story writing time
- Maintain consistency with INVEST principles

### Scope Definition
- Convert requirements document → markdown scope
- Generate stories → validate understanding
- Iterate to refine scope

## 🔧 Customization

### Change the LLM Provider
Implement `ILLMProvider` for any LLM (Gemini, GPT, etc.):

```python
from infra.llm_provider import ILLMProvider

class MyLLMProvider(ILLMProvider):
    def generate(self, prompt: str) -> str:
        # Your implementation
        pass

# Use it:
llm_provider = MyLLMProvider()
story_service = StoryGenerationService(llm_provider)
```

### Customize Story Prompt
Edit `StoryGenerationService._get_system_prompt()` to:
- Change tone or voice
- Add different guidance
- Modify output format

## ✅ Requirements Met

- ✅ Follow specs/clean_architecture.md
  - Dependency inversion principle
  - Layered architecture
  - Minimal core dependencies
  - Result objects for error handling

- ✅ Follow specs/llmPromptDesign.md
  - Three-layer prompt design
  - System constitution layer
  - Developer context layer
  - User request layer

- ✅ Follow specs/investCoaching.md
  - All stories follow INVEST criteria
  - Clear value proposition
  - Testable acceptance criteria
  - Appropriately sized

- ✅ Technology Stack
  - Python (3.9+)
  - Claude SDK (Anthropic API)
  - Console program (simple, focused)
  - Markdown I/O

- ✅ Deliverables
  - Console program ✓
  - Reads scope from markdown ✓
  - Generates user stories ✓
  - Outputs to markdown (output.md) ✓

## 📚 Documentation

- [README_STORY_SKETCHER.md](README_STORY_SKETCHER.md) - Complete documentation
- [scope.md](scope.md) - Example scope file
- [sample_output.md](sample_output.md) - Example output
- Code comments - Architecture and design decisions

## Next Steps

1. Update `scope.md` with your actual project scope
2. Add your `ANTHROPIC_API_KEY`
3. Run: `python story_sketcher.py`
4. Review generated `output.md`
5. Use stories for sprint planning
