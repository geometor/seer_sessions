```python
"""
Applies a horizontal scanline fill transformation.
It processes the grid row by row. For each row, it iterates through the cells,
toggling an 'inside' state whenever an orange (7) pixel is encountered.
If a white (0) or maroon (9) pixel is encountered while in the 'inside' state,
it is changed to azure (8) in the output grid. Orange pixels and white/maroon
pixels encountered while 'outside' remain unchanged.
"""

import numpy as np

# Define color constants for clarity
BG_WHITE = 0
BOUNDARY_ORANGE = 7
FILL_AZURE = 8
NON_FILL_MAROON = 9

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Fills areas horizontally enclosed by orange boundaries using a scanline approach.

    Args:
        input_grid: A 2D numpy array representing the input grid with integer
                    color values (0-9).

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape
    # Initialize output_grid as a copy of the input. We will modify this.
    output_grid = np.copy(input_grid)

    # Iterate through each row of the grid.
    for r in range(rows):
        # Initialize the state for the current row. 'False' means 'outside'.
        is_inside = False
        # Iterate through each cell (column) in the current row.
        for c in range(cols):
            # Get the color of the current cell from the original input grid.
            current_color = input_grid[r, c]

            # Check if the current cell is a boundary color (orange).
            if current_color == BOUNDARY_ORANGE:
                # Toggle the state: if outside, become inside; if inside, become outside.
                is_inside = not is_inside
                # The boundary pixel itself remains unchanged (already copied).
            # Check if the current cell is a fillable color (white or maroon).
            elif current_color == BG_WHITE or current_color == NON_FILL_MAROON:
                # If we are currently 'inside' the boundaries...
                if is_inside:
                    # Change this pixel's color to the fill color (azure) in the output grid.
                    output_grid[r, c] = FILL_AZURE
                # If 'outside', the pixel remains unchanged (already copied).
            # Else (for any other color, though not expected in this task):
            # The pixel remains unchanged (already copied).
            # No explicit action needed here.

    # Return the modified grid.
    return output_grid
```