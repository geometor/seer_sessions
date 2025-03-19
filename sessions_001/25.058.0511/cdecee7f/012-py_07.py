"""
1.  **Selection:** Identify all distinct, contiguous blocks of non-zero (non-white) pixels within the input grid. A block is defined as one or more adjacent pixels of the same color.
2.  **Ordering:** Maintain the input order of the blocks.
3.  **Arrangement:** Create an output grid. The dimensions of the output grid and arrangement of blocks are determined by the shapes and locations of the selected blocks in the input. Each block from the input is placed into the output grid in its entirety. If multiple blocks are present, the output grid encompasses them, maintaining their relative positions and the space between. If blocks form rows or columns, maintain that relationship.
"""

import numpy as np

def find_blocks(grid):
    """
    Identifies contiguous blocks of non-zero pixels in the grid.
    """
    blocks = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, block):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, block)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                block = []
                dfs(r, c, grid[r][c], block)
                blocks.append(block)
    return blocks

def transform(input_grid):
    """
    Transforms the input grid into an output grid based on identified blocks.
    """
    input_grid = np.array(input_grid)
    blocks = find_blocks(input_grid)

    if not blocks:
        return np.zeros((1, 1), dtype=int)  # Handle empty case

    # Determine output grid dimensions
    min_row = min(min(r for r, _ in block) for block in blocks)
    max_row = max(max(r for r, _ in block) for block in blocks)
    min_col = min(min(c for _, c in block) for block in blocks)
    max_col = max(max(c for _, c in block) for block in blocks)

    output_rows = max_row - min_row + 1
    output_cols = max_col - min_col + 1
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Place blocks into the output grid
    for block in blocks:
        for r, c in block:
            output_grid[r - min_row, c - min_col] = input_grid[r, c]
            
    return output_grid