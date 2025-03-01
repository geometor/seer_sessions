import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height + 2
    output_width = input_width + 2

    # Initialize output_grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy input grid to the center of the output grid
    output_grid[1:input_height+1, 1:input_width+1] = input_grid

    # Create the border

    # Top border (excluding corners)
    output_grid[0, 1:output_width-1] = input_grid[0, :]
    # Bottom border (excluding corners)
    output_grid[output_height-1, 1:output_width-1] = input_grid[input_height-1, :]
    # Left border (excluding corners)
    output_grid[1:output_height-1, 0] = input_grid[:, 0]
    # Right border (excluding corners)
    output_grid[1:output_height-1, output_width-1] = input_grid[:, input_width-1]

    # Corners - very important for seamless connection of the border
    output_grid[0, 0] = input_grid[0, 0]  # Top-left
    output_grid[0, output_width - 1] = input_grid[0, input_width - 1]  # Top-right
    output_grid[output_height - 1, 0] = input_grid[input_height - 1, 0]  # Bottom-left
    output_grid[output_height - 1, output_width - 1] = input_grid[input_height - 1, input_width - 1]  # Bottom-right

    return output_grid