"""
1.  **Split:** Divide the input grid vertically into two equal halves (left and right).
2.  **Mirror:** Mirror the left half of the input grid horizontally.
3.  **Extract:** Extract the first row from the right half of the input grid.
4.  **Combine:**  Combine the extracted row (from Step 3) with the mirrored left half (from Step 2). The extracted row is placed to the *left* of the mirrored half.
"""

import numpy as np

def split_grid_vertical(grid):
    """Splits the grid into two halves vertically."""
    cols = len(grid[0])
    mid_col = cols // 2
    left_side = [row[:mid_col] for row in grid]
    right_side = [row[mid_col:] for row in grid]
    return left_side, right_side

def mirror_horizontal(grid):
    """Mirrors the grid horizontally."""
    return np.fliplr(grid).tolist()

def get_first_row(grid):
    """Extracts the first row from the grid."""
    return grid[0] if grid else []

def transform(input_grid):
    # Convert input to numpy array
    input_grid_np = np.array(input_grid)

    # Split the input grid vertically
    left_side, right_side = split_grid_vertical(input_grid_np)

    # Mirror the left side horizontally
    mirrored_left = mirror_horizontal(left_side)

    # Extract the first row of the right side
    first_row_right = get_first_row(right_side)
    
    #Concatenate to create the output grid
    if first_row_right:
         output_grid = np.concatenate(([first_row_right], mirrored_left), axis=1)
    else:
        output_grid = np.array(mirrored_left)

    return output_grid.tolist()