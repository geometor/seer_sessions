"""
1. **Identify the Cross:** Locate the central, cross-shaped pattern spanning the grid. Note its color.
2. **Iterate through Rows:** For each row in the grid:
3. **Identify Target Pixels:** Find pixels *within the current row* that have a color *different* from the cross' color.
4. **Extend Target Pixels:**  if there are multiple pixels with the same color: connect all pixels of the target color within that row and the cross by filling the spaces between. It seems that the cross color will always be found within this range.
"""

import numpy as np

def get_cross_color(grid):
    """Finds color of the central cross"""
    center_row = len(grid) // 2
    for col in range(len(grid[0])):
      if grid[center_row][col] != 0:
        return grid[center_row][col]
    return 0

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])
    cross_color = get_cross_color(input_grid)


    for r in range(rows):
        # Iterate through rows
        row = input_grid[r]

        #find the first and last non-background pixel in current row
        colored_pixels = np.where(row != 0)[0]

        if len(colored_pixels) > 0:
            first_pixel = colored_pixels[0]
            last_pixel = colored_pixels[-1]
        else: continue # if no non_zero pixels in row

        # find targets
        for c in range(first_pixel, last_pixel + 1):
            current_color = input_grid[r][c]

            # check if the target needs extension
            if current_color != cross_color and current_color!=0:
                target_color = current_color
                target_indices = []

                # find the indices of target color
                for inner_c in range(first_pixel, last_pixel + 1):
                    if input_grid[r][inner_c] == target_color:
                        target_indices.append(inner_c)

                # perform the fill
                if len(target_indices)>1:
                  first_target = target_indices[0]
                  last_target = target_indices[-1]

                  for fill_c in range(first_target, last_target + 1):
                    output_grid[r][fill_c] = target_color

    return output_grid