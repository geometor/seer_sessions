"""
The transformation rule involves identifying a seed pattern of colored pixels in the input grid,
and then vertically elongating, mirroring, and duplicating this pattern in the output grid.
The horizontal color sequence red(2), green(3), and azure(8), with yellow(4) above azure(8), defines the seed, which then expands to fill the vertical space.
"""

import numpy as np

def find_seed(input_grid):
    """Finds the non-zero pixels and their arrangement in the input grid."""
    rows, cols = np.where(input_grid != 0)
    seed_pixels = []
    for r, c in zip(rows, cols):
        seed_pixels.append((r, c, input_grid[r, c]))
    return seed_pixels

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the seed pixels.
    seed_pixels = find_seed(input_grid)

    # Find the center of the seed pattern.
    seed_rows = [p[0] for p in seed_pixels]
    seed_cols = [p[1] for p in seed_pixels]
   # seed_center_row = int(np.mean(seed_rows))
    seed_center_col = int(np.mean(seed_cols))

    # find the row where the center column has a 2
    seed_colors = [ (input_grid[r,c],r,c) for r,c in zip(seed_rows, seed_cols)]
    for color, row, col in seed_colors:
        if color == 2:
            center_row_start = row
            break


    # Determine vertical sequence
    vertical_sequence = []
    for color, row, col in seed_colors:
        if col == seed_center_col:
            vertical_sequence.append((row,color))
    vertical_sequence.sort()

    vertical_sequence_colors = [c for r,c in vertical_sequence]

    # Duplicate and elongate vertically.

    for r in range(rows):
      output_grid[r,seed_center_col] = vertical_sequence_colors[(r-center_row_start)% len(vertical_sequence_colors)]

    # Create horizontal sequence in the middle

    horizontal_sequence = []
    for color,row,col in seed_colors:
        if row == center_row_start:
            horizontal_sequence.append( (col,color) )

    horizontal_sequence.sort()
    horizontal_colors = [ c for col,c in horizontal_sequence]
   # print(horizontal_colors)
    for c in range(cols):
        # 3, 8, 4, 2
        output_grid[center_row_start,c] = horizontal_colors[c%4]
    
    return output_grid