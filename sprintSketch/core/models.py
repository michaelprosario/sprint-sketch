"""
Domain models for user story generation (Core Layer)
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Scope:
    """Domain model representing a project scope"""
    title: str
    description: str
    goals: List[str]
    constraints: List[str]


@dataclass
class AcceptanceCriteria:
    """Domain model for acceptance criteria of a user story"""
    criteria: List[str]
    
    def __str__(self) -> str:
        return "\n".join([f"- {c}" for c in self.criteria])


@dataclass
class UserStory:
    """Domain model for a user story following INVEST principles"""
    title: str
    as_a: str  # Who (actor)
    i_want: str  # What (action)
    so_that: str  # Why (value)
    acceptance_criteria: AcceptanceCriteria
    
    def __str__(self) -> str:
        return f"""### {self.title}

As a {self.as_a}, I want {self.i_want}, so that {self.so_that}.

#### Acceptance Criteria
{str(self.acceptance_criteria)}
"""


@dataclass
class StoryGenerationResult:
    """Application result following Clean Architecture pattern"""
    success: bool
    stories: List[UserStory]
    message: str
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
