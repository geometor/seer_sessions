"""
Transforms an input grid by expanding 2x2 colored blocks (blue=1, red=2) into diagonal lines. Blue lines expand up-left from the top-left corner of the blue block and down-right from the bottom-right corner. Red lines expand down-right from the bottom-right corner of the red block and up-left from the top-left. Blue takes precedence, overwriting red. Red lines stop at non-black cells.
"""

import numpy as np

def find_blocks(grid):
    """Finds 2x2 blocks of colors 1 and 2 in the grid."""
    blocks = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if grid[r, c] == grid[r+1, c] == grid[r, c+1] == grid[r+1, c+1] and grid[r, c] in (1, 2):
                blocks.append((grid[r, c], (r, c)))
    return blocks

def draw_diagonal(grid, start_row, start_col, color, direction):
    """Draws a diagonal line on the grid with the given color and direction. Stops one cell short of boundary."""
    row, col = start_row, start_col
    while True:
        if not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]):
            break
        
        next_row = row -1 if direction == "up-left" else row + 1
        next_col = col - 1 if direction == "up-left" else col + 1

        if not (0 <= next_row < grid.shape[0] and 0 <= next_col < grid.shape[1]):
            break

        if color == 2 and grid[row,col] != 0:
            break


        grid[row, col] = color

        row = next_row
        col = next_col

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.zeros_like(input_grid)

    # Find 2x2 blocks
    blocks = find_blocks(input_grid)

    # Draw blue diagonals (overwriting)
    for color, (row, col) in blocks:
        if color == 1:
            draw_diagonal(output_grid, row, col, 1, "up-left")
            draw_diagonal(output_grid, row + 1, col + 1, 1, "down-right")

    # Draw red diagonals (stop at non-black cells)
    for color, (row, col) in blocks:
        if color == 2:
            draw_diagonal(output_grid, row, col, 2, "up-left")
            draw_diagonal(output_grid, row + 1, col + 1, 2, "down-right")

    return output_grid