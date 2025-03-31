```python
"""
Identify the background color (most frequent color). Iterate through each pixel.
If a pixel is not the background color, check its four cardinal neighbors (up, down, left, right).
If none of the cardinal neighbors have the same color as the pixel, change the pixel's color to the background color in the output grid.
Otherwise, keep the pixel's original color.
"""

import numpy as np
from collections import Counter

def _get_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    # Find the color with the highest count
    background_color = counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Transforms the input grid by removing pixels from colored objects that
    lack cardinal neighbors of the same color.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)

    # Determine the background color
    background_color = _get_background_color(grid)

    # Define cardinal neighbor offsets (row, col)
    cardinal_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            current_color = grid[r, c]

            # Skip if the current pixel is already the background color
            if current_color == background_color:
                continue

            # Count cardinal neighbors with the same color
            same_color_neighbor_count = 0
            for dr, dc in cardinal_neighbors:
                nr, nc = r + dr, c + dc

                # Check if neighbor is within grid boundaries
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if neighbor has the same color
                    if grid[nr, nc] == current_color:
                        same_color_neighbor_count += 1
                        # Optimization: If we find one, we know it won't be removed
                        break 

            # If no cardinal neighbors have the same color, change pixel to background color in output
            if same_color_neighbor_count == 0:
                output_grid[r, c] = background_color

    # Convert back to list of lists if necessary, though numpy array is often preferred
    return output_grid.tolist()
```