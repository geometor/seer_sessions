```python
import numpy as np

"""
Identify the vertical gray (5) separator lines in the input grid. These lines
divide the grid into three sections: Left, Middle, and Right. 
The Left section of the output is a direct copy of the Left section of the input.
The Middle section of the output is the Left section of the input rotated 90 
degrees clockwise.
The Right section of the output is the Left section of the input rotated 180 
degrees.
The gray separator lines are preserved in the output.
"""

def transform(input_grid):
    """
    Transforms the input grid based on rotations of the left-most section.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Find the column indices of the gray (5) separators.
    # Assume separators span the full height and are consistent.
    # We check the first row for efficiency.
    separator_cols = [c for c in range(width) if grid_np[0, c] == 5]

    # Expecting exactly two separators based on the examples
    if len(separator_cols) != 2:
        # If the structure deviates, the logic might not apply.
        # Returning the input might be a safe fallback, or raise an error.
        # For this task, based on examples, we assume two separators.
        raise ValueError("Input grid does not contain exactly two gray separator columns.")

    sep1_col, sep2_col = separator_cols

    # Extract the Left subgrid (columns 0 to sep1_col)
    # The width of this subgrid determines the dimensions for rotation.
    left_subgrid = grid_np[:, 0:sep1_col]

    # Initialize the output grid as a copy of the input grid.
    # This ensures the Left section and the separators are already correctly placed.
    output_grid = np.copy(grid_np)

    # --- Perform Rotations ---
    # Rotate the Left subgrid 90 degrees clockwise (k=-1)
    rotated_90 = np.rot90(left_subgrid, k=-1)

    # Rotate the Left subgrid 180 degrees (k=-2)
    rotated_180 = np.rot90(left_subgrid, k=-2)

    # --- Place Rotated Subgrids into Output ---
    # Define column ranges for the Middle and Right sections
    middle_start_col = sep1_col + 1
    middle_end_col = sep2_col
    right_start_col = sep2_col + 1
    right_end_col = width # Goes to the end of the grid

    # Get the target slices in the output grid
    middle_slice = output_grid[:, middle_start_col:middle_end_col]
    right_slice = output_grid[:, right_start_col:right_end_col]

    # Check if the dimensions match before placing the rotated grids.
    # This is crucial if the sections aren't guaranteed to be square
    # or equal in size. Based on examples, they are 3x3.
    if middle_slice.shape == rotated_90.shape:
        output_grid[:, middle_start_col:middle_end_col] = rotated_90
    else:
        # Handle potential dimension mismatch (e.g., log warning, error, pad, crop)
        # For now, raise error if shapes don't match the expectation from examples
        raise ValueError(f"Dimension mismatch: Cannot place 90-rotated shape {rotated_90.shape} into middle section shape {middle_slice.shape}")


    if right_slice.shape == rotated_180.shape:
        output_grid[:, right_start_col:right_end_col] = rotated_180
    else:
        # Handle potential dimension mismatch
        raise ValueError(f"Dimension mismatch: Cannot place 180-rotated shape {rotated_180.shape} into right section shape {right_slice.shape}")


    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()

```