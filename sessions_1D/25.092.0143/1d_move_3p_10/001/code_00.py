import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

"""
Identifies a single contiguous block of non-white pixels in a 1D input row. 
Shifts this block 3 positions to the right, maintaining its color and length, 
and places it within a white background of the same total length.
"""

def find_colored_block(grid_1d):
    """
    Finds the first contiguous block of non-white pixels in a 1D grid.

    Args:
        grid_1d (np.array): A 1D numpy array representing the row.

    Returns:
        tuple: (start_index, length, color) or (None, 0, 0) if no block found.
    """
    start_index = -1
    length = 0
    color = 0
    in_block = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and not in_block:
            # Start of a new block
            start_index = i
            color = pixel
            length = 1
            in_block = True
        elif pixel == color and in_block:
            # Continue the block
            length += 1
        elif pixel != color and in_block:
            # End of the block
            break # Since we only expect one block

    if start_index == -1:
        # No block found
        return None, 0, 0
    else:
        return start_index, length, color

def transform(input_grid):
    """
    Shifts the single non-white block in a 1D grid 3 positions to the right.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed row.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        # Assuming input might be a list of lists for consistency with ARC tasks,
        # but this task only uses 1D arrays. Handle potential nesting.
        if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
             grid_1d = np.array(input_grid[0], dtype=int)
        elif isinstance(input_grid, list):
             grid_1d = np.array(input_grid, dtype=int)
        else:
             # Attempt conversion, might fail for unexpected formats
             grid_1d = np.array(input_grid, dtype=int).flatten()
    else:
        # Flatten if it's a 2D array with one row
        grid_1d = input_grid.flatten()


    logging.info(f"Input grid (1D): {grid_1d}")

    # Find the colored block in the input grid
    start_index, length, color = find_colored_block(grid_1d)
    logging.info(f"Found block: start={start_index}, length={length}, color={color}")

    # Initialize the output grid with the background color (white = 0)
    output_grid = np.zeros_like(grid_1d)
    logging.info(f"Initialized output grid: {output_grid}")


    if start_index is not None:
        # Calculate the new starting position
        new_start_index = start_index + 3
        logging.info(f"Calculated new start index: {new_start_index}")

        # Determine the end index for slicing (exclusive)
        new_end_index = new_start_index + length

        # Ensure the block stays within the grid boundaries
        # This check might be redundant if the problem guarantees space, but good practice.
        if new_start_index < len(grid_1d):
             # Calculate the actual length that fits in the output grid
             actual_length = min(length, len(grid_1d) - new_start_index)
             actual_end_index = new_start_index + actual_length

             # Place the colored block in the output grid
             output_grid[new_start_index:actual_end_index] = color
             logging.info(f"Placed block in output: indices {new_start_index} to {actual_end_index-1}")

    logging.info(f"Final output grid: {output_grid}")
    # Return the output grid (potentially nested in a list like input format if needed)
    # For consistency with potential ARC runner expectations, return as list of lists
    return output_grid.tolist() # Return as standard list
