"""
1.  **Identify Sub-Objects:** Within the input grid, identify all distinct 3x3 rectangular regions of uniform color, excluding regions of color white (0).
2.  **Copy Regions:** For *each* identified 3x3 region, copy it to the output grid.
3.  **Preserve Location:** The location of each copied 3x3 region in the output grid is identical to its top-left coordinates in the input grid.
4. **Output Size:** The output has the same dimensions as the input grid and is otherwise white.
"""

import numpy as np

def find_uniform_regions(grid: np.ndarray, size: int = 3) -> list:
    """
    Finds all square regions of the specified size in the grid that have a uniform color.
    Returns a list of tuples, where each tuple contains:
        - The top-left coordinate of the region (row, col).
        - The color value of the region.
    """
    regions = []
    for i in range(grid.shape[0] - size + 1):
        for j in range(grid.shape[1] - size + 1):
            subgrid = grid[i:i+size, j:j+size]
            if np.all(subgrid == subgrid[0, 0]):
                regions.append(((i, j), subgrid[0, 0]))
    return regions

def transform(input_grid):
    # Initialize output grid as all white (0).  Make it the same size as input.
    output_grid = np.zeros_like(input_grid)

    # Find uniform 3x3 regions, excluding white (0).
    uniform_regions = find_uniform_regions(input_grid)
    non_white_regions = [region for region in uniform_regions if region[1] != 0]

    # Iterate through all non-white uniform regions and copy them.
    for selected_region in non_white_regions:
        top_left_row, top_left_col = selected_region[0]
        color = selected_region[1]

        # Copy the 3x3 region.
        for i in range(3):
            for j in range(3):
                output_grid[top_left_row + i, top_left_col + j] = color

    return output_grid