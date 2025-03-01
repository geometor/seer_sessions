# 3428a4f5 • 020 • refine_coder

---
```python
"""
1. **Identify Motif:** Find a repeating structural "motif" in the input grid. The motif is not necessarily a single-color vertical block, but a distinct, repeating pattern or object within the grid. The starting position of this motif is important. The definition of "motif" needs to be determined by observation across multiple examples, it might be a specific shape, arrangement of colors, or a self-contained object.

2. **Determine Motif Properties**: Note starting row, and size (height, width).

3. **Construct Output Grid:**
    *   The output grid's width is the same as the input grid's width.
    *   The output grid's height often, but not always, seems related to removing a number of rows based on either the size or placement of a motif, but sometimes it appears to *add* rows.
    *   Create a section of all-white rows at the top of the output grid, where the height is equal to the top row index of the motif in the input grid.

4. **Populate Output:**
    *   Copy the identified motif from the input grid to the output grid, starting immediately below the all-white rows.
    *   If the motif is only partially included, only the included portion is copied

5. **Color Transformation (Conditional):**
    *   If the motif includes the color red (2), change all instances of red (2) within the copied motif to green (3) in the output. Otherwise, colors remain unchanged.
"""

import numpy as np

def find_motif(grid):
    """Attempts to identify a potential motif based on observations."""
    # Initial simplistic approach: look for smallest non-white rectangle
    rows, cols = grid.shape
    for height in range(1, rows + 1):
        for width in range(1, cols + 1):
            for r in range(0, rows - height + 1):
                for c in range(0, cols - width + 1):
                    subgrid = grid[r:r+height, c:c+width]
                    if np.any(subgrid != 0):  # Check if it's not all white
                        return r, c, height, width, subgrid.copy()
    return 0, 0, 0, 0, np.zeros((0,0)) # Return empty if no motif is found


def transform(input_grid):
    input_grid = np.array(input_grid)
    # Find the motif
    motif_top_row, motif_left_col, motif_height, motif_width, motif = find_motif(input_grid)

    # Construct output grid
    output_height = motif_top_row + motif_height
    output_width = input_grid.shape[1]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate output grid with white rows
    # (already initialized to 0, which represents white)

    # Copy motif to output, handling color change
    for r in range(motif_height):
        for c in range(motif_width):
            color = motif[r, c]
            if color == 2:
                output_grid[motif_top_row + r, motif_left_col + c] = 3  # Red to green
            else:
                output_grid[motif_top_row + r, motif_left_col + c] = color

    # adjust for offset of motif not at 0
    output_grid[:, :motif_left_col] = 0 # blank out columns to left of motif

    return output_grid
```
