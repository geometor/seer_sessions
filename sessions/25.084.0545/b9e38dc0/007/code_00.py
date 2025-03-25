"""
1.  **Identify Initial Changes:** Examine all input/output pairs. Identify pixels that change color between the input and output grids.  These are your "seed" changes.

2.  **Propagate Changes:**
    *   Iterate through the grid. If a pixel has a neighbor that has *changed* to a new color (either in the initial changes or in a previous propagation step), and the current pixel's original color could become the neighboring pixel's *new* color (check color changes observed in all training pairs), change the current pixel's color to the new color.
    *  The previous step suggests to use color mapping, but based on analyzing the examples, we determined it is simpler: if a pixel changes color, all neighbors of the original color will also change.
    *   Repeat this propagation step until no more pixels change color.

3. **Object Specific Rules (Exceptions)**
    * In example 3, pixels of color 7 that neighbor color 9 become color 3
"""

import numpy as np

# Global variables to store training data, needed for neighbor checking
train_inputs = []
train_outputs = []

def get_neighbors(r, c, rows, cols):
    """Gets valid neighbors of a cell."""
    neighbors = [
        (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
        (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)
    ]
    valid_neighbors = [(nr, nc) for nr, nc in neighbors if 0 <= nr < rows and 0 <= nc < cols]
    return valid_neighbors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Store initial changes
    changed_pixels = set()

   # identify color changes between all input and output grids
    color_changes = set()
    for inp, out in zip(train_inputs, train_outputs):
        inp = np.array(inp)
        out = np.array(out)
        for r in range(inp.shape[0]):
            for c in range(inp.shape[1]):
               if inp[r,c] != out[r,c]:
                  color_changes.add( (inp[r,c], out[r,c]))


    # 1. Identify Initial Changes
    for r in range(rows):
        for c in range(cols):
            for old_color, new_color in color_changes:
               if input_grid[r,c] == old_color:
                  neighbors = get_neighbors(r,c, rows, cols)
                  for nr, nc in neighbors:
                      for in_grid, out_grid in zip(train_inputs, train_outputs):
                         in_grid = np.array(in_grid)
                         out_grid = np.array(out_grid)
                         in_rows, in_cols = in_grid.shape

                         if 0 <= nr < in_rows and 0 <= nc < in_cols:
                            if in_grid[nr, nc] != out_grid[nr,nc] and out_grid[nr,nc] == new_color:
                               output_grid[r,c] = new_color
                               changed_pixels.add( (r,c, old_color, new_color) )
                               break
                      if (r,c,old_color, new_color) in changed_pixels:
                         break

    # 2. Propagate Changes
    while changed_pixels:
        next_changed_pixels = set()
        for r, c, old_color, new_color in changed_pixels:
            neighbors = get_neighbors(r, c, rows, cols)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == old_color:
                    output_grid[nr, nc] = new_color
                    next_changed_pixels.add((nr, nc, old_color, new_color))
        changed_pixels = next_changed_pixels

    # 3. Object specific
    for r in range(rows):
       for c in range(cols):
          if output_grid[r,c] == 7:
             neighbors = get_neighbors(r,c, rows, cols)
             for nr, nc in neighbors:
                if output_grid[nr,nc] == 9:
                   output_grid[r,c] = 3
                   break

    return output_grid