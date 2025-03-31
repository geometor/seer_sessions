"""
Perform a color swap transformation on an input grid based on rules defined by the top-left 2x2 area.

1. Identify the four colors in the top-left 2x2 area of the input grid:
   - ColorA = color at (row=0, col=0)
   - ColorB = color at (row=0, col=1)
   - ColorC = color at (row=1, col=0)
   - ColorD = color at (row=1, col=1)
2. Create a color swap mapping: ColorA maps to ColorB, ColorB maps to ColorA, ColorC maps to ColorD, and ColorD maps to ColorC.
3. Initialize the output grid as a copy of the input grid.
4. Iterate through each cell (r, c) of the grid.
5. If the cell is outside the top-left 2x2 area (i.e., r >= 2 or c >= 2):
   - Get the CurrentColor of the cell (r, c) from the input grid.
   - If CurrentColor exists as a key in the swap mapping, update the corresponding cell (r, c) in the output grid with its mapped value.
6. Cells within the top-left 2x2 area remain unchanged (as they were copied initially).
7. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a color swap transformation based on the top-left 2x2 control area.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Check if grid is large enough for the control area
    if height < 2 or width < 2:
        # If too small, no transformation possible, return copy
        return output_grid

    # Extract the four colors from the top-left 2x2 control area
    color_a = input_np[0, 0]
    color_b = input_np[0, 1]
    color_c = input_np[1, 0]
    color_d = input_np[1, 1]

    # Define the color swap mapping
    swap_map = {
        color_a: color_b,
        color_b: color_a,
        color_c: color_d,
        color_d: color_c,
    }

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the cell is outside the top-left 2x2 control area
            if r >= 2 or c >= 2:
                current_color = input_np[r, c]
                # If the current color is part of a swap pair, apply the swap
                if current_color in swap_map:
                    output_grid[r, c] = swap_map[current_color]
            # Else (if inside the 2x2 area), do nothing, keep the original color from the copy

    return output_grid
