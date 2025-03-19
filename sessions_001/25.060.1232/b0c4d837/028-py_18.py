"""
1.  **Identify the Core:** Find the contiguous block of azure (8) colored pixels within the input grid.
2.  **Extract:** Isolate the minimum bounding rectangle that fully encloses the azure core.
3. **Translate**: Take the value in the upper left corner of the identified rectangle.
4. **Resize:** create a 3x3 grid filled with value '0'.
5. **place**: place the value from step 3, into the upper left corner of the new grid.
"""

import numpy as np

def find_contiguous_blocks(grid, color):
    """Finds contiguous blocks of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col, current_block):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_block.append((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                current_block = []
                dfs(row, col, current_block)
                blocks.append(current_block)
    return blocks

def bounding_rectangle(block):
    """Calculates the minimum bounding rectangle for a block of pixels."""
    min_row = min(pixel[0] for pixel in block)
    max_row = max(pixel[0] for pixel in block)
    min_col = min(pixel[1] for pixel in block)
    max_col = max(pixel[1] for pixel in block)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find contiguous blocks of azure (8) pixels.
    azure_blocks = find_contiguous_blocks(input_grid, 8)

    # Find the bounding rectangle for the azure core.
    #   - we will assume that there will only ever be one block
    if azure_blocks:  # Ensure there's at least one azure block
      top_left, bottom_right = bounding_rectangle(azure_blocks[0])
      #get value
      value = input_grid[top_left[0],top_left[1]]
      #set value in output_grid
      output_grid[0,0] = value
    
    return output_grid