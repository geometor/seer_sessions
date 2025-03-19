"""
1.  **Identify Yellow Regions:** Locate all distinct regions of yellow (4) pixels in the input grid. A region is defined as a contiguous block of yellow pixels.
2. **Count Yellow Regions:**
    * If the number of distinct yellow regions is greater than 1, the output will be a 0x0 empty grid.
    * If there is only one yellow region in the input, extract the minimum bounding box containing all the yellow pixels.
3.  **Return:** The extracted sub-grid or empty grid, as appropriate.
"""

import numpy as np

def find_regions(grid, color):
    """Finds distinct regions of the specified color in the grid."""
    visited = set()
    regions = []

    def is_valid(row, col):
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

    def dfs(row, col, current_region):
        if (row, col) in visited or not is_valid(row, col) or grid[row][col] != color:
            return
        visited.add((row, col))
        current_region.append((row, col))

        # Check adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == color and (row, col) not in visited:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def bounding_box(region):
    """Calculates the bounding box of a region."""
    if not region:
        return 0, 0, 0, 0
    min_row = min(cell[0] for cell in region)
    max_row = max(cell[0] for cell in region)
    min_col = min(cell[1] for cell in region)
    max_col = max(cell[1] for cell in region)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Find distinct yellow regions
    yellow_regions = find_regions(input_array, 4)

    # Determine output based on the number of yellow regions
    if len(yellow_regions) > 1:
        output_array = np.zeros((0, 0), dtype=int)
    elif len(yellow_regions) == 1:
        min_row, max_row, min_col, max_col = bounding_box(yellow_regions[0])
        output_array = input_array[min_row:max_row + 1, min_col:max_col + 1]
    else: # Handle case of no yellow pixels (same as previous version)
        output_array = np.zeros((0,0), dtype=int)

    return output_array.tolist()