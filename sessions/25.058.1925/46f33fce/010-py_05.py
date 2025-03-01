"""
Transforms an input grid by expanding isolated non-zero pixels into rectangular blocks of the same color, 
using the white (0) pixels as boundaries. The blocks are squares sized relative to the number of non-zero pixels,
and their placement order is top-left to bottom-right based on the initial pixels.
"""

import numpy as np

def find_objects(grid):
    """Finds isolated non-zero pixels in the grid."""
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Check if it is an isolated pixel
                is_isolated = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != 0:
                            is_isolated = False
                            break
                    if not is_isolated:
                        break
                if is_isolated:
                    objects.append((r, c, grid[r, c]))
                    visited[r,c] = True #mark as visitied
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array
    objects = find_objects(input_grid)
    num_objects = len(objects)
    output_grid = np.zeros((input_grid.shape[0] * 2, input_grid.shape[1] * 2), dtype=int) #make output grid larger

    block_size = num_objects

    for i, (r, c, color) in enumerate(objects):
      #calculate the position of the block
      row_start = (i // 2) * (block_size)
      col_start = (i % 2) * (block_size)
      row_end = row_start + block_size
      col_end = col_start + block_size

      # Check for grid boundaries
      row_end = min(row_end, output_grid.shape[0])
      col_end = min(col_end, output_grid.shape[1])

      output_grid[row_start:row_end, col_start:col_end] = color

    return output_grid.tolist()