import numpy as np

"""
Identify a contiguous horizontal block of pixels that are not white (0) and not yellow (4).
Identify the position of the single yellow pixel (4).
Shift the main block two positions to the right.
Keep the yellow pixel in its original absolute position.
Fill the remaining cells with the background color (white - 0).
"""

def find_main_block(grid):
    """
    Finds the contiguous horizontal block of a single color (not white or yellow).

    Args:
        grid (np.ndarray): The input grid (assumed 1D for this task).

    Returns:
        tuple: (color, start_index, end_index) or None if not found.
               Indices are inclusive.
    """
    rows, cols = grid.shape
    if rows != 1:
        # This specific solution assumes a 1D grid based on examples
        raise ValueError("Input grid must be 1D (1 row).")

    start_index = -1
    end_index = -1
    block_color = -1

    for c in range(cols):
        pixel = grid[0, c]
        if pixel != 0 and pixel != 4: # Not white, not yellow
            if start_index == -1: # Start of a potential block
                start_index = c
                block_color = pixel
            elif pixel != block_color: # Found a different color, previous block ended
                end_index = c - 1
                return block_color, start_index, end_index
        elif start_index != -1: # End of the block (found white or yellow)
            end_index = c - 1
            return block_color, start_index, end_index

    # Handle case where block goes to the end of the grid
    if start_index != -1:
        end_index = cols - 1
        return block_color, start_index, end_index

    return None # No suitable block found

def find_marker_pixel(grid, marker_color=4):
    """
    Finds the index of the first occurrence of the marker color.

    Args:
        grid (np.ndarray): The input grid (assumed 1D).
        marker_color (int): The color value of the marker pixel (default 4).

    Returns:
        int: The column index of the marker pixel, or -1 if not found.
    """
    rows, cols = grid.shape
    if rows != 1:
        raise ValueError("Input grid must be 1D (1 row).")

    for c in range(cols):
        if grid[0, c] == marker_color:
            return c
    return -1 # Marker not found

def transform(input_grid):
    """
    Shifts the main colored block (non-white, non-yellow) two positions to the right,
    keeping the yellow marker pixel in its original position.

    Args:
        input_grid (np.ndarray): A 1D numpy array representing the input grid.

    Returns:
        np.ndarray: The transformed 1D grid.
    """
    # Ensure input is numpy array
    input_grid_np = np.array(input_grid)

    # Check if input is 1D (or effectively 1D like [[...]])
    if input_grid_np.ndim == 1:
        input_grid_np = input_grid_np.reshape(1, -1) # Convert to 1xN 2D array
    elif input_grid_np.ndim != 2 or input_grid_np.shape[0] != 1:
         raise ValueError("Input grid must be convertible to 1xN shape.")

    rows, cols = input_grid_np.shape

    # Initialize output_grid with background color (white - 0)
    output_grid = np.zeros_like(input_grid_np)

    # Find the main block in the input
    block_info = find_main_block(input_grid_np)
    if block_info is None:
        # If no block, maybe just return the original or empty grid?
        # Based on examples, a block always exists.
        # Let's try just placing the marker if it exists.
        marker_index = find_marker_pixel(input_grid_np)
        if marker_index != -1:
             output_grid[0, marker_index] = 4
        return output_grid # Return grid with just marker or all white

    block_color, start_index, end_index = block_info

    # Find the marker pixel in the input
    marker_index = find_marker_pixel(input_grid_np, marker_color=4)
    if marker_index == -1:
         # If no marker, maybe just shift the block?
         # Based on examples, a marker always exists.
         pass # Continue with shifting the block

    # Calculate the new position for the main block
    new_start_index = start_index + 2
    new_end_index = end_index + 2

    # Place the shifted main block onto the output grid
    # Ensure indices are within bounds
    actual_start = max(0, new_start_index)
    actual_end = min(cols, new_end_index + 1) # +1 because slicing is exclusive at the end

    if actual_start < actual_end: # Check if the block is still visible
        output_grid[0, actual_start:actual_end] = block_color

    # Place the marker pixel at its original position
    if marker_index != -1 and 0 <= marker_index < cols:
        # Check if the marker position is overwritten by the shifted block
        # If so, the marker still takes precedence according to the rule "keeping the yellow pixel fixed".
        output_grid[0, marker_index] = 4

    return output_grid