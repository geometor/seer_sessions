import numpy as np

"""
Transforms a 1xN grid by identifying a single contiguous horizontal segment of non-white pixels 
and shifting this segment 2 positions to the right. The grid is assumed to contain exactly one 
such segment, and the shift is assumed not to cause the segment to exceed the grid boundaries.
The implementation handles input grids represented as either 1D numpy arrays (shape N,) or 
2D numpy arrays with a single row (shape 1,N).
"""

def find_colored_segment_1d(grid_1d):
    """
    Finds the start index, end index, and color of the first contiguous
    non-background (non-zero) segment in a guaranteed 1D grid.

    Args:
        grid_1d (np.array): A 1D numpy array representing the grid row.

    Returns:
        tuple: (start_index, end_index, color) if found, otherwise (None, None, None).
    """
    # Find indices of all non-background (non-zero) pixels
    non_background_indices = np.where(grid_1d != 0)[0]

    # If no non-background pixels are found, return None for all values
    if len(non_background_indices) == 0:
        return None, None, None

    # Determine the start and end indices of the segment
    # For a single contiguous segment, these are the min and max indices
    start_index = non_background_indices[0]
    end_index = non_background_indices[-1]

    # Get the color of the segment (assuming it's uniform)
    color = grid_1d[start_index]

    return start_index, end_index, color

def transform(input_grid):
    """
    Shifts the single colored horizontal segment in the input grid 2 positions to the right.
    Handles both 1D (N,) and 2D (1,N) input grid shapes.

    Args:
        input_grid (np.array): A numpy array representing the input grid row (shape N, or 1,N).

    Returns:
        np.array: A numpy array representing the transformed grid row, with the same shape as the input.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Store original shape and determine if it's 2D (1,N) or 1D (N,)
    original_shape = input_grid.shape
    is_2d = input_grid.ndim == 2 and input_grid.shape[0] == 1

    # Work with a 1D view for finding the segment
    if is_2d:
        grid_1d = input_grid[0] # Get the first (only) row as a 1D array
    else:
        grid_1d = input_grid # It's already 1D

    # Initialize output_grid with the same shape and type as input, filled with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Find the colored segment in the 1D view
    start_index, end_index, color = find_colored_segment_1d(grid_1d)

    # If a segment is found, calculate its new position and place it in the output grid
    if start_index is not None:
        # Calculate new start and end indices (shift right by 2)
        new_start_index = start_index + 2
        new_end_index = end_index + 2

        # Determine grid width
        grid_width = grid_1d.shape[0]

        # Check if the new end index is within bounds (optional based on task assumption)
        if new_end_index < grid_width:
            # Place the segment with the original color in the new position
            # Use appropriate slicing based on the original input shape
            if is_2d:
                output_grid[0, new_start_index : new_end_index + 1] = color
            else:
                output_grid[new_start_index : new_end_index + 1] = color
        else:
            # This case is assumed not to happen based on examples, but if it could:
            # Option 1: Truncate the segment
            # Option 2: Wrap around (not typical for ARC unless specified)
            # Option 3: Raise an error or handle as per specific rules
            # For now, we just place it, assuming it fits, as per the original code logic derived from examples.
            # If robustness is needed, add explicit boundary handling here.
            # print(f"Warning: Shifted segment end index {new_end_index} potentially exceeds grid width {grid_width}.")
            if is_2d:
                 output_grid[0, new_start_index : new_end_index + 1] = color
            else:
                 output_grid[new_start_index : new_end_index + 1] = color


    return output_grid