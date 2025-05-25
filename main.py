
from typing import Optional
import anthropic
import os
import pandas as pd
import sys

client = anthropic.Anthropic(
    # This will automatically use the ANTHROPIC_API_KEY environment variable
    # or you can pass the key directly: api_key="your-api-key-here"
)

def generate_text(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1000,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None
) -> str:
    """
    Generate text using Claude API
    
    Args:
        prompt: The user's input prompt
        model: Claude model to use
        max_tokens: Maximum tokens in response
        temperature: Controls randomness (0.0 = deterministic, 1.0 = very random)
        system_prompt: Optional system message to set Claude's behavior
    
    Returns:
        Generated text response
    """
    try:
        # Prepare messages
        messages = [{"role": "user", "content": prompt}]
        
        # Create the request
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt if system_prompt else "",
            messages=messages
        )
        
        return response.content[0].text
        
    except anthropic.APIError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def read_sprint_backlog(file_path):
    """
    Read sprint backlog from Excel file and return as array of dictionaries
    
    Args:
        file_path (str): Path to the Excel file
    
    Returns:
        list: Array of sprint backlog items
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Verify required columns exist
        required_columns = ['storyName', 'story', 'doneConditions', 'workItemId']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return []
        
        # Convert DataFrame to array of dictionaries
        backlog_items = df.to_dict('records')
        
        return backlog_items
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return []

def sketchSprintTasks(backlog_items, teamStandards):
    """
    Print sprint backlog items in a formatted way
    
    Args:
        backlog_items (list): Array of sprint backlog items
    """
    if not backlog_items:
        print("No backlog items to display.")
        return
    
    print("=" * 40)
    print("SPRINT BACKLOG")
    print("=" * 40)
    
    for i, item in enumerate(backlog_items, 1):
        print(f"\n--- Item #{i} ---")
        print(f"Work Item ID: {item.get('workItemId', 'N/A')}")
        print(f"Story Name: {item.get('storyName', 'N/A')}")
        print(f"Story: {item.get('story', 'N/A')}")
        print(f"Done Conditions: {item.get('doneConditions', 'N/A')}")
        print("-" * 40)

        storyName = item.get('storyName', 'N/A')
        doneConditions = item.get('doneConditions', 'N/A')
        # create prompt
        prompt = f'''
        ## Context

        ### User story: 
        {storyName}

        ### Done conditions: 
        {doneConditions}
        
        ### Team standards: 
        {teamStandards}

        ## Intent
        Please generate user story tasks for the above user story and done conditions.
        The tasks should be clear, actionable, and follow the team standards.
        You do not need to include code samples, just the tasks.
        Keep tasks clear and 1 or 2 sentences long.
        The tasks should be in the format of a bullet list.
        '''

        print("===============")
        taskOutput = generate_text(prompt)
        print(taskOutput)

def test_llm():
    answer = generate_text("make a joke about developers.")
    print(answer)

def getTeamStandards():
    try:
        with open("team-standards-brief.md", "r") as file:
            standards = file.read()
        return standards
    except FileNotFoundError:
        return "Team standards file not found."

def main():
    """
    Main function to execute the sprint backlog reader
    """
    # You can change this to your Excel file path
    file_path = "backlog.xlsx"  # Change this to your file path
    
    # Allow command line argument for file path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    print(f"Reading sprint backlog from: {file_path}")
    
    # Read the sprint backlog from Excel
    backlog_array = read_sprint_backlog(file_path)

    teamStandards = getTeamStandards()
    
    # Print the sprint backlog items
    sketchSprintTasks(backlog_array,teamStandards)

if __name__ == "__main__":
    main()
    
