import math
import copy

"""
Transformation Rule Natural Language Description:

1.  Identify the first contiguous horizontal sequence (block) of 2 or more identical non-white (not 0) pixels in the input row. This is the "pattern". Note its sequence of values, its color, and its length.
2.  If no such pattern is found, the output is identical to the input.
3.  Identify all "target" pixels in the input row. A target pixel is a single non-white pixel that:
    a. Has the same color as the identified pattern.
    b. Is "isolated", meaning the pixel immediately to its left is white (0) or it's the first pixel in the row, AND the pixel immediately to its right is white (0) or it's the last pixel in the row.
4.  Create a copy of the input row to serve as the output row.
5.  For each identified target pixel at index `i`:
    a. Calculate the starting index for replacement in the output row: `start_index = i - floor(pattern_length / 2)`.
    b. Overwrite the segment of the output row starting at `start_index` with the `pattern` sequence. Ensure writing stays within the row boundaries (0 to length-1). If the pattern extends beyond the boundaries, only the parts within the boundaries are written.
6.  Return the modified output row, wrapped in a list to represent the grid format.
"""

def find_first_pattern(grid_row):
    """
    Finds the first contiguous sequence of 2 or more identical non-white pixels.

    Args:
        grid_row: A list of integers representing the input row.

    Returns:
        A tuple (pattern, pattern_color, pattern_length) where:
        - pattern: A list of integers representing the pattern sequence.
        - pattern_color: The integer color value of the pattern.
        - pattern_length: The length of the pattern sequence.
        Returns (None, -1, 0) if no such pattern is found.
    """
    n = len(grid_row)
    i = 0
    while i < n:
        current_color = grid_row[i]
        # Look for start of a potential pattern (non-white)
        if current_color != 0:
            start_index = i
            j = i + 1
            # Find the end of the contiguous block of the same color
            while j < n and grid_row[j] == current_color:
                j += 1
            
            length = j - start_index
            # Check if the block meets the pattern criteria (length >= 2)
            if length >= 2:
                pattern = grid_row[start_index:j]
                return pattern, current_color, length
            else:
                # Block was too short, continue searching from the end of this block
                i = j 
        else:
            # Current pixel is white, move to the next
            i += 1
            
    # No pattern found after checking the whole row
    return None, -1, 0

def find_isolated_targets(grid_row, pattern_color):
    """
    Finds indices of isolated single pixels matching the pattern_color.
    Isolated means surrounded by white (0) or grid boundaries.

    Args:
        grid_row: A list of integers representing the input row.
        pattern_color: The integer color value to match.

    Returns:
        A list of integer indices where isolated target pixels are found.
    """
    n = len(grid_row)
    target_indices = []
    if pattern_color == -1: # No pattern means no targets
        return []
        
    for i in range(n):
        # Check if the current pixel matches the pattern color
        if grid_row[i] == pattern_color:
            # Check left neighbor (is it white or boundary?)
            left_is_isolated = (i == 0) or (grid_row[i-1] == 0)
            # Check right neighbor (is it white or boundary?)
            right_is_isolated = (i == n-1) or (grid_row[i+1] == 0)
            
            # If isolated on both sides, it's a target
            if left_is_isolated and right_is_isolated:
                 target_indices.append(i)
                 
    return target_indices


def transform(input_grid):
    """
    Applies the pattern replacement transformation to the input grid.

    Args:
        input_grid: A list containing a single list of integers (the input row).
                    Example: [[0, 0, 7, 7, 7, 0, ...]]

    Returns:
        A list containing a single list of integers (the transformed row).
        Returns a copy of the input_grid if no pattern is found.
    """
    # Ensure input is in the expected format and handle potential NumPy conversion
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
         # Or raise an error, or return input depending on desired robustness
         return copy.deepcopy(input_grid) 
         
    input_row = list(input_grid[0]) # Convert to list to avoid NumPy issues
    output_row = list(input_row)    # Create a mutable copy for the output
    n = len(input_row)

    # 1. Find the pattern
    pattern, pattern_color, pattern_length = find_first_pattern(input_row)

    # 2. If no pattern found, return the original grid (as a copy)
    if pattern is None:
        # Return the structure expected [[row]]
        return [output_row] 

    # 3. Find isolated targets matching the pattern color
    target_indices = find_isolated_targets(input_row, pattern_color)
    
    # 4. Replace targets in the output grid copy
    # Calculate the offset from the target index to the start of the pattern replacement
    start_offset = math.floor(pattern_length / 2)

    for i in target_indices:
        # Calculate where the pattern should start writing in the output row
        start_replace_index = i - start_offset
        
        # Iterate through the pattern and write it into the output row
        for k in range(pattern_length):
            current_write_index = start_replace_index + k
            # Check if the write index is within the bounds of the output row
            if 0 <= current_write_index < n:
                output_row[current_write_index] = pattern[k]

    # 5. Return the modified row wrapped in a list
    return [output_row]