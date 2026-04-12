"""
Infrastructure layer: LLM Provider implementations
"""
from abc import ABC, abstractmethod
from anthropic import Anthropic
import os


class ILLMProvider(ABC):
    """
    Abstract interface for LLM providers (Dependency Inversion)
    Core depends on this interface, not on concrete implementations.
    """
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate text from the given prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            The generated text response
        """
        pass


class ClaudeLLMProvider(ILLMProvider):
    """
    Concrete implementation using Anthropic's Claude API.
    This infrastructure class implements the interface.
    """
    
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-6"):
        """
        Initialize the Claude LLM provider.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str) -> str:
        """
        Generate text using Claude API.
        
        Args:
            prompt: The complete prompt (including system, developer, and user layers)
            
        Returns:
            The generated text response
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")
