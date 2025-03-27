import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a 12x6 input grid into a 3x6 output grid.
    The input grid is treated as four stacked 3x6 subgrids.
    For each cell (r, c) in the output grid, its color is determined by checking the corresponding cells
    in the input subgrids from top to bottom: input[r, c], input[r+3, c], input[r+6, c], and input[r+9, c].
    The output color is the color of the first non-white (non-zero) cell encountered in this sequence.
    If all four corresponding input cells are white, the output cell remains white.
    """

    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_height = input_height // 4
    output_width = input_width

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Check the color in the first subgrid (rows 0-2)
            color1 = input_grid[r, c]
            if color1 != 0:
                output_grid[r, c] = color1
                continue # Move to the next output cell

            # If color1 is white, check the second subgrid (rows 3-5)
            color2 = input_grid[r + output_height, c]
            if color2 != 0:
                output_grid[r, c] = color2
                continue # Move to the next output cell

            # If color2 is white, check the third subgrid (rows 6-8)
            color3 = input_grid[r + 2 * output_height, c]
            if color3 != 0:
                output_grid[r, c] = color3
                continue # Move to the next output cell

            # If color3 is white, check the fourth subgrid (rows 9-11)
            # The output color will be this color, even if it's white.
            color4 = input_grid[r + 3 * output_height, c]
            output_grid[r, c] = color4

    return output_grid