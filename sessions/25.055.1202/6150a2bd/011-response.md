# 6150a2bd • 011 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous blocks of pixels of the same color. Each of these blocks is an object.
2.  **Find Single Pixel Objects**: From all objects, check if is there any object that consists of only one pixel.
3.  **Move Single Pixel Objects**:
   *   If a single-pixel object exists at the bottom-left corner, move it to the top-right corner.
   *    If a single-pixel object exists at the bottom-right corner, move it to the bottom-left corner.
4.  **Preserve Other Objects:** All other objects (non-single-pixel objects) remain unchanged in their original positions and colors.
"""

from skimage import measure
import numpy as np

def find_objects(grid):
    # Find all contiguous blocks of pixels of the same color.
    arr = np.array(grid)
    unique_colors = np.unique(arr)
    objects = []
    for color in unique_colors:
        color_arr = (arr == color).astype(int)
        labeled_arr, num_labels = measure.label(color_arr, connectivity=1, return_num=True)
        for i in range(1, num_labels + 1):
            objects.append(labeled_arr == i)
    return objects

def is_single_pixel_object(obj):
    # check if the object is single pixel
    return np.sum(obj) == 1

def get_object_position(obj):
    # Get the (row, col) position of a single-pixel object.
    rows, cols = np.where(obj)
    return rows[0], cols[0]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid).tolist()
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]

    # Find all objects
    objects = find_objects(input_grid)

    # Find and move single-pixel objects
    for obj in objects:
        if is_single_pixel_object(obj):
            row, col = get_object_position(obj)
            color = input_grid[row, col]
            # Move single-pixel objects based on their position.
            if row == rows - 1 and col == 0:  # Bottom-left corner
                output_grid[row][col] = input_grid[0][0] # change the original pixel to the color of top-left
                output_grid[0][cols - 1] = color # Top-right corner
            elif row == rows - 1 and col == cols - 1:  # Bottom-right corner
                output_grid[row][col] = input_grid[0][0] # change the original pixel to the color of top-left
                output_grid[rows - 1][0] = color # Bottom-left corner
    return output_grid
```
