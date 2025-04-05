"""
Identifies the least frequent non-zero digit in the input grid, moves it to the 
geometric center of the grid, and sets its original location to zero. All other 
grid elements remain unchanged.
"""

import numpy as np
from collections import Counter
import math

def find_least_frequent_marker(grid):
    """
    Finds the non-zero digit with the minimum frequency and its location.
    Args:
        grid (np.array): The input grid.
    Returns:
        tuple: (marker_value, marker_row, marker_col) or (None, None, None) if no non-zero digit found.
    """
    non_zeros = grid[grid != 0]
    if non_zeros.size == 0:
        return None, None, None # No non-zero digits

    counts = Counter(non_zeros)
    
    # Find the minimum frequency
    min_freq = min(counts.values())
    
    # Find all digits that have the minimum frequency
    candidates = [digit for digit, freq in counts.items() if freq == min_freq]
    
    # In case of a tie in frequency, the problem description implies uniqueness.
    # We'll assume the first one found is the target, but a real-world scenario might need tie-breaking.
    marker_value = candidates[0] 
    
    # Find the location of the first occurrence of this marker value
    locations = np.argwhere(grid == marker_value)
    if locations.size > 0:
        marker_row, marker_col = locations[0] # Take the first location if multiple exist
        return marker_value, marker_row, marker_col
    else:
        # This case should ideally not happen if the marker_value came from the grid
        return None, None, None 

def calculate_center(grid):
    """
    Calculates the geometric center coordinates of the grid.
    Args:
        grid (np.array): The input grid.
    Returns:
        tuple: (center_row, center_col)
    """
    H, W = grid.shape
    center_row = (H - 1) // 2  # Integer division for center index
    center_col = (W - 1) // 2
    return center_row, center_col

def transform(input_grid):
    """
    Transforms the input grid by moving the least frequent non-zero digit to the center.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The transformed 2D grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # --- Step 1 & 2: Find the marker digit and its location ---
    marker_value, marker_row, marker_col = find_least_frequent_marker(input_np)

    # If no marker is found (e.g., all zeros), return the original grid
    if marker_value is None:
        return input_grid 

    # --- Step 3 & 4: Calculate the center position ---
    center_row, center_col = calculate_center(input_np)

    # --- Step 5: Create the output grid (copy of input) ---
    output_np = np.copy(input_np)

    # --- Step 6: Modify the output grid ---
    # Set original marker location to 0
    output_np[marker_row, marker_col] = 0
    # Place marker value at the center
    output_np[center_row, center_col] = marker_value

    # --- Step 7: Return the modified grid ---
    # Convert back to list of lists
    output_grid = output_np.tolist()
    return output_grid
