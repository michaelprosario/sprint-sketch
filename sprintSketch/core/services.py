"""
Application services (Core Layer)
Contains business logic for generating user stories
"""
from core.models import Scope, StoryGenerationResult


class StoryGenerationService:
    """
    Application service that orchestrates user story generation.
    Depends on abstractions (providers), not concrete implementations.
    """

    def __init__(self, llm_provider):
        """
        Args:
            llm_provider: Implementation of ILLMProvider interface
        """
        self.llm_provider = llm_provider

    def generate_stories(self, scope: Scope) -> StoryGenerationResult:
        """
        Core business logic: generate user stories from a scope.

        Args:
            scope: The scope containing project goals and context

        Returns:
            StoryGenerationResult with success status and markdown content
        """
        try:
            prompt = self._build_generation_prompt(scope)
            response = self.llm_provider.generate(prompt)

            if not response or not response.strip():
                return StoryGenerationResult(
                    success=False,
                    markdown="",
                    message="No content was generated",
                    errors=["LLM returned an empty response"]
                )

            return StoryGenerationResult(
                success=True,
                markdown=response,
                message="Successfully generated user stories"
            )

        except Exception as e:
            return StoryGenerationResult(
                success=False,
                markdown="",
                message="Error generating stories",
                errors=[str(e)]
            )

    def _build_generation_prompt(self, scope: Scope) -> str:
        """
        Build the LLM prompt following the LLM Prompt Design spec.
        Layers: System (constitution) + Developer (context) + User (request)
        """
        system_layer = self._get_system_prompt()
        developer_layer = self._get_developer_context(scope)
        user_layer = self._get_user_request()

        return f"""{system_layer}

{developer_layer}

{user_layer}"""

    def _get_system_prompt(self) -> str:
        """Layer 1: System Layer - Agent constitution"""
        return """You are an expert Agile project manager and user story crafting specialist.
Your role is to create high-quality user stories that follow the INVEST principles:
- Independent: Stories stand alone and can be delivered separately
- Negotiable: Stories are conversation starters, not rigid contracts
- Valuable: Each story delivers clear user or business value
- Estimable: The team can reasonably size the story
- Small: Stories fit within a single sprint
- Testable: Clear acceptance criteria allow verification

When generating stories, always structure them as:
As a [actor], I want [action], so that [value].

Follow with 3-5 clear, testable acceptance criteria."""

    def _get_developer_context(self, scope: Scope) -> str:
        """Layer 2: Developer Layer - Session context"""
        goals = "\n".join([f"- {goal}" for goal in scope.goals])
        constraints = "\n".join([f"- {constraint}" for constraint in scope.constraints])

        return f"""PROJECT CONTEXT:
Title: {scope.title}
Description: {scope.description}

Goals:
{goals}

Constraints:
{constraints}

Output Format: Return stories as a structured markdown document, one story per section, clearly labeled."""

    def _get_user_request(self) -> str:
        """Layer 3: User Layer - The actual request"""
        return """Please generate user stories for this project scope.
        Each story must follow INVEST principles and include acceptance criteria."""
