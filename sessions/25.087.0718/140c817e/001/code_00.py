import numpy as np

"""
Transforms the input grid based on the locations of blue (1) pixels.

1.  Identify all blue (1) pixels in the input grid.
2.  Create an output grid initialized as a copy of the input grid.
3.  For each blue pixel found at coordinates (r, c):
    a. Draw a horizontal line of blue (1) across the entire row r in the output grid.
    b. Draw a vertical line of blue (1) down the entire column c in the output grid.
4.  For each original blue pixel location (r, c):
    a. Change the pixel at (r, c) in the output grid to red (2).
    b. Change the four diagonal neighbors (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1) to green (3), if they are within the grid boundaries.
5.  The red (2) and green (3) pixels overwrite any blue (1) lines previously drawn at their locations.
"""

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    coords = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color:
                coords.append((r, c))
    return coords

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Identify the coordinates of all blue (1) pixels
    blue_coords = find_pixels(input_np, 1)

    # 3. Draw horizontal and vertical blue lines for each original blue pixel
    for r, c in blue_coords:
        # Draw horizontal line (row r)
        output_grid[r, :] = 1
        # Draw vertical line (column c)
        output_grid[:, c] = 1

    # 4. Place red (2) centers and green (3) diagonal markers
    for r, c in blue_coords:
        # a. Set the center pixel to red (2)
        output_grid[r, c] = 2
        
        # b. Define potential diagonal neighbors
        diagonals = [
            (r - 1, c - 1), (r - 1, c + 1),
            (r + 1, c - 1), (r + 1, c + 1)
        ]
        
        # c. Set valid diagonal neighbors to green (3)
        for nr, nc in diagonals:
            # Check if the neighbor coordinates are within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                output_grid[nr, nc] = 3

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()