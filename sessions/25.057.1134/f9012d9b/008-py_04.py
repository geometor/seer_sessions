"""
1. Identify Repeating Pattern: Observe the input grid and note the two colors/numbers that constitute the repeating pattern (in this case, 8 and 6, azure and magenta).
2. Select Dominant Value: Ignore outlier values (like the single 0), and determine the numerically higher value in the repeating pattern.
3. Output: Create a 1x1 grid containing only the selected value, with the corresponding color. In other words find the numerically highest number in the input checkerboard pattern. Output it.
"""

import numpy as np

def find_checkerboard_values(grid):
    # Find the values that form the checkerboard pattern, ignoring singular outliers.
    unique_values = np.unique(grid)
    counts = [np.sum(grid == val) for val in unique_values]
    
    # Consider values part of the checkerboard if their count is close to half the grid size.
    checkerboard_values = [val for val, count in zip(unique_values, counts) if count > (grid.size / 4)] #use one quarter as a good check
    return checkerboard_values
    

def transform(input_grid):
    """
    Transforms an input grid with a checkerboard pattern into a 1x1 grid containing the
    numerically larger value from the checkerboard.
    """
    # Find the values that constitute the repeating checkerboard pattern
    checkerboard_vals = find_checkerboard_values(input_grid)
    
    # Select the largest numerical value from these
    dominant_value = np.max(checkerboard_vals)

    # Create the 1x1 output grid
    output_grid = np.array([[dominant_value]])

    return output_grid