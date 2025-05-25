import pandas as pd
from typing import List, Dict, Any


def read_backlog_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Read sprint backlog from an Excel file
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        List of dictionaries, each representing a backlog item
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Extract backlog items
        items = []
        current_item = {}
        
        for _, row in df.iterrows():
            if pd.notna(row.get('Work Item ID')):
                # Save the previous item if it exists
                if current_item:
                    items.append(current_item)
                
                # Start a new item
                current_item = {
                    'Work Item ID': int(row['Work Item ID']),
                    'Story Name': row.get('Story Name', ''),
                    'Story': row.get('Story', ''),
                    'Done Conditions': []
                }
            
            # Add done conditions
            if pd.notna(row.get('Done Conditions')):
                current_item['Done Conditions'].append(row['Done Conditions'])
        
        # Add the last item
        if current_item:
            items.append(current_item)
        
        return items
        
    except Exception as e:
        print(f"Error reading backlog from Excel: {e}")
        return []
