```python
"""
1.  **Identify Green Blocks:** Find all contiguous blocks of green (3) pixels within the input grid.
2.  **Mirror Each Block:** For each identified green block:
    *   Mirror the block across the main diagonal (y=x). If the mirrored location in the original grid was white (0), place an azure (8) pixel at that location in the output grid.
    *   Mirror the block across the anti-diagonal (y = -x + rows - 1, where 'rows' is the number of rows in the grid). If the mirrored location in the original grid was white (0), place an azure (8) pixel at that location in the output grid.
3. **Preserve Originals** Ensure that the location of green cells are kept intact.
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
    Transforms the input grid based on the defined rules.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy to preserve originals

    # 1. Identify Green Blocks
    green_blocks = find_blocks(input_grid, 3)

    # 2. Mirror and Place Azure Pixels
    for block in green_blocks:
        # Main diagonal mirror
        main_mirrored = mirror_block(block, rows, cols, 'main')
        for r, c in main_mirrored:
            if 0 <= r < rows and 0 <= c < cols and input_grid[r, c] == 0:  # Check original grid
                output_grid[r, c] = 8

        # Anti-diagonal mirror
        anti_mirrored = mirror_block(block, rows, cols, 'anti')
        for r, c in anti_mirrored:
            if 0 <= r < rows and 0 <= c < cols and input_grid[r, c] == 0:  # Check original grid
                output_grid[r, c] = 8

    return output_grid
```
