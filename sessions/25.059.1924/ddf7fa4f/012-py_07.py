"""
1.  **Reference Row:** The first row of the input grid serves as a reference. The non-zero values on this row will be used to determine how other cells should be replaced.
2.  **Identify Blocks:** Starting from the second row, identify contiguous blocks of pixels that share the same color. Black (0) is neutral and is ignored, acting as a separator.
3. **Map to Reference by Position** For each identified block below the first row, find the color value in the input grid's first row, in a column that falls within the block's horizontal extent.
4.  **Replace:** Replace all pixels in the identified blocks with the color determined by the positionally corresponding element in the first row. If the first row's value in the relevant column is black (0), *do not change the value* of the block.
"""

import numpy as np

def find_blocks(grid):
    """
    Finds contiguous blocks of the same color in the grid, excluding the top row.
    """
    blocks = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, block):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        dfs(r + 1, c, color, block)
        dfs(r - 1, c, color, block)
        dfs(r, c + 1, color, block)
        dfs(r, c - 1, color, block)

    for r in range(1, rows):  # Start from the second row
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:
                    block = []
                    dfs(r, c, color, block)
                    if block: # Avoid empty blocks
                      blocks.append((color, block))
    return blocks

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Reference Row
    reference_row = input_grid[0]

    # 2. Identify Blocks
    blocks = find_blocks(input_grid)

    # 3. & 4. Map and Replace
    for color, block in blocks:
        # Find a representative column for the block.
        first_coord = block[0]
        
        rep_col = first_coord[1]

        # Get reference color from the first row.
        reference_color = reference_row[rep_col]

        if reference_color != 0:
          # Replace the block's color if the reference color is not black.
          for row, col in block:
              output_grid[row, col] = reference_color

    return output_grid