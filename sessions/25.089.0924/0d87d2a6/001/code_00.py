import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return set(zip(rows, cols))

def transform(input_grid):
    """
    Transforms the input grid based on the locations of blue pixels (1).

    Identifies all pixels with color blue (1) in the input grid. Determines the
    set of unique row indices and column indices containing these blue pixels.
    Creates an output grid of the same dimensions as the input. For each pixel
    location (row, col), if its row index is in the set of affected rows OR
    its column index is in the set of affected columns, set the corresponding
    output pixel's color to blue (1). Otherwise, copy the color from the
    input grid at that location.
    """
    # Convert input grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Find coordinates of all blue pixels (color 1)
    blue_pixels_coords = find_pixels_by_color(input_array, 1)

    # Collect unique row and column indices containing blue pixels
    affected_rows = set(r for r, c in blue_pixels_coords)
    affected_cols = set(c for r, c in blue_pixels_coords)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # If the current row or column contained a blue pixel in the input
            if r in affected_rows or c in affected_cols:
                # Change the corresponding output pixel to blue (1)
                output_array[r, c] = 1
            # Otherwise, the pixel retains its original color (already copied)

    # Convert the numpy array back to a list of lists
    return output_array.tolist()
