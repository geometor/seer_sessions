"""
1. Identify 4x4 Subgrids: Examine the input grid and identify all possible 4x4 subgrids.
2. Filter by Color: From the identified 4x4 subgrids, select the subgrid composed entirely of either yellow, blue, or white pixels.
3. Prioritize finding a grid: If multiple such grids exist, it is not clear what rule to apply - the problem description implies there should be only one.
4. Output: The output is the selected 4x4 subgrid.
"""

import numpy as np

def find_all_4x4_subgrids(grid):
    # Find all 4x4 subgrids in the given grid.
    height, width = grid.shape
    subgrids = []
    for r in range(height - 3):
        for c in range(width - 3):
            subgrids.append(grid[r:r+4, c:c+4])
    return subgrids

def is_subgrid_valid(subgrid):
    # Check if a subgrid is composed entirely of yellow, blue, or white pixels.
    unique_colors = np.unique(subgrid)
    return all(color in [0, 1, 4] for color in unique_colors)

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find all 4x4 subgrids
    subgrids = find_all_4x4_subgrids(input_grid)

    # Filter subgrids based on color validity
    valid_subgrids = [subgrid for subgrid in subgrids if is_subgrid_valid(subgrid)]

    # Select the first valid subgrid (if any)
    if valid_subgrids:
        # return the entire matching subgrid
        # find coordinates
        for r in range(input_grid.shape[0] - 3):
            for c in range(input_grid.shape[1] - 3):
                if np.array_equal(input_grid[r:r+4, c:c+4],valid_subgrids[0]):
                    output_grid = input_grid[r:r+4, c:c+4]
                    return output_grid.tolist()
    
    return None # Return None if no valid subgrid is found