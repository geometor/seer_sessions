import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D input grid based on the following rules:
1. Identifies a single contiguous block of pixels with a color other than white (0) or green (3).
2. Identifies a single green (3) marker pixel.
3. Counts the number of white (0) pixels located strictly between the end of the colored block and the green marker.
4. Creates a new grid of the same size, initialized with white (0).
5. Places the identified colored block into the new grid, shifted to the right from its original starting position by the count of intermediate white pixels.
6. Places the green (3) marker into the new grid at its original index.
7. The remaining pixels in the new grid stay white (0).
"""

# --- Helper Functions ---

def find_colored_block(grid: List[int]) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the main contiguous block of color (not 0 or 3).

    Args:
        grid: The 1D input grid (list of integers).

    Returns:
        A tuple (color, start_index, end_index, length) if found, else None.
    """
    block_color = -1
    block_start = -1
    block_end = -1
    
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 3: # Found a potential block pixel
            if block_start == -1: # Start of a new block
                block_color = pixel
                block_start = i
                block_end = i
            elif pixel == block_color: # Continuation of the current block
                block_end = i
            else: # Found a different color, means the first block ended
                # Assumes only one block exists as per problem description.
                break 
        elif block_start != -1: # Found 0 or 3 after a block started, block ends here
            break # Stop searching once the block ends
            
    if block_start != -1:
        block_length = block_end - block_start + 1
        return block_color, block_start, block_end, block_length
    else:
        # No block meeting the criteria was found
        return None 

def find_marker(grid: List[int], marker_color: int = 3) -> Optional[int]:
    """
    Finds the index of the first occurrence of the marker color.

    Args:
        grid: The 1D input grid (list of integers).
        marker_color: The color of the marker to find (default is 3 green).

    Returns:
        The index of the marker if found, else None.
    """
    try:
        # Use list.index() which finds the first occurrence
        return grid.index(marker_color)
    except ValueError:
        # Marker color not found in the list
        return None

def count_whitespace_between(grid: List[int], start_exclusive: int, end_exclusive: int) -> int:
    """
    Counts the number of white (0) pixels between two indices (exclusive).

    Args:
        grid: The 1D input grid (list of integers).
        start_exclusive: The index after which to start counting (e.g., block_end).
        end_exclusive: The index before which to stop counting (e.g., marker_index).

    Returns:
        The count of white pixels (0) in the specified range. Returns 0 if the range is invalid or empty.
    """
    count = 0
    # Ensure the range is valid and has at least one element to check
    # The range is (start_exclusive, end_exclusive)
    if end_exclusive > start_exclusive + 1:
        for i in range(start_exclusive + 1, end_exclusive):
            if grid[i] == 0:
                count += 1
    return count

# --- Main Transformation Function ---

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the block shift transformation based on intermediate whitespace.
    """
    
    # --- Validate Input and Extract Grid Row ---
    # Expecting a list containing a single list (the 1D row)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format, maybe return input or raise error
        # Returning original input for robustness in ARC context
        print("Error: Input format is not a single-row grid.")
        return input_grid 

    grid_row = input_grid[0]
    grid_length = len(grid_row)
    
    # --- Step 1 & 2: Identify Block and Marker ---
    block_info = find_colored_block(grid_row)
    marker_index = find_marker(grid_row, 3)

    # --- Handle Cases Where Elements Are Not Found ---
    # If the required elements aren't present, return the original grid
    if block_info is None:
        print("Warning: Could not find the colored block. Returning original grid.")
        return input_grid 
    if marker_index is None:
        print("Warning: Could not find the green marker (3). Returning original grid.")
        return input_grid 
        
    # Extract block details if found
    block_color, block_start, block_end, block_length = block_info
    
    # --- Step 3: Calculate Shift Distance ---
    # Count white pixels strictly between the block's end and the marker's index
    shift_distance = count_whitespace_between(grid_row, block_end, marker_index)

    # --- Step 4: Initialize Output Grid ---
    # Create a new list initialized with white (0) pixels
    output_row = [0] * grid_length
    
    # --- Step 5: Place Shifted Block ---
    # Calculate the new starting index for the block
    new_block_start = block_start + shift_distance
    
    # Copy the original block's color into the output grid row at the new position
    # Check for boundary conditions to prevent index errors
    for i in range(block_length):
        target_index = new_block_start + i
        # Ensure we don't write past the end of the grid
        if target_index < grid_length: 
            output_row[target_index] = block_color
        else:
            # Block shift goes out of bounds, stop placing pixels
            print(f"Warning: Shifted block placement truncated due to grid boundary (length={grid_length}).")
            break 

    # --- Step 6: Place Marker ---
    # Place the green marker at its original position in the output grid row
    # Check marker_index is valid (it should be if found previously, but double-check)
    if 0 <= marker_index < grid_length:
        output_row[marker_index] = 3
    else:
        # This case should ideally not happen if marker was found correctly
        print(f"Warning: Original marker index {marker_index} seems out of bounds for grid length {grid_length}.")
        
    # --- Step 7: Finalize Output ---
    # The rest of the grid remains white (0) due to initialization.
    # Wrap the result row in a list to match the required nested list format
    return [output_row]