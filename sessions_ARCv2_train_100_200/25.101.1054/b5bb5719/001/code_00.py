"""
1. Create a new grid, called `output_grid`, initially identical to the `input_grid`.
2. Iterate through each row of the `output_grid`, starting from the second row (row index 1) down to the last row. Let the current row index be `r`.
3. Within each row `r`, iterate through each column index `c` from 0 to the grid width minus 1.
4. For the current cell `(r, c)`, check if its color in `output_grid` is Orange (7). If it is not Orange (7), skip the following steps and proceed to the next column `c`.
5. Identify the two source pixel locations in the row above: `(r-1, c-1)` and `(r-1, c+1)`.
6. Determine the colors of these source pixels from the `output_grid`. If a source location `(r-1, col)` is outside the grid boundaries (i.e., `col < 0` or `col >= width`), treat its color as Orange (7). Let the left source color be `color1` and the right source color be `color2`.
7. Check if *both* `color1` and `color2` are non-Orange (i.e., both are Red (2) or Gray (5)). If either source color is Orange (7), do not modify the cell `(r, c)` and proceed to the next column `c`.
8. If both source colors are non-Orange, apply the transformation rule:
   a. If `color1` is the same as `color2`:
      i. If `color1` is Red (2), set the result color to Gray (5).
      ii. If `color1` is Gray (5), set the result color to Red (2).
   b. If `color1` is different from `color2`:
      i. Set the result color to be the same as `color2` (the color of the right source pixel).
9. Update the cell `(r, c)` in the `output_grid` with the calculated result color.
10. After processing all columns `c` for the current row `r`, move to the next row `r+1`.
11. Once all rows from 1 to the end have been processed, the `output_grid` contains the final result. Return the `output_grid`.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on a rule involving two pixels in the row above.
    The color of a pixel (r, c) below the first row depends on the colors of pixels
    (r-1, c-1) and (r-1, c+1) in the already processed grid, but only if the
    target pixel (r, c) is initially Orange (7) and both source pixels are
    either Red (2) or Gray (5).
    - If the two source pixels are the same (both Red or both Gray), the output
      pixel becomes the *other* color (Red -> Gray, Gray -> Red).
    - If the two source pixels are different (one Red, one Gray), the output
      pixel takes the color of the *right* source pixel (r-1, c+1).
    Out-of-bounds source pixels are treated as Orange (7).
    """
    # Define colors
    RED = 2
    GRAY = 5
    ORANGE = 7
    BOUNDARY_COLOR = ORANGE

    # Convert input to numpy array for easier indexing and manipulation
    output_grid = np.array(input_grid, dtype=int)
    height, width = output_grid.shape

    # Helper function to get color, handling boundary conditions
    def get_color(grid, r, c):
        if 0 <= r < height and 0 <= c < width:
            return grid[r, c]
        else:
            return BOUNDARY_COLOR

    # Iterate through rows starting from the second row (index 1)
    for r in range(1, height):
        # Iterate through columns
        for c in range(width):
            # Check if the current cell is Orange
            if output_grid[r, c] == ORANGE:
                # Get the colors of the two source pixels from the row above
                # Note: We use the potentially already modified output_grid
                #       because the transformation depends on the state of the row above.
                color1 = get_color(output_grid, r - 1, c - 1)
                color2 = get_color(output_grid, r - 1, c + 1)

                # Check if both source colors are non-Orange (Red or Gray)
                if color1 != ORANGE and color2 != ORANGE:
                    # Apply the transformation rule
                    if color1 == color2:
                        # If both are the same, swap the color
                        new_color = GRAY if color1 == RED else RED
                    else:
                        # If different, take the color of the right source pixel
                        new_color = color2

                    # Update the output grid
                    output_grid[r, c] = new_color

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()