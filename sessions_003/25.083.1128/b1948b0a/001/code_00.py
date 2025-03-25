"""
Transforms a grid by changing magenta (6) pixels to red (2) based on adjacency.
A magenta pixel changes to red unless it's part of a contiguous block of three or more magenta pixels.
Orange (7) pixels remain unchanged.
"""

import numpy as np

def count_adjacent_same_color(grid, row, col, color):
    """Counts adjacent cells with the same color."""
    count = 0
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
                count += 1
    return count

def find_contiguous_blocks(grid, color):
    """Find contiguous blocks of a specified color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    def dfs(row, col, current_block):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_block.append((row, col))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                dfs(row + dr, col + dc, current_block)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                current_block = []
                dfs(row, col, current_block)
                if len(current_block) >=1:
                   blocks.append(current_block)

    return blocks
def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    magenta_blocks = find_contiguous_blocks(input_grid, 6)
    
    for block in magenta_blocks:
       if len(block) < 3:
          for cell in block:
             row, col = cell
             output_grid[row,col] = 2

    return output_grid