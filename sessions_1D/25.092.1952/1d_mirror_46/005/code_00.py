import numpy as np
from typing import Tuple, Optional

"""
Transformation Rule:

1.  Accept the input grid, assuming it is a 1xN structure (e.g., a NumPy array with shape (1, N)). Extract the single row as a 1D sequence.
2.  Determine the length (N) of the 1D sequence.
3.  Initialize an output sequence of length N, filled with the background color (white, 0).
4.  Locate the index (`pivot_index`) of the single maroon (9) pixel (the Pivot) in the input sequence. If not found, return the initialized background output sequence formatted as a 1xN grid.
5.  Locate the contiguous block of identical pixels in the input sequence whose color is not background (0) and not pivot (9). Record its color (`block_color`) and length (`block_length`). If not found, place the pivot pixel at `pivot_index` in the output sequence (if pivot was found) and return it formatted as a 1xN grid.
6.  Place the pivot pixel (maroon, 9) into the output sequence at `pivot_index`.
7.  Place the background color (white, 0) into the output sequence at index `pivot_index + 1`, if this index is within the sequence bounds (0 to N-1).
8.  Starting at index `output_block_start = pivot_index + 2`, place the `block_color` into the output sequence for `block_length` positions, ensuring each position index is within the sequence bounds (0 to N-1). Stop if the bounds are exceeded.
9.  Format the final output sequence back into the 1xN grid structure (e.g., a NumPy array of shape (1, N)). Return the result.
"""

# Constants
BACKGROUND_COLOR = 0
PIVOT_COLOR = 9

def find_pivot(input_list: np.ndarray) -> Optional[int]:
    """
    Finds the index of the first occurrence of the pivot color (9) in a 1D NumPy array.
    Returns the index (as a standard Python int) or None if not found.
    """
    indices = np.where(input_list == PIVOT_COLOR)[0]
    # Convert to standard Python int if found, otherwise return None
    return int(indices[0]) if len(indices) > 0 else None

def find_block(input_list: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of identical pixels that are not
    background (0) or pivot (9) color in a 1D NumPy array.
    Returns a tuple (color, start_index, length) as standard Python ints,
    or None if no such block is found.
    """
    block_color = -1
    block_start = -1
    block_length = 0
    in_block = False

    for i, color_val in enumerate(input_list):
        # Cast color to int for comparison
        current_color = int(color_val)
        is_block_candidate = (current_color != BACKGROUND_COLOR and current_color != PIVOT_COLOR)

        if is_block_candidate and not in_block: # Start of a potential block
            in_block = True
            block_color = current_color
            block_start = i
            block_length = 1
        elif is_block_candidate and in_block: # Continuing a block
            if current_color == block_color:
                block_length += 1
            else: # Color changed, this marks the end of the *first* block
                  # Return the properties of the block found so far
                  return int(block_color), int(block_start), int(block_length)
        elif not is_block_candidate and in_block: # End of the block (hit background or pivot)
            # Found the block, return its properties
            return int(block_color), int(block_start), int(block_length)

    # If the block runs to the end of the list
    if in_block:
        return int(block_color), int(block_start), int(block_length)

    # No block found
    return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    # Validate input shape (should be 1xN)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
         # Return an empty grid of roughly expected size or input?
         # Let's return an empty 1x0 grid for invalid input format.
         print(f"Warning: Invalid input shape {input_grid.shape}. Expected (1, N).")
         return np.array([[]], dtype=int)

    # Extract the 1D sequence (the first row)
    input_list = input_grid[0]
    n = len(input_list)

    # Handle empty input list edge case
    if n == 0:
        return np.array([[]], dtype=int)

    # Initialize output_list (as a Python list for easier modification) with background color
    output_list = [BACKGROUND_COLOR] * n

    # Find the pivot pixel
    pivot_index = find_pivot(input_list)

    # Find the colored block
    block_info = find_block(input_list)

    # Handle cases where pivot or block are not found
    if pivot_index is None:
        print("Warning: Pivot not found. Returning background grid.")
        # Convert the background list to the required output format
        return np.array([output_list], dtype=int)

    # Place the pivot pixel first (even if block is not found)
    # Check bounds just in case, though find_pivot ensures it's within input bounds if not None
    if 0 <= pivot_index < n:
        output_list[pivot_index] = PIVOT_COLOR
    else:
        # This case should ideally not happen if pivot_index was found correctly
        print(f"Error: Pivot index {pivot_index} out of bounds for grid length {n}.")
        # Return background grid on unexpected error
        return np.array([[BACKGROUND_COLOR] * n], dtype=int)

    # If block is not found, return the grid with only the pivot placed
    if block_info is None:
        print("Warning: Block not found. Returning grid with only pivot placed.")
        return np.array([output_list], dtype=int)

    # Extract block properties (don't need input block_start)
    block_color, _, block_length = block_info

    # --- Continue constructing the output list ---

    # Place the separator (white pixel) to the right of the pivot
    separator_index = pivot_index + 1
    if separator_index < n: # Check if index is within bounds
        output_list[separator_index] = BACKGROUND_COLOR # Explicitly set, though likely already is
    else:
        # Pivot was at the last index, cannot place separator or block after it.
        print("Warning: Pivot at end of grid, cannot place separator or block.")
        # Return the grid with only the pivot placed (already done above)
        return np.array([output_list], dtype=int)

    # Place the colored block to the right of the separator
    output_block_start = separator_index + 1
    for i in range(block_length):
        current_index = output_block_start + i
        if current_index < n: # Check if index is within bounds
            output_list[current_index] = block_color
        else:
            # Block extends beyond the grid boundary, stop placing pixels
            print(f"Warning: Block placement truncated at index {current_index-1} due to grid boundary.")
            break

    # Convert the final Python list back to a 1xN NumPy array
    output_grid = np.array([output_list], dtype=int)
    return output_grid