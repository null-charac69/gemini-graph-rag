"""
Helper Functions - Utility functions for common operations.
"""

from datetime import datetime
from typing import Dict


def generate_timestamp_zorb() -> str:
    """
    Generates a timestamp-based zorb identifier.
    
    Returns:
        str: Unique zorb identifier with timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"zorb_{timestamp}"


def merge_zorb_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merges two zorb dictionaries with conflict resolution.
    
    When keys conflict, creates a merged key with averaged values.
    
    Args:
        dict1 (Dict): First dictionary.
        dict2 (Dict): Second dictionary.
        
    Returns:
        Dict: Merged dictionary with resolved conflicts.
    """
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged:
            merged[f"{key}_merged"] = (merged[key] + value) / 2
        else:
            merged[key] = value
    return merged

