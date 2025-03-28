```python
"""
Draws vertical and horizontal lines extending from each non-white pixel 
to the nearest corresponding grid edge. The lines take the color of the 
source pixel. If a pixel is equidistant between two opposing edges, 
the line extends towards the top or left edge.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by drawing lines from non-white pixels.

    Args:
        input_grid (list[list[int]]): The input grid represented as a 2D list.

    Returns:
        list[list[int]]: The transformed grid as a 2D list.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    
    # Get grid dimensions
    height, width = grid.shape

    # Find the locations and colors of all non-white source pixels
    source_pixels = []
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                source_pixels.append({'row': r, 'col': c, 'color': color})

    # Process each source pixel
    for pixel_info in source_pixels:
        r, c, color = pixel_info['row'], pixel_info['col'], pixel_info['color']

        # --- Vertical Line Drawing ---
        # Calculate distances to top and bottom edges
        dist_top = r
        dist_bottom = height - 1 - r

        # Determine vertical direction and draw line
        if dist_top <= dist_bottom:
            # Draw line upwards from row 0 to the pixel's row (inclusive)
            output_grid[0 : r + 1, c] = color
        else:
            # Draw line downwards from the pixel's row to the bottom row (inclusive)
            output_grid[r : height, c] = color

        # --- Horizontal Line Drawing ---
        # Calculate distances to left and right edges
        dist_left = c
        dist_right = width - 1 - c

        # Determine horizontal direction and draw line
        if dist_left <= dist_right:
            # Draw line leftwards from column 0 to the pixel's column (inclusive)
            output_grid[r, 0 : c + 1] = color
        else:
            # Draw line rightwards from the pixel's column to the rightmost column (inclusive)
            output_grid[r, c : width] = color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```