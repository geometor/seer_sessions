import numpy as np

def find_shape_color(grid):
    """
    Finds the first non-white (0) and non-gray (5) color in the grid.
    """
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and grid[r, c] != 5:
                return grid[r, c]
    return 0 # Should not happen based on examples, but return white as default

def transform(input_grid):
    """
    The transformation identifies the main colored shape (excluding gray)
    in the input grid. It then creates an output grid of the same size.
    The original shape is preserved in the output. Additionally, a mirrored
    version of the shape is added to the output grid. The mirroring is done
    horizontally across the vertical center line of the grid. Any gray pixels
    from the input are ignored and effectively removed in the output.
    """
    # Convert input list of lists to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with white (0)
    output_np = np.zeros_like(input_np)

    # Find the primary color of the shape (ignore white and gray)
    shape_color = find_shape_color(input_np)

    # Iterate through the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is part of the shape
            if input_np[r, c] == shape_color:
                # Copy the original pixel to the output
                output_np[r, c] = shape_color

                # Calculate the mirrored column index
                mirrored_c = width - 1 - c

                # Add the mirrored pixel to the output
                output_np[r, mirrored_c] = shape_color

    # Convert the numpy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
