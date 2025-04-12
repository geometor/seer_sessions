import numpy as np

"""
The transformation involves two main steps:
1. Column Filtering: Identify and remove columns from the input grid that consist entirely of the background color (0).
2. Pixel Mapping with Vertical Shift: Map the pixels from the remaining (non-empty) columns to a new output grid. The relative horizontal order of these columns is preserved. During this mapping, pixels undergo a vertical shift (change in row index). The rule for this shift, based on analysis of Example 1 Column 6, appears to be dependent on the *new* column index (`c_new`) in the output grid. Specifically, a pixel at original position `(r, c)` moves to `(r_new, c_new)` where `c_new` is the mapped column index and `r_new = (r - c_new) % H`, with `H` being the grid height. Pixels are processed column by column, then row by row within the column; if multiple input pixels map to the same output cell, the one from the highest original row index overwrites others.
"""

def find_non_empty_columns(grid: np.ndarray) -> tuple[list[int], dict[int, int]]:
    """
    Identifies non-empty columns (not all background color 0) and creates a mapping.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple containing:
        - A list of indices of non-empty columns in the original grid.
        - A dictionary mapping original non-empty column indices to their new 0-based indices.
    """
    height, width = grid.shape
    background_color = 0
    non_empty_col_indices = []
    col_mapping = {}
    new_col_idx = 0
    # Iterate through each column index
    for c in range(width):
        # Check if all elements in the column are the background color
        is_empty = np.all(grid[:, c] == background_color)
        # If the column is not empty
        if not is_empty:
            # Record the original index
            non_empty_col_indices.append(c)
            # Map original index to the new index
            col_mapping[c] = new_col_idx
            # Increment the new index for the next non-empty column
            new_col_idx += 1
    return non_empty_col_indices, col_mapping

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by removing empty columns and applying a vertical shift
    to the pixels in the remaining columns based on the destination column index.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # Handle empty input grid edge cases
    if input_grid.size == 0:
        return [] # Input was []

    height, width = input_grid.shape
    background_color = 0

    if height == 0: # Input was [[]] or similar
         # Return a structure matching the likely intent for zero height
         return [] if width == 0 else [[] for _ in range(width)] # Match numpy behavior? Or just []? ARC usually implies non-zero dimensions. Let's assume [] is best.
    if width == 0: # Input was [[], [], []]
        # Return a grid of original height but zero width
        return [[] for _ in range(height)]

    # --- Step 1: Identify non-empty columns and create the mapping ---
    non_empty_col_indices, col_mapping = find_non_empty_columns(input_grid)

    # --- Step 2: Determine output grid dimensions ---
    output_height = height
    output_width = len(non_empty_col_indices)

    # Handle case where all columns were empty
    if output_width == 0:
         # Return grid of original height but zero width
         return [[] for _ in range(output_height)]

    # --- Step 3: Create the output grid, initialized with background color ---
    output_grid = np.full((output_height, output_width), background_color, dtype=int)
    H = output_height # Alias for height for the formula

    # --- Step 4: Iterate through NON-EMPTY input columns and place pixels in output grid with shift ---
    # Process column by column to potentially handle overlaps based on column order if needed
    for c in non_empty_col_indices:
        # Get the corresponding new column index for the output grid
        c_new = col_mapping[c]

        # Iterate through rows for this specific non-empty input column
        for r in range(height):
            # Get the pixel color from the input grid
            pixel_color = input_grid[r, c]

            # Only process non-background pixels
            if pixel_color != background_color:
                # Calculate the new row index using the candidate rule: r_new = (r - c_new) % H
                # This rule is derived from analyzing specific examples and might need refinement.
                r_new = (r - c_new) % H

                # Place the pixel color in the output grid at the calculated new position
                # If multiple input pixels map to the same output cell, the one processed
                # later (from a higher original row index 'r' within the same column 'c')
                # will overwrite the value.
                output_grid[r_new, c_new] = pixel_color

    # --- Step 5: Convert the result back to list of lists format and return ---
    return output_grid.tolist()