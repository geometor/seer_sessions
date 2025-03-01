"""
1.  **Identify Gray Pixels:** Locate all gray (5) pixels in the input grid. Copy these directly to the output grid, maintaining their positions.
2.  **Identify Connected Green Objects:** Find all connected regions of green (3) pixels in the input grid. Treat each connected region as a single object.
3.  **Expand Green Objects:** For *each* connected green object, expand its boundary outwards by one pixel. This creates a one-pixel-wide green outline *around* the original location of the green object. The interior of the original green region is *not* filled with green in the output.
4.  **Background:** The background remains white (0) - any location not covered by gray pixels or the expanded green outline will be white.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def get_pixels_by_color(grid, color):
    """Returns coordinates of all pixels of the specified color."""
    return np.argwhere(grid == color)

def expand_object_boundary(grid, object_pixels):
    """Expands the boundary of a single object (list of pixels)."""
    expanded_pixels = set()
    rows, cols = grid.shape
    for r, c in object_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the original pixel
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    expanded_pixels.add((nr, nc))
    return list(expanded_pixels)

def transform(input_grid):
    # Initialize output_grid as all white (0)
    output_grid = np.zeros_like(input_grid)

    # Copy gray pixels to output_grid
    gray_pixels = get_pixels_by_color(input_grid, 5)
    for r, c in gray_pixels:
        output_grid[r, c] = 5

    # Find connected green objects
    green_pixels = get_pixels_by_color(input_grid, 3)
    green_mask = (input_grid == 3).astype(int)  # Create a binary mask for labeling
    labeled_mask, num_labels = label(green_mask)

    # Expand each green object and draw the outline
    for i in range(1, num_labels + 1):  # Label 0 is background
        object_pixels = np.argwhere(labeled_mask == i)
        expanded_boundary = expand_object_boundary(input_grid, object_pixels)

        # Draw only the expanded boundary (outline)
        for r, c in expanded_boundary:
            # this is key - test expanded pixel is not part of original green
            # object
            if (r,c) not in [tuple(pixel) for pixel in object_pixels]:
               output_grid[r,c] = 3

    return output_grid