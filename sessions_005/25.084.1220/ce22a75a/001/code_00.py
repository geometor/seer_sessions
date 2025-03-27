import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing each gray pixel (5) with a 3x3 blue square (1) centered at the gray pixel's location. The background remains white (0). Overlapping blue squares merge.

    1. Initialize an output grid of the same size as the input grid, filling it entirely with white pixels (0).
    2. Iterate through each pixel of the input grid to find the row and column coordinates of all gray pixels (5).
    3. For each gray pixel found at coordinates (row, col):
        a. Consider the 3x3 square region centered at (row, col).
        b. Iterate through each cell (r, c) within this 3x3 region (from row-1 to row+1, and col-1 to col+1).
        c. If the cell coordinate (r, c) is within the bounds of the grid dimensions, change the pixel at position (r, c) in the output grid to blue (1).
    4. Return the final output grid.
    """

    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    height, width = input_array.shape

    # Initialize output_grid with the same dimensions as the input, filled with white (0)
    output_grid = np.zeros_like(input_array)

    # Find the coordinates of all gray pixels (5)
    gray_pixels_coords = np.argwhere(input_array == 5)

    # Define the color for the squares
    blue_color = 1

    # For each gray pixel coordinate
    for center_row, center_col in gray_pixels_coords:
        # Iterate through the 3x3 region centered at the gray pixel
        for r in range(center_row - 1, center_row + 2):
            for c in range(center_col - 1, center_col + 2):
                # Check if the coordinate (r, c) is within the grid boundaries
                if 0 <= r < height and 0 <= c < width:
                    # Set the corresponding pixel in the output grid to blue (1)
                    output_grid[r, c] = blue_color

    # Convert back to list of lists if necessary, though numpy array is often preferred
    return output_grid.tolist()