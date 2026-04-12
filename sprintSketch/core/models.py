"""
Domain models for user story generation (Core Layer)
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Scope:
    """Domain model representing a project scope"""
    title: str
    description: str
    goals: List[str]
    constraints: List[str]


@dataclass
class StoryGenerationResult:
    """Application result following Clean Architecture pattern"""
    success: bool
    markdown: str
    message: str
    errors: List[str] = field(default_factory=list)
