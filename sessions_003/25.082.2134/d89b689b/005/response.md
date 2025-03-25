```python
"""
1.  **Find Azure Blocks:** Identify all 2x2 blocks within the input grid where all four pixels are azure (color 8). Record the top-left coordinates of each such block.
2.  **Mask Outside Blocks:** For every pixel in the grid *not* located inside a 2x2 azure block, change the value of any pixels of value 1, 2, 3, 4, 5, 6, 7 or 9, to 0 (black).
3.  **Gather Replacement Colors:** Create a sorted (ascending order) list of unique colors, excluding 0 (black) and 8 (azure), that appear in the *input* grid *outside* of any identified 2x2 azure blocks.
4.  **Replace Colors:** For each 2x2 azure block:
    *   Iterate through the sorted list of replacement colors.
    *   Starting with the top-left pixel of the azure block and proceeding clockwise (top-left, top-right, bottom-right, bottom-left), replace the azure pixel with the next color from the sorted replacement color list.
    * If the end of the color list has been reached, use 0 as the replacement color.
    * If the color list is empty, the cells should all have color 0 (black).
"""

import numpy as np

def find_azure_blocks(grid):
    """Finds the top-left coordinates of all 2x2 azure blocks."""
    height, width = grid.shape
    azure_blocks = []
    for i in range(height - 1):
        for j in range(width - 1):
            if (grid[i:i+2, j:j+2] == 8).all():
                azure_blocks.append((i, j))
    return azure_blocks

def get_replacement_colors(input_grid, azure_blocks):
    """Gets the sorted unique colors outside of azure blocks."""
    height, width = input_grid.shape
    colors = set()
    for i in range(height):
        for j in range(width):
            is_inside_block = False
            for block_i, block_j in azure_blocks:
                if block_i <= i < block_i + 2 and block_j <= j < block_j + 2:
                    is_inside_block = True
                    break
            if not is_inside_block and input_grid[i, j] not in [0, 8]:
                colors.add(input_grid[i, j])
    return sorted(list(colors))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find 2x2 azure blocks
    azure_blocks = find_azure_blocks(input_grid)

    # Mask Outside Blocks
    for i in range(height):
        for j in range(width):
            is_inside_block = False
            for block_i, block_j in azure_blocks:
                if block_i <= i < block_i + 2 and block_j <= j < block_j + 2:
                    is_inside_block = True
                    break
            if not is_inside_block and output_grid[i, j] in [1, 2, 3, 4, 5, 6, 7, 9]:
                output_grid[i, j] = 0

    # Gather Replacement Colors
    replacement_colors = get_replacement_colors(input_grid, azure_blocks)

    # Replace Colors in blocks
    for block_i, block_j in azure_blocks:
        num_colors = len(replacement_colors)
        output_grid[block_i,     block_j]     = replacement_colors[0 % num_colors] if num_colors > 0 else 0
        output_grid[block_i,     block_j + 1] = replacement_colors[1 % num_colors] if num_colors > 0 else 0
        output_grid[block_i + 1, block_j + 1] = replacement_colors[2 % num_colors] if num_colors > 0 else 0
        output_grid[block_i + 1, block_j]     = replacement_colors[3 % num_colors] if num_colors > 0 else 0

    return output_grid
```