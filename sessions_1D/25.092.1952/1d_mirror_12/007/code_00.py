import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D grid (represented as a list, interpreted as a single-row 2D grid)
by relocating a contiguous colored block based on its horizontal position 
relative to a fixed pivot pixel (maroon, 9).

The core logic identifies the single pivot pixel (9) and the single 
contiguous block of another color (not background 0 or pivot 9) within the 
single row. It assumes the block initially lies entirely to the left of the 
pivot. It calculates the horizontal separation distance (number of background 
pixels/columns) between the end of the block and the pivot in the input row. 
An output grid of the same shape (1 row, N columns) is created. The pivot pixel 
is placed at its original column index in the output row. The colored block is 
then placed *after* the pivot pixel in the output row, maintaining the same 
separation distance that existed between the block's end and the pivot in the 
input. The remaining positions are filled with the background color (0). 
The final 2D grid is flattened back into a list before returning.
"""

def find_pivot_column(row: np.ndarray, pivot_color: int = 9) -> Optional[int]:
    """
    Finds the column index of the unique pivot pixel within a single row.

    Args:
        row: The 1D numpy array representing the grid row.
        pivot_color: The integer value of the pivot pixel (default 9).

    Returns:
        The column index of the pivot pixel, or None if exactly one is not found.
    """
    pivot_indices = np.where(row == pivot_color)[0]
    if len(pivot_indices) == 1:
        return int(pivot_indices[0]) # Ensure standard int type
    # Return None if zero or more than one pivot is found
    return None


def find_movable_block_in_row(row: np.ndarray, background_color: int = 0, pivot_color: int = 9) -> Optional[Tuple[int, int, int]]:
    """
    Finds the color, start column index, and size (length) of the first contiguous 
    non-background, non-pivot block within a single row.

    Args:
        row: The 1D numpy array representing the grid row.
        background_color: The integer value of the background (default 0).
        pivot_color: The integer value of the pivot pixel (default 9).

    Returns:
        A tuple containing (block_color, block_start_col, block_size), 
        or None if no such block is found. Returns standard int types.
    """
    block_color = -1
    block_start_col = -1
    block_size = 0
    in_block = False

    for i, pixel in enumerate(row):
        is_block_pixel = (pixel != background_color and pixel != pivot_color)

        if is_block_pixel and not in_block:
            # Start of a new block
            block_color = int(pixel) # Ensure standard int
            block_start_col = i
            block_size = 1
            in_block = True
        elif is_block_pixel and in_block:
            # Continue existing block
            if pixel == block_color:
                block_size += 1
            else:
                # Found a different colored block immediately after - stop at the first block.
                break
        elif not is_block_pixel and in_block:
            # End of the current block
            break # Stop searching after the first block ends

    if block_start_col != -1:
        return block_color, block_start_col, block_size
    else:
        # Movable block not found
        return None


def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid list.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid. Returns 
        the original input list under certain error conditions (missing/multiple
        pivots, block not before pivot). Returns a grid with only the pivot if 
        the movable block is missing or cannot be placed in the output.
    """
    # Define constants
    background_color = 0
    pivot_color = 9
    
    # -- Step 1: Reshape Input and Initialize Output --
    try:
        # Convert input list to a 1xN 2D numpy array
        input_np = np.array(input_grid, dtype=int).reshape(1, -1)
        rows, cols = input_np.shape
        if rows != 1:
            # This function assumes a single row structure based on examples
            return input_grid 
    except ValueError: # Handle potential issues with input list format
        return input_grid 

    # Initialize the output grid (1xN) with the background color
    output_grid = np.full((1, cols), background_color, dtype=int)
    
    # Extract the single row for easier processing
    input_row = input_np[0, :]
    output_row = output_grid[0, :] # Get a view to modify output_grid directly

    # -- Step 2: Find Pivot --
    pivot_col = find_pivot_column(input_row, pivot_color)
    if pivot_col is None:
        # If pivot is missing or ambiguous, return the original grid list
        return input_grid 

    # -- Step 3: Place Pivot in Output --
    output_row[pivot_col] = pivot_color

    # -- Step 4: Find Movable Block --
    block_info = find_movable_block_in_row(input_row, background_color, pivot_color)
    if block_info is None:
        # If block is missing, return the grid with only the pivot placed (flattened)
        return output_grid.flatten().tolist() 

    block_color, input_block_start_col, block_size = block_info

    # Calculate the end column index of the block in the input row
    input_block_end_col = input_block_start_col + block_size - 1

    # -- Step 5: Validate Input Block Position --
    # Check if the block is entirely before the pivot
    if input_block_end_col >= pivot_col:
        # Rule assumption (block before pivot) not met, return the original input list
        return input_grid 

    # -- Step 6: Calculate Separation Distance --
    # Distance = number of background cells between block end and pivot start
    separation_distance = pivot_col - (input_block_end_col + 1)
    # separation_distance should logically be >= 0 due to the check in step 5

    # -- Step 7: Calculate Output Block Position --
    # Output start col = column after pivot + separation distance
    output_block_start_col = pivot_col + 1 + separation_distance

    # -- Step 8: Place Block in Output, Handling Boundaries --
    output_block_end_col = output_block_start_col + block_size

    # Check if the block starts outside the grid
    if output_block_start_col >= cols:
        # Cannot place the block at all, return grid with only the pivot (flattened)
        return output_grid.flatten().tolist() 
        
    # Determine the actual end column index considering grid boundaries (exclusive index)
    actual_end_col = min(output_block_end_col, cols)
    
    # Place the (potentially truncated) block in the output row
    output_row[output_block_start_col:actual_end_col] = block_color
    
    # -- Step 9: Return Flattened Output --
    # Convert the final 2D output numpy array back into a flat list
    return output_grid.flatten().tolist()