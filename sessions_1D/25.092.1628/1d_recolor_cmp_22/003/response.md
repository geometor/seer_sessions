```python
"""
Transforms a 2D grid by iterating through each row, finding the longest 
contiguous horizontal segment of red (color 2) pixels within that row, 
and changing the color of the pixels within that specific segment to azure (color 8). 
All other pixels remain unchanged. If multiple segments share the maximum 
length in a row, the one encountered first (leftmost) is chosen.
"""

import numpy as np

def find_longest_segment_in_row(row: np.ndarray, target_color: int) -> tuple[int, int]:
    """
    Finds the start index and length of the longest contiguous segment 
    of target_color in a 1D NumPy array (row).

    Args:
        row: A 1D NumPy array representing a row of the grid.
        target_color: The integer color value to search for.

    Returns:
        A tuple (start_index, length). Returns (-1, 0) if no segment is found.
    """
    max_length = 0
    longest_start_index = -1
    
    current_start_index = -1
    current_length = 0
    
    n = len(row)
    
    for i in range(n):
        if row[i] == target_color:
            # Start or continue a segment
            if current_start_index == -1:
                current_start_index = i
            current_length = i - current_start_index + 1 # Calculate length up to current index
        else:
            # End of a segment (or not in one)
            if current_start_index != -1:
                # Check if the just-ended segment is the new longest
                if current_length > max_length:
                    max_length = current_length
                    longest_start_index = current_start_index
                # Reset current segment tracking
                current_start_index = -1
                current_length = 0
                
    # Check if the row ended while inside a segment
    if current_start_index != -1:
        if current_length > max_length:
            max_length = current_length
            longest_start_index = current_start_index
            
    # If no segment was ever found, longest_start_index remains -1
    # If segments were found, max_length will be > 0
    if longest_start_index != -1:
        return longest_start_index, max_length
    else:
        return -1, 0


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Define target and replacement colors
    target_color = 2  # red
    replacement_color = 8 # azure

    # Iterate through each row of the grid
    num_rows = input_grid.shape[0]
    for r in range(num_rows):
        current_row = input_grid[r, :]
        
        # Find the longest contiguous segment of the target color in this row
        start_index, length = find_longest_segment_in_row(current_row, target_color)
        
        # If a segment was found (length > 0)
        if length > 0:
            # Change the corresponding pixels in the output grid row
            output_grid[r, start_index : start_index + length] = replacement_color

    return output_grid
```