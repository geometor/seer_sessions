"""
Transforms a 5x5 input grid based on two main steps:
1. Gravity Simulation: All '4's in the input grid fall downwards within their respective columns until they hit the bottom edge (row 4) or another '4'. Empty spaces ('0') fill the vacated cells.
2. Row Transformation: Based on the count of '4's in the bottom two rows of the *original* input grid, entire rows in the gravity-applied grid are potentially replaced with '5's.
   - If the original input's bottom row (row 4) has 3 or more '4's, the output grid's bottom row becomes all '5's.
   - If the original input's second-to-bottom row (row 3) has 3 or more '4's AND the original input's bottom row (row 4) also has 3 or more '4's, the output grid's second-to-bottom row becomes all '5's.
"""

import numpy as np

def transform(input_grid):
    """
    Applies gravity to '4's and then transforms rows to '5's based on original counts.

    Args:
        input_grid: A list of lists representing the 5x5 input grid.

    Returns:
        A list of lists representing the transformed 5x5 output grid.
    """
    
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    # --- Step 0: Store counts from the original input grid ---
    # Count '4's in the second-to-last row (row index 3) of the original input
    original_row3_fours = np.count_nonzero(grid_np[3, :] == 4)
    # Count '4's in the last row (row index 4) of the original input
    original_row4_fours = np.count_nonzero(grid_np[4, :] == 4)

    # --- Step 1: Apply Gravity ---
    # Create an intermediate grid to store the result of gravity
    intermediate_grid = np.zeros_like(grid_np)

    # Process each column independently
    for j in range(cols):
        # Extract the column
        column = grid_np[:, j]
        # Get the '4's in the current column
        fours_in_col = column[column == 4]
        # Determine the starting row index to place the fallen '4's
        start_row = rows - len(fours_in_col)
        # Place the '4's at the bottom of the column in the intermediate grid
        intermediate_grid[start_row:, j] = fours_in_col
        # The rest of the column defaults to '0' due to np.zeros_like initialization

    # --- Step 2: Apply Row Transformation based on original counts ---
    # Initialize the output grid with the result of the gravity step
    output_grid_np = intermediate_grid.copy()

    # Check condition for the bottom row (row 4)
    if original_row4_fours >= 3:
        output_grid_np[4, :] = 5 # Set the entire row to 5

    # Check condition for the second-to-bottom row (row 3)
    # This requires both row 3 and row 4 conditions to be met in the original grid
    if original_row3_fours >= 3 and original_row4_fours >= 3:
        output_grid_np[3, :] = 5 # Set the entire row to 5

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
