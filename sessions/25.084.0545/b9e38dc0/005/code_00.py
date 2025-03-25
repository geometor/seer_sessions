"""
1.  **Global Color Mapping:**
    *   Examine all input/output pairs.
    *   Create a dictionary mapping each input color to its corresponding output color.

2.  **Apply Color Map to Input:**
    *   Iterate through all cells of the input grid.
    *   Replace each cell's color with its mapped output color, if a mapping exists.

3.  **Iterative Propagation:**
    * Create a set `changed_pixels` to store information about changed pixels: `(row, col, old_color, new_color)`.
    *   Iterate through all cells of the *current* grid (after the initial color mapping).
        *   If a cell's color in the current grid is different from its color in the *original* input grid:
            *   Add `(row, col, old_color, new_color)` to `changed_pixels`.
    *   While `changed_pixels` is not empty:
        *   Create an empty set `next_changed_pixels`.
        *   For each `(row, col, old_color, new_color)` in `changed_pixels`:
           *   Check the eight neighbors (up, down, left, right, and diagonals) of the cell at `(row, col)`.
           *   For each neighbor `(nr, nc)`:
             *  If `(nr,nc)` has not already been modified (not in `next_changed_pixels`) and color is not background (white):
                *   If the neighbor's *current* color is equal to *any* `old_color` in *any* element of changed_pixels:
                    *   Change the neighbor's color to the corresponding `new_color`.
                    *   Add `(nr, nc, current_neighbor_color, new_color)` to `next_changed_pixels`.
        *  Update `changed_pixels` to `next_changed_pixels`.

4. Apply changes to all cells that match the input/output color map.
"""

import numpy as np

# Global variables to store training data.
train_inputs = []
train_outputs = []

def calculate_color_mapping(inputs, outputs):
    """Calculates the color mapping between input and output grids."""
    color_mapping = {}
    for input_grid, output_grid in zip(inputs, outputs):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        for i in range(input_grid.shape[0]):
            for j in range(input_grid.shape[1]):
                input_val = input_grid[i, j]
                output_val = output_grid[i, j]
                if input_val != output_val:
                    color_mapping[input_val] = output_val
    return color_mapping

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Global Color Mapping
    color_mapping = calculate_color_mapping(train_inputs, train_outputs)


    # 2. Apply Color Map to Input
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] in color_mapping:
                output_grid[r, c] = color_mapping[input_grid[r, c]]

    # 3. Iterative Propagation
    changed_pixels = set()
     # initialize changed pixels
    for r in range(rows):
      for c in range(cols):
        if (input_grid[r,c] in color_mapping and
             output_grid[r,c] != input_grid[r,c]):
             old_color = input_grid[r,c]
             new_color = output_grid[r,c]
             changed_pixels.add( (r,c, old_color, new_color) )

    while changed_pixels:
        next_changed_pixels = set()
        for r, c, old_color, new_color in changed_pixels:
            # Check neighbors (up, down, left, right, and diagonals)
            neighbors = [
                (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)
            ]
            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols:
                    modified = False
                    for cr, cc, co, cn, in next_changed_pixels:
                       if nr == cr and nc == cc:
                          modified = True
                          break

                    if not modified:
                       for changed_r, changed_c, changed_old_color, changed_new_color in changed_pixels:
                            if output_grid[nr, nc] == changed_old_color:
                                output_grid[nr, nc] = changed_new_color
                                next_changed_pixels.add((nr, nc, changed_old_color, changed_new_color))
                                break

        changed_pixels = next_changed_pixels

    return output_grid