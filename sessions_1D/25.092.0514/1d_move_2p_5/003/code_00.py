"""
Shifts the single contiguous horizontal block of non-white pixels within a 1D
input grid two positions to the right. The grid size, block color, and block
length remain unchanged. The background is white (0).
"""

import numpy as np

def find_block_1d_np(row_array):
    """
    Finds the first contiguous block of non-zero pixels in a 1D NumPy array.

    Args:
        row_array: A 1D NumPy array representing a row of the grid.

    Returns:
        A tuple containing:
        - color (int): The color of the block (non-zero).
        - start_index (int): The starting index (column) of the block.
        - length (int): The length of the block.
        Returns None if no non-zero block is found.
    """
    # Find indices of non-zero elements
    non_zero_indices = np.where(row_array != 0)[0]

    if len(non_zero_indices) == 0:
        return None  # No non-white block found

    start_index = non_zero_indices[0]
    block_color = row_array[start_index]
    length = 0

    # Iterate from the start index to find the length of the contiguous block
    # of the *same* color. Assumes only one block type based on examples.
    for i in range(start_index, len(row_array)):
        if row_array[i] == block_color:
            length += 1
        else:
            break # Block ended

    # Additional check: Ensure the found non-zero elements form a single contiguous block
    # This might be overly defensive given the problem constraints but good practice.
    if len(non_zero_indices) != length or not np.all(non_zero_indices == np.arange(start_index, start_index + length)):
         # This condition implies either multiple blocks or a block with different colors,
         # which contradicts the observed examples. We proceed assuming the first block found is the target.
         # In a more complex scenario, might need error handling or different logic.
         pass # For this specific problem, assume the first contiguous block is the only one that matters.


    return block_color, start_index, length


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by shifting the non-white block right by two positions.

    Args:
        input_grid: A 1D NumPy array representing the input grid row.

    Returns:
        A 1D NumPy array representing the transformed grid row.
    """
    # Ensure input is 1D (or effectively 1D if passed as 1xN)
    if input_grid.ndim > 1:
        if input_grid.shape[0] == 1:
             input_row = input_grid[0] # Take the first row if shape is (1, N)
        elif input_grid.shape[1] == 1:
             input_row = input_grid[:,0] # Take the first column if shape is (N, 1) - less likely
        else:
             # Handle unexpected dimensions - for this problem, assume 1D or (1,N)
             # Returning original might be safest default if structure is unknown.
             print(f"Warning: Expected 1D input grid, received shape {input_grid.shape}. Returning original.")
             return input_grid
    else:
         input_row = input_grid # Already 1D

    grid_length = len(input_row)

    # Find the non-white block in the input row
    block_info = find_block_1d_np(input_row)

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros(grid_length, dtype=input_row.dtype)

    if block_info is None:
        # If no block is found, return the initialized (all white) grid
        # or potentially the original grid depending on requirements.
        # Given examples, a block is always present.
        print("Warning: No non-white block found in input.")
        return output_grid # Return all-white grid

    block_color, start_index, length = block_info

    # Calculate the new starting position for the block
    new_start_index = start_index + 2

    # Define the slice for the block in the output grid
    # Ensure the slice indices stay within the grid boundaries
    slice_start = max(0, new_start_index)
    slice_end = min(grid_length, new_start_index + length)

    # Place the block (or the part of it that fits) into the output grid
    if slice_start < slice_end: # Check if any part of the block remains on the grid
        # Calculate how much of the block to draw based on boundary clipping
        draw_length = slice_end - slice_start
        # Fill the slice with the block color
        output_grid[slice_start:slice_end] = block_color

    # If the original input was (1,N), reshape the output to match
    if input_grid.ndim > 1 and input_grid.shape[0] == 1:
        output_grid = output_grid.reshape(1, -1)
        
    return output_grid