"""
1.  **Identify Contiguous Blocks:** Find contiguous blocks of non-azure pixels. A contiguous block is a group of one or more pixels of the same color that are directly adjacent (up, down, left, or right, but *not* diagonally).
2.  **Check for Azure Adjacency:** For each contiguous block, check if *any* of its pixels are adjacent to an azure (8) pixel. The direction towards that adjacent azure defines the "shift direction" for that block. If a block borders azure in more than one direction, pick an arbitrary direction.
3.  **Shift the Block:** Shift the entire contiguous block one step in the shift direction.
4.  **Fill with Azure:** The original positions of the shifted pixels are replaced with azure (8) pixels.
5.  **Iterate**: repeat steps 1-4 on the changed grid. Continue iterating and shifting until no more contiguous blocks can be shifted (i.e. no blocks are directly adjacent to any azure pixels).
6. **Color Invariance:** The only colors in the final output should have been those present in the initial grid.
"""

import numpy as np

def find_contiguous_blocks(grid):
    """Finds all contiguous blocks of non-azure pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, block):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        block.append((r, c))
        dfs(r + 1, c, color, block)
        dfs(r - 1, c, color, block)
        dfs(r, c + 1, color, block)
        dfs(r, c - 1, color, block)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 8:
                block = []
                dfs(r, c, grid[r, c], block)
                blocks.append(block)
    return blocks

def get_shift_direction(grid, block):
    """Determines the shift direction for a block."""
    rows, cols = grid.shape
    for r, c in block:
        if r > 0 and grid[r - 1, c] == 8:
            return "up"
        if r < rows - 1 and grid[r + 1, c] == 8:
            return "down"
        if c > 0 and grid[r, c - 1] == 8:
            return "left"
        if c < cols - 1 and grid[r, c + 1] == 8:
            return "right"
    return None

def shift_block(grid, block, direction):
    """Shifts a block one step in the given direction."""
    new_grid = np.copy(grid)
    if direction == "up":
        for r, c in block:
            new_grid[r - 1, c] = grid[r, c]
            new_grid[r,c] = 8
    elif direction == "down":
        for r, c in block:
            new_grid[r + 1, c] = grid[r, c]
            new_grid[r,c] = 8

    elif direction == "left":
        for r, c in block:
            new_grid[r, c - 1] = grid[r, c]
            new_grid[r,c] = 8

    elif direction == "right":
        for r, c in block:
            new_grid[r, c + 1] = grid[r, c]
            new_grid[r,c] = 8
    return new_grid


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Iterate until no more shifts are possible
    while True:
        # Find contiguous blocks
        blocks = find_contiguous_blocks(output_grid)

        # Check for shifts and perform them
        shifted = False
        for block in blocks:
            direction = get_shift_direction(output_grid, block)
            if direction:
                output_grid = shift_block(output_grid, block, direction)
                shifted = True
        if not shifted:
             break

    return output_grid