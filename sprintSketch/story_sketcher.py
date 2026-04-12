"""
Story Sketcher - Main Application
Reads project scope and generates INVEST-compliant user stories using Claude.

Following Clean Architecture:
- Core: Business logic and domain models
- Infrastructure: LLM and file I/O implementations
- Main: User interface and orchestration
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models import Scope
from core.services import StoryGenerationService
from infra.llm_provider import ClaudeLLMProvider
from infra.file_provider import MarkdownFileProvider

# load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

def main():
    """Main program flow"""
    
    print("=" * 70)
    print("SPRINT SKETCH - User Story Generator")
    print("=" * 70)
    print()
    
    # Get input scope file
    scope_file = input("Enter the path to the scope markdown file (default: scope.md): ").strip()
    if not scope_file:
        scope_file = "scope.md"
    
    # Get output file
    output_file = input("Output file path (default: output.md): ").strip()
    if not output_file:
        output_file = "output.md"
    
    print()
    print("Processing... this may take a moment.")
    print()
    
    try:
        # Infrastructure setup
        file_provider = MarkdownFileProvider()
        llm_provider = ClaudeLLMProvider()
        
        # Read scope from file
        print(f"Reading scope from: {scope_file}")
        scope = file_provider.read_scope(scope_file)
        print(f"✓ Loaded scope: {scope.title}")
        print()
        
        # Create service with injected dependencies
        story_service = StoryGenerationService(llm_provider)
        
        # Generate stories
        print("Generating user stories...")
        result = story_service.generate_stories(scope)
        
        if not result.success:
            print(f"✗ Error: {result.message}")
            for error in result.errors:
                print(f"  - {error}")
            return 1
        
        # Format output
        output_content = _format_output(scope, result.stories)
        
        # Write to file
        print(f"Writing stories to: {output_file}")
        if file_provider.write_stories(output_file, output_content):
            print(f"✓ Successfully generated {len(result.stories)} user stories!")
            print()
            print("=" * 70)
            print("GENERATED STORIES")
            print("=" * 70)
            print()
            print(output_content)
            return 0
        else:
            print(f"✗ Failed to write output file: {output_file}")
            return 1
            
    except FileNotFoundError as e:
        print(f"✗ File error: {e}")
        return 1
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def _format_output(scope: Scope, stories) -> str:
    """Format the output markdown document"""
    
    lines = [
        f"# User Stories - {scope.title}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Scope",
        "",
        f"**Description:** {scope.description}",
        "",
        "### Goals",
        ""
    ]
    
    for goal in scope.goals:
        lines.append(f"- {goal}")
    
    lines.extend(["", "### Constraints", ""])
    
    if scope.constraints:
        for constraint in scope.constraints:
            lines.append(f"- {constraint}")
    else:
        lines.append("- None specified")
    
    lines.extend([
        "",
        "## User Stories",
        "",
        "> **INVEST Principles:** Independent | Negotiable | Valuable | Estimable | Small | Testable",
        ""
    ])
    
    for i, story in enumerate(stories, 1):
        lines.append(str(story))
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
