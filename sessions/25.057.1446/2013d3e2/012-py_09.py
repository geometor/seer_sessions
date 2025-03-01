"""
1. Scan: Iterate through all possible 3x3 regions within the input grid.
2. Identify blue square candidates: if a region is not a 3x3 blue square, proceed to the next region.
3. Check Border: If all the border pixels of the 3x3 region are blue.
4. Extract: If the conditions in steps 2 is met, extract the entire 3x3 region.
5. Repeat: Continue this process until all 3x3 regions in the input grid have been checked.
6. Output: If there are multiple blue squares, extract them all.
"""

import numpy as np

def is_3x3_blue_bordered(grid, row, col):
    # Check if the 3x3 region is within bounds
    if row + 3 > grid.shape[0] or col + 3 > grid.shape[1]:
        return False

    # Extract the 3x3 region
    region = grid[row:row+3, col:col+3]

    # Check if the border is blue
    for i in range(3):
        if region[0, i] != 1:  # Top border
            return False
        if region[2, i] != 1:  # Bottom border
            return False
        if region[i, 0] != 1:  # Left border
            return False
        if region[i, 2] != 1:  # Right border
            return False
    return True

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    output_grids = []

    # Iterate through all possible 3x3 regions
    for row in range(input_array.shape[0] - 2):
        for col in range(input_array.shape[1] - 2):
            # Check if it's a 3x3 blue bordered square
            if is_3x3_blue_bordered(input_array, row, col):
                output_grids.append(input_array[row:row+3, col:col+3].tolist())

    if len(output_grids) > 0:
      return output_grids
    else:
       return input_grid # No transformation