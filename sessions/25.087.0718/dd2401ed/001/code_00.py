import numpy as np
from typing import List

"""
Transformation Rule Description:

1.  Identify the vertical gray line (color 5) in the input grid and determine its column index (`Col_in`).
2.  Count the total number of blue pixels (color 1) present in the input grid (`N_blue`).
3.  Calculate the horizontal shift amount (`S`) for the gray line based on `N_blue`:
    *   If `N_blue` is even, `S = N_blue + 2`.
    *   If `N_blue` is odd and equal to 3, `S = N_blue + 2`.
    *   If `N_blue` is odd and not equal to 3, `S = N_blue + 1`.
4.  Determine the target column index (`Col_out`) for the gray line in the output grid: `Col_out = Col_in + S`.
5.  Construct the output grid:
    *   Initialize an output grid of the same dimensions as the input, filled with the background color (0).
    *   Copy non-gray, non-background pixels from the input to the output grid, applying a color transformation rule:
        *   If an input pixel is blue (1), copy it as blue (1) to the output grid at the same location.
        *   If an input pixel is red (2):
            *   If its column index `c` is less than the calculated target column index `Col_out`, change its color to blue (1) in the output grid.
            *   If its column index `c` is greater than or equal to `Col_out`, copy it as red (2) to the output grid.
    *   Finally, draw the vertical gray line (color 5) in the output grid at column `Col_out`, overwriting any pixels previously placed in that column.
"""

def find_gray_line_col(grid: np.ndarray) -> int:
    """Finds the column index of the first occurrence of the gray color (5)."""
    # Check columns for the gray color 5
    # Assuming the gray line is solid and vertical, finding the first instance is sufficient
    rows, cols = grid.shape
    for c in range(cols):
        if grid[0, c] == 5:  # Check the first row for efficiency
             # Verify it's a line (optional, but good practice)
             is_line = True
             for r in range(rows):
                 if grid[r, c] != 5:
                     is_line = False
                     break
             if is_line:
                 return c
    # Fallback if not found in first row or not a full line starting from row 0
    # (Could happen if line starts lower, though not seen in examples)
    gray_cols = np.where(grid == 5)[1]
    if len(gray_cols) > 0:
        return gray_cols[0] # Return the first column index where 5 appears
    raise ValueError("Gray line (color 5) not found in the input grid.")

def count_color(grid: np.ndarray, color: int) -> int:
    """Counts the number of pixels of a specific color in the grid."""
    return np.count_nonzero(grid == color)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Shifts the gray line based on the blue pixel count and modifies red pixel colors
    based on their position relative to the new gray line column.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify the initial gray line column
    try:
        col_in = find_gray_line_col(input_np)
    except ValueError as e:
        print(f"Error processing grid: {e}")
        # Return a copy of input or empty grid if gray line is essential and missing
        return input_grid # Or handle error appropriately

    # 2. Count blue pixels
    n_blue = count_color(input_np, 1)

    # 3. Calculate the shift amount
    if n_blue % 2 == 0: # Even
        shift = n_blue + 2
    else: # Odd
        if n_blue == 3:
            shift = n_blue + 2
        else:
            shift = n_blue + 1

    # 4. Determine the target column for the gray line
    col_out = col_in + shift

    # Check if col_out is within bounds (although examples suggest it stays within)
    if col_out >= width:
        # This case is not explicitly handled by examples.
        # Based on ARC constraints, output dim == input dim.
        # We might need to adjust logic, but for now assume it fits.
        # Or perhaps the line wraps or stops at the edge?
        # Let's assume it gets drawn at the calculated index, potentially
        # overwriting things. If col_out >= width, numpy indexing might error
        # or behave unexpectedly depending on how it's used later.
        # Let's proceed assuming col_out < width based on observed examples.
        # If tests fail, this is a place to revisit.
        pass # Keep col_out as calculated

    # 5. Construct the output grid
    # Initialize with background color (0)
    output_np = np.zeros_like(input_np)

    # Iterate through input grid to place transformed pixels
    for r in range(height):
        for c in range(width):
            input_color = input_np[r, c]

            if input_color == 1: # Blue pixel
                # Copy blue pixel to output
                output_np[r, c] = 1
            elif input_color == 2: # Red pixel
                # Transform red based on its column relative to col_out
                if c < col_out:
                    output_np[r, c] = 1 # Change to blue
                else:
                    output_np[r, c] = 2 # Keep red
            # Ignore background (0) and original gray line pixels (5) for now

    # Draw the shifted gray line in the output grid, overwriting anything in that column
    if 0 <= col_out < width: # Ensure column index is valid before drawing
        output_np[:, col_out] = 5
    else:
        # Handle case where col_out is out of bounds if necessary
        # For now, we assume it won't happen based on examples
        print(f"Warning: Calculated output column {col_out} is outside grid width {width}.")


    # Convert numpy array back to list of lists for the required output format
    output_grid = output_np.tolist()

    return output_grid