import math
import copy

"""
Transformation Rule Natural Language Description:

1.  Create a mutable copy of the input grid's single row to serve as the `output_row`.
2.  Scan the input row from left to right to locate the first contiguous sequence of 2 or more identical non-white pixels (value > 0). If found, store this sequence as the `pattern`, its color as `pattern_color`, and its length as `pattern_length`.
3.  If no such `pattern` (length >= 2) is found in the input row, return the unmodified `output_row` (wrapped as a grid).
4.  Scan the input row to find all indices `i` corresponding to `target_pixels`. A pixel at index `i` is a target if its color matches `pattern_color` AND the pixel at `i-1` (if it exists) is white (0) AND the pixel at `i+1` (if it exists) is white (0). Handle boundary conditions (index 0 and the last index) appropriately as being isolated on that side.
5.  If no `target_pixels` are found, return the unmodified `output_row` (wrapped as a grid).
6.  For each identified `target_pixel` index `i`:
    *   Calculate the starting index for writing the pattern into the `output_row`: `start_index = i - floor(pattern_length / 2)`.
    *   Iterate through the `pattern` (from index `k = 0` to `pattern_length - 1`):
        *   Determine the `write_index` in the `output_row`: `write_index = start_index + k`.
        *   If `write_index` is a valid index within the bounds of the `output_row`, update the pixel at `output_row[write_index]` with the value `pattern[k]`.
7.  Return the final modified `output_row`, wrapped in a list to represent the grid format `[[modified_row]]`.
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
    # Cannot find targets if there's no valid pattern color (must be 1-9)
    if pattern_color <= 0: 
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
    Assumes input_grid is a list containing a single list (the row).
    """
    # Ensure input is in the expected format [[row]]
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
         # Return input unchanged if format is wrong
         # Using deepcopy to avoid modifying original input if it's passed around
         return copy.deepcopy(input_grid) 
         
    # Extract the single row (convert to list for safety/consistency)
    input_row = list(input_grid[0])
    
    # Step 1: Create a mutable copy for the output
    output_row = list(input_row)    
    n = len(input_row)

    # Step 2: Find the first pattern (sequence of 2+ identical non-white pixels)
    pattern, pattern_color, pattern_length = find_first_pattern(input_row)

    # Step 3: If no pattern is found, return the original grid copy
    if pattern is None:
        return [output_row] # Return in the expected [[row]] format

    # Step 4: Find isolated target pixels matching the pattern color
    target_indices = find_isolated_targets(input_row, pattern_color)
    
    # Step 5: If no targets found, return the grid copy
    if not target_indices:
         return [output_row]

    # Step 6: Replace targets in the output grid copy
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

    # Step 7: Return the modified row wrapped in a list
    return [output_row]