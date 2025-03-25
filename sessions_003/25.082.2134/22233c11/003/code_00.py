"""
The function identifies all contiguous blocks of green (3) pixels within the input grid.
For each green block, it calculates the mirrored positions of that block across both
the main diagonal (y=x) and the anti-diagonal (y = -x + rows - 1). It then places
azure (8) pixels at these mirrored positions in the output grid *only* if the
original cell was white (0). Green pixels remain unchanged.
"""

import numpy as np

def find_blocks(grid, color):
    """Finds contiguous blocks of a given color in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    def dfs(r, c, current_block):
        """Depth-first search to find contiguous cells."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_block.append((r, c))
        dfs(r + 1, c, current_block)
        dfs(r - 1, c, current_block)
        dfs(r, c + 1, current_block)
        dfs(r, c - 1, current_block)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_block = []
                dfs(r, c, current_block)
                blocks.append(current_block)
    return blocks

def mirror_block(block, rows, cols, diagonal_type):
    """Mirrors a block across the specified diagonal."""
    mirrored_block = []
    for r, c in block:
        if diagonal_type == 'main':
            mirrored_block.append((c, r))
        elif diagonal_type == 'anti':
            mirrored_block.append((cols - 1 - c, rows - 1 - r))
    return mirrored_block

def transform(input_grid):
    """
    Transforms the input grid by finding green blocks, mirroring them
    diagonally, and placing azure pixels at mirrored positions if originally white.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # 1. Identify Green Blocks
    green_blocks = find_blocks(input_grid, 3)

    # 2. Mirror and Place Azure Pixels
    for block in green_blocks:
        # Mirror across the main diagonal
        mirrored_block_main = mirror_block(block, rows, cols, 'main')
        for r, c in mirrored_block_main:
            if 0 <= r < rows and 0 <= c < cols and output_grid[r, c] == 0:
                output_grid[r, c] = 8

        # Mirror across the anti-diagonal
        mirrored_block_anti = mirror_block(block, rows, cols, 'anti')
        for r, c in mirrored_block_anti:
            if 0 <= r < rows and 0 <= c < cols and output_grid[r, c] == 0:
                output_grid[r, c] = 8
    # 3. Keep green unchanged (already handled by copying the input at start)

    return output_grid