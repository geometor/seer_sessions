"""
Transforms a 1xN input grid by finding a marker pixel (maroon, 9), identifying
the last non-white pixel before it, and then filling all pixels between that
non-white pixel and the marker pixel with the color of the non-white pixel.
Assumes the input grid has exactly one row.
"""

import numpy as np

def transform(input_grid):
    """
    Fills the gap between the end of a colored block and a subsequent marker
    pixel (maroon, 9) with the color of the block.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.
                     Expected to be a 1xN grid.

    Returns:
        A list of lists representing the transformed grid.
    """

    # Handle numpy array input or list of lists
    if isinstance(input_grid, np.ndarray):
        if input_grid.shape[0] != 1:
            # This specific task assumes a 1xN grid based on examples
            # In a more general case, we might iterate through rows or apply
            # different logic. For this task, error out or return unchanged if
            # the shape is not 1xN.
            # Returning unchanged might be safer if test cases vary.
            print(f"Warning: Expected 1xN grid, got {input_grid.shape}. Returning input unchanged.")
            return input_grid.tolist() # Return as list of lists
        grid_row = input_grid[0].tolist()
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        grid_row = input_grid[0]
    else:
        raise ValueError("Input grid must be a 1xN list of lists or numpy array.")

    # Initialize output_grid as a copy of the input row
    output_row = list(grid_row)
    n_cols = len(output_row)

    # --- Find the marker (maroon, 9) ---
    marker_index = -1
    try:
        marker_index = output_row.index(9)
    except ValueError:
        # If no marker is found, the transformation rule cannot be applied.
        # Return the original grid wrapped in a list.
        print("Warning: Marker (9) not found. Returning input unchanged.")
        return [output_row] # Return original row wrapped in list

    # --- Find the end of the colored block before the marker ---
    last_color_index = -1
    fill_color = -1
    # Scan backwards from the position just before the marker
    for i in range(marker_index - 1, -1, -1):
        if output_row[i] != 0: # Found a non-white pixel
            last_color_index = i
            fill_color = output_row[i]
            break # Found the last colored pixel before the marker

    # --- Fill the gap ---
    # Check if a colored block was actually found before the marker
    if last_color_index != -1 and fill_color != -1:
        # Iterate from the position immediately after the colored block
        # up to (but not including) the marker's position
        for i in range(last_color_index + 1, marker_index):
             # Change the pixel in the output row to the fill_color
             output_row[i] = fill_color

    # Return the transformed row, wrapped in a list to represent a 1xN grid
    return [output_row]