import numpy as np

"""
Transformation Rule:

1.  Identify "pattern units," which are 5x5 blocks starting at coordinates (row, col) where both row and col are multiples of 5.
2.  Check the top-left corner pixel (row, col) of each pattern unit in the input grid.
3.  If this corner pixel's color is neither white (0) nor azure (8), it's a "trigger pixel."
4.  For each trigger pixel found:
    a.  Store its color (fill_color).
    b.  In the output grid (initially a copy of the input), set the pixel at the trigger location (row, col) to white (0).
    c.  Examine the 5x5 block in the *input* grid corresponding to this pattern unit.
    d.  For every pixel within this 5x5 block (excluding the trigger pixel itself) that is white (0) in the input grid, change the corresponding pixel in the *output* grid to the fill_color.
5.  Pattern units whose top-left corner pixel is white (0) or azure (8) remain unchanged in the output grid, except for modifications caused by adjacent trigger pixels (which shouldn't happen based on the examples, as the frame is azure).
"""

def transform(input_grid):
    """
    Applies a transformation based on trigger pixels located at the corners of 5x5 blocks.
    If a corner pixel (r, c where r and c are multiples of 5) is not white (0) or azure (8),
    its color is used to fill the white pixels within its corresponding 5x5 block in the output grid,
    and the trigger pixel itself is set to white in the output.
    """
    input_np = np.array(input_grid)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Iterate through the grid, checking the top-left corner of potential 5x5 blocks
    for r in range(0, height, 5):
        for c in range(0, width, 5):
            trigger_pixel_color = input_np[r, c]

            # Check if the corner pixel is a trigger (not white and not azure)
            if trigger_pixel_color != 0 and trigger_pixel_color != 8:
                fill_color = trigger_pixel_color

                # Reset the trigger pixel location in the output grid to white
                output_grid[r, c] = 0

                # Iterate through the 5x5 block associated with the trigger pixel
                for y in range(r, min(r + 5, height)):
                    for x in range(c, min(c + 5, width)):
                        # Skip the trigger pixel itself
                        if y == r and x == c:
                            continue

                        # If the pixel in the *input* grid block is white,
                        # fill the corresponding pixel in the *output* grid with the fill_color
                        if input_np[y, x] == 0:
                            output_grid[y, x] = fill_color

    return output_grid.tolist()