"""
1.  **Copy Grid:** Create an output grid that is initially a copy of the input grid.
2.  **Locate Blue Pixels:** Identify all pixels in the input grid that have a value of 1 (blue). These pixels will be the "seed" points for color expansion.
3. **Preserve Blue:** Keep all blue pixels from the input grid unchanged in the output grid.
4.  **Ordered Expansion:** For *each* blue pixel, examine its four immediate neighbors (Up, Down, Left, Right) *in that order*.
5. **Deterministic Coloring**:
    *   If a neighbor is white (0) in the *output* grid, change its color according to the following rule, based on the neighbor's position relative to the current blue pixel, using a fixed color sequence (2, 6, 7, 8):
        *   Up: Change the white pixel to 2 (red).
        *   Down: Change the white pixel to 6 (magenta).
        *   Left: Change the white pixel to 7 (orange).
        *   Right: Change the white pixel to 8 (azure).
6. Do not expand colors from non-blue pixels.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right) in order."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col, "Up"))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col, "Down"))  # Down
    if col > 0:
        neighbors.append((row, col - 1, "Left"))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1, "Right"))  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find the blue pixels in input_grid
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 1:
                blue_pixels.append((r,c))
    
    # Iterate and expand based on relative position
    color_map = {
        "Up": 2,
        "Down": 6,
        "Left": 7,
        "Right": 8
    }
    
    for r, c in blue_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        
        for nr, nc, direction in neighbors:
            if output_grid[nr,nc] == 0: # if the neighbor in the output grid is white
                output_grid[nr, nc] = color_map[direction]

    return output_grid