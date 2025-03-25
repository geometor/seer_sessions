"""
1.  **Identify 2x2 Azure Blocks:** Locate all 2x2 blocks where all pixels are azure (color 8).
2.  **Outside Azure Blocks:** For all pixels *not* within a 2x2 azure block, transform colors 1, 2, 3, 4, 5, 6, 7, and 9 to 0 (black).
3. **Inside Azure Block Transformation**: For all 2x2 azure blocks perform these operations:
    - Get a unique, sorted list of other colors from input that are in the corresponding output. The sorting must be clockwise and begin in the top-left.
    - Replace each of the four azure pixels with the colors from the ordered other color list.
    - If there are fewer unique colors than 4, then stop after placing the colors found.
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

def get_cyclic_colors(input_grid, output_grid, block_i, block_j):
    """Gets the clockwise cyclic colors for an azure block."""
    height, width = input_grid.shape
    colors = []
    
    for i in range(height):
      for j in range(width):
        if not(block_i <= i < block_i+2 and block_j <= j < block_j + 2):
          if output_grid[i,j] != 0:
            colors.append(output_grid[i,j])

    unique_colors = sorted(list(set(colors)))

    return unique_colors


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find 2x2 azure blocks
    azure_blocks = find_azure_blocks(input_grid)
    azure_block_set = set(azure_blocks)

    # Outside azure blocks: transform to 0
    for i in range(height):
        for j in range(width):
            is_inside_block = False
            for block_i, block_j in azure_block_set:
                if block_i <= i < block_i + 2 and block_j <= j < block_j + 2:
                    is_inside_block = True
                    break
            if not is_inside_block:
                if output_grid[i, j] in [1, 2, 3, 4, 5, 6, 7, 9]:
                    output_grid[i, j] = 0

    # Inside azure blocks: cyclic transformation
    for block_i, block_j in azure_blocks:
        # output is used, not the input
        cyclic_colors = get_cyclic_colors(input_grid, output_grid, block_i, block_j)
        
        # Apply cyclic replacement within the block
        num_colors = len(cyclic_colors)

        output_grid[block_i,     block_j]     = cyclic_colors[0 % num_colors] if num_colors > 0 else 0
        output_grid[block_i,     block_j + 1] = cyclic_colors[1 % num_colors] if num_colors > 1 else 0
        output_grid[block_i + 1, block_j + 1] = cyclic_colors[2 % num_colors] if num_colors > 2 else 0
        output_grid[block_i + 1, block_j]     = cyclic_colors[3 % num_colors] if num_colors > 3 else 0
    return output_grid