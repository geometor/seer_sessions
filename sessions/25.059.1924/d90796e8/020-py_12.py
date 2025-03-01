"""
Identify and replace adjacent red and green pixels with azure, regardless of their order or direction of adjacency.  Continue this replacement iteratively until no more adjacent red and green pixels exist.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    changes_made = True
    while changes_made:
        changes_made = False
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 2:  # Red pixel
                    # Check all eight neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip the pixel itself
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 3:
                                output_grid[r, c] = 8
                                output_grid[nr, nc] = 8
                                changes_made = True
                elif output_grid[r, c] == 3:  # Green pixel
                    # Check all eight neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # skip the pixel itself
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 2:
                                output_grid[r, c] = 8
                                output_grid[nr, nc] = 8
                                changes_made = True
    return output_grid