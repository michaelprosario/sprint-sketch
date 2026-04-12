"""
Application services (Core Layer)
Contains business logic for generating user stories
"""
from typing import List
from core.models import Scope, UserStory, AcceptanceCriteria, StoryGenerationResult


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
    
    def generate_stories(self, scope: Scope, num_stories: int = 5) -> StoryGenerationResult:
        """
        Core business logic: generate user stories from a scope.
        
        Args:
            scope: The scope containing project goals and context
            num_stories: Number of stories to generate
            
        Returns:
            StoryGenerationResult with success status and stories
        """
        try:
            # Build the prompt using the scope context
            prompt = self._build_generation_prompt(scope, num_stories)
            
            # Use the LLM provider (injected dependency)
            response = self.llm_provider.generate(prompt)
            
            # Parse the response into UserStory objects
            stories = self._parse_stories(response)
            
            if not stories:
                return StoryGenerationResult(
                    success=False,
                    stories=[],
                    message="No valid stories were generated",
                    errors=["LLM response did not contain valid user stories"]
                )
            
            return StoryGenerationResult(
                success=True,
                stories=stories,
                message=f"Successfully generated {len(stories)} user stories"
            )
            
        except Exception as e:
            return StoryGenerationResult(
                success=False,
                stories=[],
                message="Error generating stories",
                errors=[str(e)]
            )
    
    def _build_generation_prompt(self, scope: Scope, num_stories: int) -> str:
        """
        Build the LLM prompt following the LLM Prompt Design spec.
        Layers: System (constitution) + Developer (context) + User (request)
        """
        system_layer = self._get_system_prompt()
        developer_layer = self._get_developer_context(scope)
        user_layer = self._get_user_request(num_stories)
        
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

Output Format: Return stories as a structured list, one per block, clearly labeled."""
    
    def _get_user_request(self, num_stories: int) -> str:
        """Layer 3: User Layer - The actual request"""
        return f"""Please generate exactly {num_stories} user stories for this project scope.
Each story must follow INVEST principles and include acceptance criteria."""
    
    def _parse_stories(self, response: str) -> List[UserStory]:
        """
        Parse LLM response into UserStory objects.
        Simple parser that looks for story structure patterns.
        """
        stories = []
        
        # Split by numbered sections or "story" markers
        blocks = response.split("###")
        
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            try:
                story = self._parse_story_block(block)
                if story:
                    stories.append(story)
            except Exception:
                # Skip malformed blocks
                continue
        
        return stories
    
    def _parse_story_block(self, block: str) -> UserStory:
        """
        Parse a single story block into a UserStory object.
        Expected format:
        Story Title
        As a [actor], I want [action], so that [value].
        
        Acceptance Criteria
        - criterion 1
        - criterion 2
        """
        lines = block.strip().split("\n")
        
        title = lines[0].strip() if lines else "Untitled"
        
        # Find the "As a..." line
        story_line = ""
        criteria_start = -1
        
        for i, line in enumerate(lines[1:], 1):
            if "as a" in line.lower():
                story_line = line.strip()
            if "acceptance criteria" in line.lower() or "criteria:" in line.lower():
                criteria_start = i
                break
        
        if not story_line:
            # Try to use the second line if it looks right
            if len(lines) > 1:
                story_line = lines[1].strip()
            else:
                raise ValueError("No story line found")
        
        # Parse the story line: "As a X, I want Y, so that Z"
        as_a, i_want, so_that = self._parse_story_line(story_line)
        
        # Extract acceptance criteria
        acceptance_criteria = []
        if criteria_start > 0:
            for line in lines[criteria_start + 1:]:
                line = line.strip()
                if line.startswith("-"):
                    acceptance_criteria.append(line[1:].strip())
                elif line and not line.startswith("#"):
                    acceptance_criteria.append(line)
        
        if not acceptance_criteria:
            acceptance_criteria = ["Implementation meets requirements", "Code is tested and reviewed"]
        
        return UserStory(
            title=title,
            as_a=as_a,
            i_want=i_want,
            so_that=so_that,
            acceptance_criteria=AcceptanceCriteria(acceptance_criteria)
        )
    
    def _parse_story_line(self, line: str) -> tuple:
        """Parse 'As a X, I want Y, so that Z' format"""
        # Remove common prefixes
        line = line.lower()
        
        # Split by commas to extract parts
        parts = [p.strip() for p in line.split(",")]
        
        as_a = ""
        i_want = ""
        so_that = ""
        
        for part in parts:
            if part.startswith("as a "):
                as_a = part[5:].strip()
            elif part.startswith("i want "):
                i_want = part[7:].strip()
            elif part.startswith("so that "):
                so_that = part[8:].strip()
        
        if not as_a:
            as_a = "user"
        if not i_want:
            i_want = "complete the task"
        if not so_that:
            so_that = "achieve the goal"
        
        return as_a, i_want, so_that
