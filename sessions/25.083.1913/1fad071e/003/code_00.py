"""
1.  **Identify Connected Regions:** In the input grid, locate all distinct, contiguous regions of the color blue (1). Contiguous regions are connected horizontally or vertically, *not* diagonally.
2.  **Count Regions:** Determine the *number* of distinct blue regions identified in the previous step.
3.  **Construct Output:** Create an output array consisting of 5 elements.
4.  **Populate Output:** Fill the output array as follows: The first *N* elements of the array should be 1 (blue), where *N* corresponds to the count of blue regions found in step 2. If *N* is greater than 5, then *N* = 5. The remaining elements in the array (up to the 5th element) should be 0 (white).
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

    # 3. Populate Output: First N elements are 1, the rest are 0. N is capped at 5.
    for i in range(min(num_blue_regions, 5)):
        output_array[i] = 1

    return output_array