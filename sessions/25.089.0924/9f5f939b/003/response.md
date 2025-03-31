```python
import numpy as np

"""
Transforms the input grid by changing specific azure (8) pixels to yellow (4).
An azure pixel at position (r, c) is changed to yellow if and only if it satisfies two conditions:
1.  It lies on the intersection of a vertical "corridor" and a horizontal "corridor" defined by blue (1) pixels. This means there must be at least one blue pixel above it in the same column, one below it in the same column, one to its left in the same row, and one to its right in the same row.
2.  The azure pixel must be exactly halfway between the *closest* blue pixel above and the *closest* blue pixel below it in the same column.
3.  The azure pixel must be exactly halfway between the *closest* blue pixel to its left and the *closest* blue pixel to its right in the same row.
All other pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient slicing and searching
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    
    # Get the dimensions of the grid
    num_rows, num_cols = grid.shape

    # Iterate through each pixel of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Check if the current pixel is azure (8)
            if grid[r, c] == 8:
                # Find indices of blue pixels in the same column
                blue_in_col = np.where(grid[:, c] == 1)[0]
                # Find indices of blue pixels in the same row
                blue_in_row = np.where(grid[r, :] == 1)[0]

                # Separate indices based on relative position to the current pixel (r, c)
                blues_above = blue_in_col[blue_in_col < r]
                blues_below = blue_in_col[blue_in_col > r]
                blues_left = blue_in_row[blue_in_row < c]
                blues_right = blue_in_row[blue_in_row > c]

                # Check Condition 1: Existence of blue pixels in all four directions
                if blues_above.size > 0 and blues_below.size > 0 and blues_left.size > 0 and blues_right.size > 0:
                    # Find the closest blue pixels in each direction
                    r_above_closest = np.max(blues_above)
                    r_below_closest = np.min(blues_below)
                    c_left_closest = np.max(blues_left)
                    c_right_closest = np.min(blues_right)

                    # Calculate distances to the closest blue pixels
                    dist_up = r - r_above_closest
                    dist_down = r_below_closest - r
                    dist_left = c - c_left_closest
                    dist_right = c_right_closest - c
                    
                    # Check Conditions 2 & 3: Midpoint conditions
                    if dist_up == dist_down and dist_left == dist_right:
                        # If all conditions are met, change the pixel to yellow (4)
                        output_grid[r, c] = 4

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```