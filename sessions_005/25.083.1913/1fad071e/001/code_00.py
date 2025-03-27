"""
1. Identify Connected Regions: In the input grid, identify all distinct, contiguous regions of the color blue (value 1). "Contiguous" means connected horizontally or vertically, but *not* diagonally.
2. Count Regions: Count the number of these distinct blue regions.
3. Construct Output: Create an output array of length 5.
4. Populate Output: Fill the output array. The first *N* elements should be 1 (blue), where *N* is the number of blue regions counted in step 2. The remaining elements of the array are filled with 0 (white).
"""

import numpy as np

def find_connected_regions(grid, color):
    """
    Finds and counts distinct connected regions of a specified color in a grid.
    """
    visited = set()
    count = 0
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(row, col):
        if (row, col) in visited or not is_valid(row, col) or grid[row][col] != color:
            return
        visited.add((row, col))
        # Check up, down, left, right
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == color and (row, col) not in visited:
                dfs(row, col)
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert input_grid to numpy array for easier processing
    input_grid = np.array(input_grid)

    # 1. Identify and Count Connected Regions of blue (1)
    num_blue_regions = find_connected_regions(input_grid, 1)

    # 2. Construct Output array of length 5
    output_array = [0] * 5

    # 3. Populate Output: First N elements are 1, the rest are 0
    for i in range(min(num_blue_regions, 5)):  # Ensure we don't exceed bounds
        output_array[i] = 1

    return output_array