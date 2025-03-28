```python
import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by drawing full horizontal or vertical lines based on the color and position of non-white pixels, ensuring horizontal lines (Blue, Green) take precedence over vertical lines (Red) at intersections.

    1. Initialize an output grid of the same dimensions as the input, filled with white (0).
    2. Find all unique row indices for Blue (1) and Green (3) pixels in the input.
    3. Find all unique column indices for Red (2) pixels in the input.
    4. Draw vertical Red lines: For each unique Red column index, fill the entire corresponding column in the output grid with Red (2).
    5. Draw horizontal Blue lines: For each unique Blue row index, fill the entire corresponding row in the output grid with Blue (1). This overwrites any existing pixels (including Red) in that row.
    6. Draw horizontal Green lines: For each unique Green row index, fill the entire corresponding row in the output grid with Green (3). This overwrites any existing pixels (including Red or Blue) in that row.
    7. Return the final output grid.
    """

    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with white pixels (0)
    output_grid = np.zeros_like(input_np)

    # Find unique rows/columns for each color
    blue_rows = set()
    red_cols = set()
    green_rows = set()

    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            if pixel_color == 1: # Blue
                blue_rows.add(r)
            elif pixel_color == 2: # Red
                red_cols.add(c)
            elif pixel_color == 3: # Green
                green_rows.add(r)

    # Draw vertical Red lines first
    for c in red_cols:
        output_grid[:, c] = 2

    # Draw horizontal Blue lines next (overwriting Red where necessary)
    for r in blue_rows:
        output_grid[r, :] = 1

    # Draw horizontal Green lines last (overwriting Red or Blue where necessary)
    for r in green_rows:
        output_grid[r, :] = 3

    # Return the final output grid as a list of lists
    return output_grid.tolist()
```