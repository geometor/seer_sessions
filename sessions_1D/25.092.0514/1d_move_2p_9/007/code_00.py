import numpy as np
from typing import List, Tuple, Optional, Union

"""
Transforms a single-row input grid by identifying the first contiguous block of a 
single non-white color and shifting this block two positions horizontally 
to the right. The space vacated by the block becomes white (0), and the 
background remains white. The block retains its original color and length, 
though it might be truncated if the shift moves it partially off the right edge 
of the grid. The output grid has the same dimensions as the input grid and is 
returned in the standard ARC format (List[List[int]]). Handles potential input 
format variations (List[int] or List[List[int]]).
"""

def find_contiguous_block(row: np.ndarray) -> Tuple[Optional[int], Optional[int], int]:
    """
    Finds the start index, color, and length of the first contiguous 
    non-white block in a 1D numpy array (row).

    Args:
        row: A 1D numpy array representing the input row.

    Returns:
        A tuple containing:
        - start_index (int or None): The starting index of the block, or None if no block found.
        - color (int or None): The color of the block, or None if no block found.
        - length (int): The length of the block (0 if no block found).
    """
    start_index = None
    color = None
    length = 0
    width = len(row)

    # Iterate through the row to find the first non-white pixel
    for i in range(width):
        if row[i] != 0:
            start_index = i
            color = int(row[i]) # Ensure color is standard int
            break # Found the start of the block

    # If a block start was found, determine its length
    if start_index is not None:
        current_length = 0 # Use a separate counter for length calculation
        for i in range(start_index, width):
            if row[i] == color:
                current_length += 1
            else:
                break # End of the contiguous block of the same color
        length = current_length

    return start_index, color, length

# Define a type hint that accepts either List[int] or List[List[int]]
GridInputType = Union[List[List[int]], List[int]]

def transform(input_grid: GridInputType) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Identifies a contiguous non-white block in the single-row input grid 
    and shifts it two positions to the right in the output grid, handling truncation.

    Args:
        input_grid: Input data representing a single row. Can be List[List[int]] 
                    (with one inner list) or List[int].

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    
    # --- Input Handling and Normalization ---
    # Check if input is List[List[int]] and extract the first row if so
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         if len(input_grid) > 1:
              # Based on examples, we expect only one row. Handle unexpected multi-row input.
              # Consider logging a warning or raising a specific error if strict adherence is needed.
              # For robustness, we'll process only the first row.
              pass # Process input_grid[0]
         input_row_list = input_grid[0]
    # Check if input is already List[int]
    elif isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
         input_row_list = input_grid
    # Handle empty or invalid formats
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list) and len(input_grid[0]) == 0:
         # Handle case like [[]]
         return [[]]
    elif isinstance(input_grid, list) and len(input_grid) == 0:
         # Handle case like [] - interpret as empty grid? Return [[]] for consistency.
         return [[]]
    else:
         # Invalid format not directly handled, raise error or return default
         raise ValueError("Invalid input grid format. Expected List[int] or List[List[int]] representing a single row.")

    # Convert the extracted row list to a numpy array
    input_row = np.array(input_row_list, dtype=int)
    width = len(input_row)

    # Handle empty row case after potential extraction
    if width == 0:
        return [[]] # Return an empty row within a list

    # --- Core Transformation Logic ---
    # Initialize the output grid as a row filled with background color (0)
    output_row = np.zeros(width, dtype=int)

    # Find the non-white block details in the input row
    start_index, block_color, block_length = find_contiguous_block(input_row)

    # If a block was found, calculate its new position and place it in the output row
    if start_index is not None and block_color is not None:
        # Calculate the new starting position by shifting right by 2
        new_start_index = start_index + 2
        
        # Place the block's color in the output grid, handling truncation
        # Iterate for the original length of the block
        for i in range(block_length):
            # Calculate the target index in the output row for this part of the block
            target_index = new_start_index + i
            
            # Check if the target index is within the grid bounds [0, width)
            if 0 <= target_index < width:
                # If within bounds, place the block's color
                output_row[target_index] = block_color
            # If target_index is >= width, the block is truncated, so do nothing more for this i or subsequent i's

    # --- Output Formatting ---
    # Convert the final numpy output row back into a standard list
    output_list = output_row.tolist()
    
    # Return the transformed row wrapped in a list to match ARC output format List[List[int]]
    return [output_list]
