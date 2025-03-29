import numpy as np

"""
Transformation Rule:

1.  Create the output grid as a copy of the input grid.
2.  Identify potential "pattern units," which are notionally 5x5 blocks starting at coordinates (row, col) where both row and col are multiples of 5.
3.  Examine the top-left corner pixel (the "trigger pixel") of each pattern unit in the *input* grid.
4.  If the trigger pixel's color is *not* white (0), then it is an "active trigger." Store its color (`fill_color`) and its location (`trigger_row`, `trigger_col`).
5.  For *each* active trigger identified:
    a.  In the *output* grid, change the color of the pixel at the trigger location (`trigger_row`, `trigger_col`) to white (0).
    b.  Consider the 5x5 block associated with this trigger in the *input* grid (from `trigger_row` to `min(trigger_row + 5, height)`, and `trigger_col` to `min(trigger_col + 5, width)`).
    c.  For every pixel within this 5x5 block (excluding the trigger pixel itself at `trigger_row`, `trigger_col`): if that pixel's color in the *input* grid is white (0), change the corresponding pixel in the *output* grid to the stored `fill_color`.
6.  Pattern units whose trigger pixel in the input grid is white (0) do not initiate any changes themselves. Their pixels in the output grid remain as they were copied from the input, unless modified by the fill action of an adjacent active trigger.
7.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a transformation based on trigger pixels located at the corners of 5x5 blocks.
    If a corner pixel (r, c where r and c are multiples of 5) is not white (0),
    its color is used to fill the white pixels within its corresponding 5x5 block in the output grid,
    and the trigger pixel itself is set to white in the output.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Iterate through the grid, checking the top-left corner of potential 5x5 blocks
    # These corners have row and column indices that are multiples of 5
    for r in range(0, height, 5):
        for c in range(0, width, 5):
            # Get the color of the potential trigger pixel from the *input* grid
            trigger_pixel_color = input_np[r, c]

            # Check if the corner pixel is an active trigger (any color except white)
            if trigger_pixel_color != 0:
                # Store the trigger color to be used for filling
                fill_color = trigger_pixel_color

                # Set the trigger pixel location in the *output* grid to white
                output_grid[r, c] = 0

                # Iterate through the 5x5 block associated with the trigger pixel
                # Ensure loops do not go beyond grid boundaries using min()
                for y in range(r, min(r + 5, height)):
                    for x in range(c, min(c + 5, width)):
                        # Skip the trigger pixel itself, as it's already handled
                        if y == r and x == c:
                            continue

                        # Check if the pixel in the *input* grid block is white (0)
                        if input_np[y, x] == 0:
                            # If it is white in the input, fill the corresponding
                            # pixel in the *output* grid with the fill_color
                            output_grid[y, x] = fill_color

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()