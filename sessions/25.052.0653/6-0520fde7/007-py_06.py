import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of a gray line (color 5).
    """
    output_grid = np.zeros((3, 3), dtype=int)
    rows, cols = input_grid.shape
    gray_line_present = False
    gray_line_top = None

    # Find the gray line and top position
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 5:
              gray_line_present = True
              gray_line_top = (r,c)
              break # Assumes only 1 gray line
        if gray_line_present:
          break

    if gray_line_present:
        # Variant 1: Only gray pixels
        if np.all((input_grid == 5) | (input_grid == 0)):
          output_grid[1,1] = 2

        else:
          # Determine variant based on pixel left from top of gray line
          top_r, top_c = gray_line_top
          if top_c > 0:  # Ensure we don't go out of bounds
            left_pixel = input_grid[top_r, top_c -1]
            
          if top_c > 0 and left_pixel == 1:
            #Variant 2
            output_grid[0, 1] = 2
            output_grid[1, 2] = 2
            output_grid[2, 1] = 2

          elif top_c > 0 and left_pixel == 0:
            # Variant 3
            output_grid[0, 2] = 2
            output_grid[1, 0] = 2
            output_grid[2, 1] = 2

          else:
            output_grid[1, 1] = 2 # Fallback to center

    return output_grid