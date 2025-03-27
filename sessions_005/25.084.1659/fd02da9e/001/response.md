```python
import numpy as np

"""
1. Identify the single non-orange pixel (the "marker pixel") in the 8x8 input grid. Record its color and its coordinates (row, col).
2. Determine which corner the marker pixel occupies: top-left (0, 0), top-right (0, 7), bottom-left (7, 0), or bottom-right (7, 7).
3. Create a new 8x8 output grid filled entirely with orange (7).
4. Based on the identified corner, draw a specific 3-pixel shape using the marker pixel's color onto the output grid at coordinates relative to the original marker pixel's location (row, col):
    - If top-left (0, 0), draw at (+1,+1), (+1,+2), (+2,+1).
    - If top-right (0, 7), draw at (+1,-2), (+1,-1), (+2,-1).
    - If bottom-left (7, 0), draw at (-3,+2), (-2,+2), (-1,+3).
    - If bottom-right (7, 7), draw at (-3,-2), (-2,-2), (-1,-3).
5. The resulting grid is the final output.
"""

def find_marker_pixel(grid):
    """Finds the first pixel not matching the background color (assumed 7)."""
    rows, cols = grid.shape
    background_color = 7
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                return r, c, grid[r, c]
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Transforms the input grid by finding a corner marker pixel and drawing
    a corresponding 3-pixel shape in a new location.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    background_color = 7

    # Initialize output_grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # 1. Find the marker pixel and its properties
    marker_info = find_marker_pixel(input_grid_np)
    if marker_info is None:
        # Return the blank grid if no marker is found (edge case)
        return output_grid.tolist() 
        
    marker_row, marker_col, marker_color = marker_info

    # 2. Determine the corner and 4. Draw the output shape based on the corner
    pixels_to_draw = []
    if marker_row == 0 and marker_col == 0: # Top-left
        pixels_to_draw = [
            (marker_row + 1, marker_col + 1),
            (marker_row + 1, marker_col + 2),
            (marker_row + 2, marker_col + 1)
        ]
    elif marker_row == 0 and marker_col == cols - 1: # Top-right
        pixels_to_draw = [
            (marker_row + 1, marker_col - 2),
            (marker_row + 1, marker_col - 1),
            (marker_row + 2, marker_col - 1)
        ]
    elif marker_row == rows - 1 and marker_col == 0: # Bottom-left
        pixels_to_draw = [
            (marker_row - 3, marker_col + 2),
            (marker_row - 2, marker_col + 2),
            (marker_row - 1, marker_col + 3)
        ]
    elif marker_row == rows - 1 and marker_col == cols - 1: # Bottom-right
         pixels_to_draw = [
            (marker_row - 3, marker_col - 2),
            (marker_row - 2, marker_col - 2),
            (marker_row - 1, marker_col - 3)
        ]

    # Draw the pixels onto the output grid
    for r, c in pixels_to_draw:
        # Check bounds just in case, although based on examples they should be within 8x8
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = marker_color

    # 5. Return the final grid
    return output_grid.tolist()
```