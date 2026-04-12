"""
Infrastructure layer: File I/O operations
"""
from abc import ABC, abstractmethod
from typing import Optional
from core.models import Scope
import os


class IFileProvider(ABC):
    """
    Abstract interface for file operations.
    Core depends on this interface, not on concrete implementations.
    """
    
    @abstractmethod
    def read_scope(self, file_path: str) -> Scope:
        """Read scope from a file"""
        pass
    
    @abstractmethod
    def write_stories(self, file_path: str, content: str) -> bool:
        """Write stories to a file"""
        pass


class MarkdownFileProvider(IFileProvider):
    """
    Concrete implementation for reading/writing markdown files.
    """
    
    def read_scope(self, file_path: str) -> Scope:
        """
        Read scope from a markdown file.
        Expected format:
        # Project Title
        
        ## Description
        Brief description...
        
        ## Goals
        - Goal 1
        - Goal 2
        
        ## Constraints
        - Constraint 1
        - Constraint 2
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Scope file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the markdown
        return self._parse_scope_markdown(content)
    
    def write_stories(self, file_path: str, content: str) -> bool:
        """
        Write stories to a markdown file.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {str(e)}")
            return False
    
    def _parse_scope_markdown(self, content: str) -> Scope:
        """
        Parse markdown content into a Scope object.
        """
        lines = content.split("\n")
        
        title = ""
        description = ""
        goals = []
        constraints = []
        
        current_section = None
        
        for line in lines:
            line = line.rstrip()
            
            # Check for section headers
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            elif line.startswith("## Description"):
                current_section = "description"
            elif line.startswith("## Goals"):
                current_section = "goals"
            elif line.startswith("## Constraints"):
                current_section = "constraints"
            elif line.startswith("##"):
                current_section = None
            elif current_section and line.strip():
                # Parse list items
                if line.strip().startswith("-"):
                    item = line.strip()[1:].strip()
                    if current_section == "goals":
                        goals.append(item)
                    elif current_section == "constraints":
                        constraints.append(item)
                elif current_section == "description":
                    description += " " + line.strip()
        
        description = description.strip()
        
        if not title:
            title = "Untitled Project"
        
        if not goals:
            goals = ["Implement core functionality"]
        
        return Scope(
            title=title,
            description=description,
            goals=goals,
            constraints=constraints
        )
