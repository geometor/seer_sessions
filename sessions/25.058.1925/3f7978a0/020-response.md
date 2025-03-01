# 3f7978a0 • 020 • refine_coder

---
```python
"""
1.  **Extract:** Locate all azure (8) and grey (5) pixels in the input grid. Ignore all other colors.
2.  **Determine Output Dimensions:**
    *   The output grid height is always 6.
    *   Identify distinct columns containing grey pixels. The output width will be double number of unique grey columns minus 1, unless there is only 1 column, then it should be 3.
3.  **Create Output Grid:** Initialize an empty output grid of size 6 x Calculated Width, filled with black (0).
4.  **Place Grey Pixels:** Place the grey pixels into the output grid.
    *   There will be a grey pixel at the top most row.
    *   Maintain the relative column positions of the grey pixels.
    *   Ensure symmetry: Duplicate each grey pixel symmetrically across both the horizontal and vertical center lines of the output grid.
5.  **Place Azure Pixels:** For each azure pixel in the input, find the nearest grey pixel column.
     * Place an azure pixel adjacent to the grey pixel on the same row in the output grid. Adjacency here means side by side.
     * Maintain horizontal and vertical symmetry
6.  **Ensure Symmetry:** The final arrangement must be symmetrical across both the horizontal and vertical midlines of the output grid.
"""

import numpy as np

def get_colored_pixels(grid, colors_to_extract):
    """ Extracts coordinates and colors of specified colors. """
    coords = []
    colors = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel in colors_to_extract:
                coords.append((row_idx, col_idx))
                colors.append(pixel)
    return coords, colors

def transform(input_grid):
    # extract azure and grey pixels
    coords, colors = get_colored_pixels(input_grid, [5, 8])

    if not coords:
        return np.zeros((1, 1), dtype=int)

    # separate azure and grey coordinates
    grey_coords = [c for c, color in zip(coords, colors) if color == 5]
    azure_coords = [c for c, color in zip(coords, colors) if color == 8]

    # determine output grid size
    output_height = 6
    grey_cols = sorted(list(set([c[1] for c in grey_coords])))
    output_width = len(grey_cols) + (len(grey_cols)-1) if len(grey_cols) >1 else (3 if len(grey_cols) == 1 else 1)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # calculate the center column for mirroring
    center_col = output_width // 2

    # place grey pixels
    for row, col in grey_coords:
      new_row = row - min(r for r, _ in grey_coords) # Normalize row to top
      new_col_index = grey_cols.index(col)
      new_col = new_col_index
      output_grid[new_row, new_col] = 5
      output_grid[output_height - 1 - new_row, new_col] = 5
      output_grid[new_row, output_width - 1 - new_col] = 5
      output_grid[output_height - 1 - new_row, output_width - 1 - new_col] = 5

    # place azure pixels, relative to grey, with adjacency
    for row, col in azure_coords:
        # find nearest grey
        nearest_grey_col_index = min(range(len(grey_cols)), key=lambda i: abs(grey_cols[i]-col))
        new_row = row - min(r for r, _ in grey_coords if _[1] == grey_cols[nearest_grey_col_index])
        if new_row > (output_height // 2) -1:
          new_row = (output_height // 2) -1


        # position of azure is adjacent to the gray columns,
        diff_col = col - grey_cols[nearest_grey_col_index]
        if abs(diff_col) > 1:
            diff_col = diff_col // abs(diff_col)  # Keep only the sign

        new_col_index = grey_cols.index(grey_cols[nearest_grey_col_index])

        new_col = new_col_index + diff_col


        if new_col < 0 or new_col > output_width -1 :
          continue

        output_grid[new_row, new_col] = 8
        output_grid[output_height - 1 - new_row, new_col] = 8 # Vertical mirror
        output_grid[new_row, output_width - 1 - new_col] = 8 # Horizontal mirror
        output_grid[output_height - 1 - new_row, output_width - 1 - new_col] = 8 # Both mirror

    return output_grid
```
