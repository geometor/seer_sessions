```python
import numpy as np

"""
Fill the rectangular bounding box of each distinct colored object in the input grid with its color to produce the output grid.

1. Initialize the output grid as a new grid of the same dimensions as the input, filled with the background color (white, 0).
2. Identify all unique non-white colors present in the input grid.
3. For each unique non-white color:
    a. Find all pixels in the input grid that have this color.
    b. Determine the minimum and maximum row and column indices (the bounding box) for these pixels.
    c. Fill the area within this bounding box in the output grid with the current color.
4. Return the final output grid.
"""

def find_colored_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color:
                pixels.append((r, c))
    return pixels

def get_bounding_box(pixels):
    """Calculates the bounding box (min_row, max_row, min_col, max_col) for a list of pixels."""
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid):
    """
    Transforms the input grid by finding the bounding box for each non-background color
    and filling that box with the respective color in the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(input_np)

    # Find all unique non-white colors in the input grid
    unique_colors = np.unique(input_np)
    non_white_colors = [color for color in unique_colors if color != 0]

    # Process each non-white color
    for color in non_white_colors:
        # Find all pixels of the current color
        pixels = find_colored_pixels(input_np, color)

        if pixels:
            # Calculate the bounding box for these pixels
            min_row, max_row, min_col, max_col = get_bounding_box(pixels)

            # Fill the bounding box in the output grid with the current color
            # Slicing is inclusive for the start index and exclusive for the end index,
            # so we add 1 to max_row and max_col.
            output_grid[min_row : max_row + 1, min_col : max_col + 1] = color

    return output_grid.tolist() # Return as a list of lists
```