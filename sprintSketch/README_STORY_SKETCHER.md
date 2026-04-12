# Story Sketcher - User Story Generator

A clean architecture Python application that reads project scope from a markdown file and generates INVEST-compliant user stories using Claude AI.

## Architecture

The application follows **Clean Architecture** principles with the following layers:

### Core Layer (`core/`)
- **models.py**: Domain models following Ardalis/Smith clean architecture
  - `Scope`: Project scope domain model
  - `UserStory`: User story domain model following INVEST principles
  - `AcceptanceCriteria`: Testable acceptance criteria
  - `StoryGenerationResult`: Application result object (reports success/failure/errors)

- **services.py**: Application services orchestrating business logic
  - `StoryGenerationService`: Core business logic for story generation
  - Uses injected LLM provider (interface-based dependency)
  - Builds prompts following the LLM Prompt Design specification

### Infrastructure Layer (`infra/`)
- **llm_provider.py**: LLM service implementations
  - `ILLMProvider`: Abstract interface (dependency inversion)
  - `ClaudeLLMProvider`: Concrete Claude API implementation
  
- **file_provider.py**: File I/O implementations
  - `IFileProvider`: Abstract interface
  - `MarkdownFileProvider`: Reads scope and writes stories in markdown

### Main Application (`story_sketcher.py`)
- Console interface for user interaction
- Dependency injection and orchestration
- Output formatting

## How It Works

### 1. LLM Prompt Design Layers

The application implements three-layer prompt design:

**Layer 1: System Layer** - Agent constitution
- Defines the AI's role as an Agile PM specialist
- Establishes INVEST principle standards
- Describes output format expectations

**Layer 2: Developer Layer** - Session context
- Injects project goals, constraints, and scope
- Provides user and business context
- Specifies output format

**Layer 3: User Layer** - The request
- Simple, clear request for N user stories

### 2. INVEST Principles

All generated user stories adhere to the INVEST coaching:
- **I**ndependent - Stories don't depend on each other
- **N**egotiable - Details can evolve through conversation
- **V**aluable - Clear user/business value
- **E**stimable - Team can reasonably size it
- **S**mall - Fits within a single sprint
- **T**estable - Clear acceptance criteria

### 3. Clean Architecture

**Dependency Rule**: Dependencies point inward
- Core has zero dependencies on external frameworks
- Services depend on interfaces, not implementations
- Easy to test core business logic
- Easy to swap LLM providers (Claude → Gemini, etc.)

**Domain-Driven Design**:
- Models represent domain concepts
- Services contain business logic
- Results object provides consistent error handling

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Usage

### Quick Start

```bash
python story_sketcher.py
```

The program will prompt for:
1. Path to scope markdown file (default: `scope.md`)
2. Number of stories to generate (default: 5)
3. Output file path (default: `output.md`)

### Scope File Format

Create a `scope.md` file with this structure:

```markdown
# Project Title

## Description
Brief description of the project and its purpose.

## Goals
- Goal 1
- Goal 2
- Goal 3

## Constraints
- Constraint 1
- Constraint 2
```

**Example:** See `scope.md` for an e-learning platform example.

### Output

The program generates `output.md` containing:
- Project scope summary
- Numbered user stories (3-5 stories typically)
- Each story with:
  - Clear title
  - "As a... I want... so that..." format
  - 3-5 testable acceptance criteria
  - Structured as markdown for easy integration

## Example Output

```markdown
# User Stories - E-Learning Platform MVP

**Generated:** 2024-04-12 10:30:00

## Scope

**Description:** A simple web-based platform...

### Goals
- Enable instructors to upload content
- Allow students to track progress
...

## User Stories

> **INVEST Principles:** Independent | Negotiable | Valuable | Estimable | Small | Testable

### 1. User Registration and Authentication

As a student, I want to create an account and log in securely, so that I can access my courses and track my progress.

#### Acceptance Criteria
- User can register with email and password
- System validates email format and password strength
- User receives confirmation email
- User can log in with credentials
- Session persists across page refreshes
```

## Extending the Application

### Adding a New LLM Provider

1. Implement `ILLMProvider` interface:
```python
class GeminiLLMProvider(ILLMProvider):
    def generate(self, prompt: str) -> str:
        # Your Gemini API code
        pass
```

2. Inject into service:
```python
llm_provider = GeminiLLMProvider()
story_service = StoryGenerationService(llm_provider)
```

### Customizing Story Generation

Modify `StoryGenerationService` methods:
- `_get_system_prompt()`: Change coaching/tone
- `_get_developer_context()`: Add more context
- `_parse_stories()`: Adjust parsing logic

### Compliance with Specifications

- ✅ **clean_architecture.md**: Dependency inversion, layered architecture
- ✅ **llmPromptDesign.md**: Three-layer prompt design (system/developer/user)
- ✅ **investCoaching.md**: All stories follow INVEST principles

## Requirements

- Python 3.9+
- anthropic >= 0.18.0
- python-dotenv >= 1.0.0

## License

See LICENSE file
