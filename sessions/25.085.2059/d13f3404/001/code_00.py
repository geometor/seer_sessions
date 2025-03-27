import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating an output grid double the size (both height and width).
    The output grid is populated by repeatedly copying the input grid pattern diagonally downwards and to the right.
    For each cell in the output grid, its color is determined by the first non-white (non-zero) color encountered when tracing back diagonally (up-left) through the layers of copied input patterns.
    If no non-white color is found along this trace within the bounds of the original input grid dimensions relative to the shifts, the output cell remains white (0).
    """

    # Convert input_grid to a numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output grid dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell (r, c) in the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Iterate through possible diagonal shifts 'k' starting from 0
            # k represents how many steps down and right the input pattern is shifted
            for k in range(max(output_height, output_width)): # Iterate k up to a reasonable maximum
                # Calculate the potential source coordinates in the input grid for this shift k
                input_row = r - k
                input_col = c - k

                # Check if these input coordinates are within the bounds of the original input grid
                if 0 <= input_row < input_height and 0 <= input_col < input_width:
                    # Get the color from the input grid at these coordinates
                    input_color = input_np[input_row, input_col]

                    # If the color is non-white (not 0)
                    if input_color != 0:
                        # Assign this color to the output grid cell
                        output_grid[r, c] = input_color
                        # Break the inner loop (k) since we found the color for this output cell
                        # The first non-white color encountered when tracing back diagonally takes precedence
                        break
                # Optimization: If either coordinate goes negative, further shifts (larger k)
                # will also result in negative coordinates for this output cell (r, c).
                # We can stop checking shifts for this cell.
                elif input_row < 0 or input_col < 0:
                     break # No need to check larger k for this output cell

    # Convert the result back to a list of lists if necessary for the environment
    # return output_grid.tolist()
    return output_grid