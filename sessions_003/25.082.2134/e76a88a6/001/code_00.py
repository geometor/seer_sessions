"""
Replace color `5` in any 3x3 gray object with colors that mirrors the top-left 3x3 object.
"""

import numpy as np

def get_top_left_3x3(grid):
    """Extract the 3x3 subgrid from the top-left corner."""
    return grid[:3, :3]

def mirror_3x3(subgrid):
    """Mirror a 3x3 subgrid."""
    return subgrid.T

def find_3x3_gray_blocks(grid):
    """Find the top-left coordinates of all 3x3 gray blocks (all 5s)."""
    gray_blocks = []
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            if np.all(grid[i:i+3, j:j+3] == 5):
                gray_blocks.append((i, j))
    return gray_blocks

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get and mirror the top-left 3x3 block.
    top_left_3x3 = get_top_left_3x3(input_grid)
    mirrored_block = mirror_3x3(top_left_3x3)

    # Find all 3x3 gray blocks.
    gray_blocks = find_3x3_gray_blocks(input_grid)

    # Replace each gray block with the mirrored top-left block.
    for i, j in gray_blocks:
        output_grid[i:i+3, j:j+3] = mirrored_block
        
    return output_grid