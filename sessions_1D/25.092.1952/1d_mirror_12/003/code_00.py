import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D grid by relocating a contiguous colored block based on its position relative to a fixed pivot pixel (maroon, 9). 

The core logic identifies the single pivot pixel (9) and the single contiguous block of another color (not background 0 or pivot 9). It assumes the block initially lies entirely before the pivot. It calculates the separation distance (number of background pixels) between the end of the block and the pivot in the input. An output grid of the same size is created. The pivot pixel is placed at its original index in the output. The colored block is then placed *after* the pivot pixel in the output, maintaining the same separation distance that existed between the block's end and the pivot in the input. The remaining positions are filled with the background color (0).
"""

def find_pivot(grid: np.ndarray, pivot_color: int = 9) -> Optional[int]:
    """
    Finds the index of the first occurrence of the pivot pixel.

    Args:
        grid: The 1D numpy array representing the grid.
        pivot_color: The integer value of the pivot pixel (default 9).

    Returns:
        The index of the pivot pixel, or None if not found or multiple found.
    """
    pivot_indices = np.where(grid == pivot_color)[0]
    if len(pivot_indices) == 1:
        return pivot_indices[0]
    elif len(pivot_indices) == 0:
        # print("Debug: Pivot pixel not found.") # Optional debug message
        return None
    else:
        # print("Debug: Multiple pivot pixels found.") # Optional debug message
        # Based on examples, assume only one pivot. If multiple, the rule is ambiguous.
        return None


def find_movable_block(grid: np.ndarray, background_color: int = 0, pivot_color: int = 9) -> Optional[Tuple[int, int, int]]:
    """
    Finds the color, start index, and size of the first contiguous non-background, non-pivot block.

    Args:
        grid: The 1D numpy array representing the grid.
        background_color: The integer value of the background (default 0).
        pivot_color: The integer value of the pivot pixel (default 9).

    Returns:
        A tuple containing (block_color, block_start_index, block_size), or None if no such block is found.
    """
    block_color = -1
    block_start_index = -1
    block_size = 0
    in_block = False

    for i, pixel in enumerate(grid):
        is_block_pixel = (pixel != background_color and pixel != pivot_color)

        if is_block_pixel and not in_block:
            # Start of a new block
            block_color = pixel
            block_start_index = i
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

    if block_start_index != -1:
        return block_color, block_start_index, block_size
    else:
        # print("Debug: Movable block not found.") # Optional debug message
        return None


def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the 1D output grid. Returns the input grid
        if essential components (pivot, block) are missing or misplaced according
        to the observed pattern.
    """
    # Convert input list to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    grid_size = len(input_np)
    background_color = 0
    pivot_color = 9

    # Initialize the output grid with the background color
    output_grid = np.full(grid_size, background_color, dtype=int)

    # Find the pivot pixel
    pivot_index = find_pivot(input_np, pivot_color)
    if pivot_index is None:
        # print("Debug: Cannot transform - pivot missing or ambiguous.") # Optional
        return input_grid # Return original if pivot rule not met

    # Place the pivot pixel in the output grid
    output_grid[pivot_index] = pivot_color

    # Find the movable block
    block_info = find_movable_block(input_np, background_color, pivot_color)
    if block_info is None:
        # print("Debug: Cannot transform - block missing.") # Optional
        # Return grid with only pivot if block is missing
        return output_grid.tolist() 

    block_color, input_block_start_index, block_size = block_info

    # Calculate the end index of the block in the input
    input_block_end_index = input_block_start_index + block_size - 1

    # Validate that the block is entirely before the pivot in the input
    if input_block_end_index >= pivot_index:
        # print("Debug: Block is not entirely before pivot in input.") # Optional
        return input_grid # Rule assumption not met, return original

    # Calculate the separation distance (number of background pixels) in the input
    # Distance = pivot_index - (index immediately after block end)
    separation_distance = pivot_index - (input_block_end_index + 1)
    if separation_distance < 0:
         # This case should be covered by the check above, but added for safety
         # print("Debug: Negative separation distance implies overlap or adjacency.") # Optional
         return input_grid # Invalid input state based on examples

    # Calculate the required starting index for the block in the output grid
    # Output start = index immediately after pivot + separation distance
    output_block_start_index = pivot_index + 1 + separation_distance

    # Calculate the end index for the block in the output grid (exclusive)
    output_block_end_index = output_block_start_index + block_size

    # Check if the calculated block position is valid within the grid boundaries
    if output_block_start_index >= grid_size:
        # The block starts outside the grid - cannot place it.
        # print("Debug: Output block start index is outside grid bounds.") # Optional
        # Return grid with only pivot placed, as block cannot be placed according to rule
        return output_grid.tolist() 
        
    # Place the movable block in the output grid
    # Ensure the block doesn't extend beyond the grid end
    actual_end_index = min(output_block_end_index, grid_size)
    output_grid[output_block_start_index:actual_end_index] = block_color
    
    # Convert the numpy array back to a list and return
    return output_grid.tolist()