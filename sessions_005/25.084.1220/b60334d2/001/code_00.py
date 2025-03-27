"""
Transformation Rule:

1. Create a new output grid with the same dimensions as the input grid, filled entirely with white (0) pixels.
2. Identify the coordinates (row, column) of every gray (5) pixel in the input grid.
3. For each identified gray pixel location (r, c):
    a. Define the 3x3 pattern centered at (r, c). The pattern is:
        Gray Blue Gray   (5 1 5)
        Blue White Blue  (1 0 1)
        Gray Blue Gray   (5 1 5)
    b. Apply this pattern to the output grid centered at (r, c).
    c. For each of the 9 positions (pr, pc) covered by this pattern:
        i. Check if the position (pr, pc) is within the valid row and column boundaries of the output grid.
        ii. If it is within bounds, set the pixel value at (pr, pc) in the output grid to the color specified by the pattern for that relative position. This overwrites any previous value.
4. After processing all gray pixels from the input, return the resulting output grid.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Applies a 3x3 pattern centered on each gray (5) pixel found in the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with white (0) pixels
    output_grid = np.zeros_like(input_np)

    # Define the 3x3 pattern (relative coordinates -> color)
    # We can represent this as a 3x3 array for direct indexing
    pattern = np.array([
        [5, 1, 5],
        [1, 0, 1],
        [5, 1, 5]
    ], dtype=int)

    # Find the locations of all gray (5) pixels in the input
    gray_pixels = find_pixels(input_np, 5)

    # Iterate through each gray pixel location
    for r, c in gray_pixels:
        # Apply the pattern centered at (r, c)
        for dr in range(-1, 2):  # Relative row offset (-1, 0, 1)
            for dc in range(-1, 2):  # Relative col offset (-1, 0, 1)
                # Calculate the absolute coordinates in the output grid
                pr = r + dr
                pc = c + dc

                # Check if the coordinates are within the grid boundaries
                if 0 <= pr < height and 0 <= pc < width:
                    # Get the color from the pattern based on relative offset
                    # Adjust indices for pattern array (dr+1, dc+1)
                    pattern_color = pattern[dr + 1, dc + 1]

                    # Apply the pattern color to the output grid
                    output_grid[pr, pc] = pattern_color

    # Convert back to list of lists if necessary, or return numpy array
    # Assuming the standard format is list of lists for ARC tasks
    return output_grid.tolist()
