# f25fbde4 • 008 • refine_coder

---
```python
"""
1.  **Locate Yellow Pixels:** Find all pixels in the input grid that are yellow (value 4).
2.  **Find Extents:** Determine the minimum and maximum row and column indices of these yellow pixels. This defines the bounding box of a rectangle.
3.  **Create Filled Rectangle:** Create a new grid where all pixels within the bounding box (inclusive) are set to yellow (value 4).
4.  **Crop (Optional):** Remove any rows or columns on the edges of the grid that consist entirely of white pixels (value 0). This step might not be necessary if the rectangle creation is precise.
"""

import numpy as np

def find_yellow_pixels(grid):
    # Find the coordinates of all yellow pixels.
    return np.argwhere(grid == 4)

def find_extents(yellow_pixels):
    # Find the minimum and maximum row/col indices.
    if len(yellow_pixels) == 0:
        return None, None, None, None  # Handle empty case
    min_row, min_col = np.min(yellow_pixels, axis=0)
    max_row, max_col = np.max(yellow_pixels, axis=0)
    return min_row, min_col, max_row, max_col

def create_filled_rectangle(extents, shape):
    # Create a grid filled with yellow within the extents.
    min_row, min_col, max_row, max_col = extents
    if min_row is None: # handle no yellow pixels
        return np.zeros(shape, dtype=int)
    
    grid = np.zeros(shape, dtype=int)
    grid[min_row:max_row+1, min_col:max_col+1] = 4
    return grid

def crop_grid(grid):
    # Crop empty (all zero) rows and cols - likely unnecessary.
    rows_to_keep = np.any(grid != 0, axis=1)
    cols_to_keep = np.any(grid != 0, axis=0)
    cropped_grid = grid[rows_to_keep][:, cols_to_keep]
    return cropped_grid

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find all yellow pixels.
    yellow_pixels = find_yellow_pixels(input_grid)

    # Find the extents (bounding box) of the yellow pixels.
    extents = find_extents(yellow_pixels)

    # Create a filled rectangle based on the extents.
    output_grid = create_filled_rectangle(extents, input_grid.shape)

    # Crop the grid (this might be redundant).
    # output_grid = crop_grid(output_grid)

    return output_grid
```

