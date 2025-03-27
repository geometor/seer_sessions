import numpy as np

"""
Transforms an input grid by generating 'L' shapes for each non-white pixel.

1. Initializes an output grid of the same dimensions as the input, filled with white (0).
2. Scans the input grid to identify all non-white pixels, recording their color, row, and column.
3. For each identified non-white pixel (color C, row R, column Col):
   a. Draws a horizontal line in the output grid: Fills cells in row R from column Col to the rightmost column (width-1) with color C.
   b. Draws a vertical line in the output grid: Fills cells in the rightmost column (width-1) from row R down to the bottommost row (height-1) with color C.
4. Overlapping regions take the color of the last drawn L-shape segment that covers them.
5. Returns the final output grid.
"""

def transform(input_grid):
    """
    Applies the L-shape generation rule to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(input_array)

    # Find all non-white pixels in the input grid
    non_white_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_array[r, c]
            if color != 0:
                non_white_pixels.append({'row': r, 'col': c, 'color': color})

    # Generate 'L' shapes for each non-white pixel
    for pixel_info in non_white_pixels:
        r = pixel_info['row']
        col = pixel_info['col']
        color = pixel_info['color']

        # Draw Horizontal Line
        # Iterate from the pixel's column to the last column
        for j in range(col, width):
            output_grid[r, j] = color

        # Draw Vertical Line
        # Iterate from the pixel's row to the last row, in the last column
        for i in range(r, height):
            output_grid[i, width - 1] = color

    return output_grid.tolist() # Return as list of lists to match ARC standard output format