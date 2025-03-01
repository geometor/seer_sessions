# 952a094c • 014 • refine_coder

---
```python
"""
1.  **Identify the Changing Pixels:** Find the four pixels that have colors that are rearranged between the input and output grids. These four pixels will always form the corners of an axis-aligned rectangle (which may be a square).
2.  **Determine Rectangle Corners:**  The locations of these four pixels can be found by noting they form a rectangular shape. The colors themselves are distinct, but the key is finding two distinct rows and two distinct columns.
3.  **Cyclic Color Swap:** The colors of these four pixels are swapped in a clockwise cyclic permutation:
    *   The color at the top-left corner moves to the top-right corner.
    *   The color at the top-right corner moves to the bottom-right corner.
    *   The color at the bottom-right corner moves to the bottom-left corner.
    *   The color at the bottom-left corner moves to the top-left corner.
"""

import numpy as np

def find_changed_pixels(input_grid, output_grid):
    """Finds the coordinates of pixels that differ between two grids."""
    diff = input_grid != output_grid
    changed_pixels = np.argwhere(diff)
    return changed_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Create a dummy output grid for comparison
    dummy_output_grid = np.copy(input_grid)
    
    # Use a large grid for testing
    changed_pixels = find_changed_pixels(input_grid, dummy_output_grid)

    # Handle cases where there may be no changes at all or fewer than 4 changes
    if len(changed_pixels) != 4:
      return output_grid
        
    # Extract rows and cols of the changed pixels
    rows = [p[0] for p in changed_pixels]
    cols = [p[1] for p in changed_pixels]

    # Determine the unique rows and columns. This defines the rectangle.
    unique_rows = sorted(list(set(rows)))
    unique_cols = sorted(list(set(cols)))

    # Ensure we have exactly two unique rows and two unique columns
    if len(unique_rows) != 2 or len(unique_cols) != 2:
        return output_grid

    # Define the corners of the rectangle
    top_left = (unique_rows[0], unique_cols[0])
    top_right = (unique_rows[0], unique_cols[1])
    bottom_left = (unique_rows[1], unique_cols[0])
    bottom_right = (unique_rows[1], unique_cols[1])
        

    # Perform the clockwise cyclic color swap
    output_grid[top_right] = input_grid[top_left]
    output_grid[bottom_right] = input_grid[top_right]
    output_grid[bottom_left] = input_grid[bottom_right]
    output_grid[top_left] = input_grid[bottom_left]

    return output_grid
```
