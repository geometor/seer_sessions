# fcb5c309 • 018 • refine_coder

---
```python
"""
1. **Identify Target:** Find all pixels of the target color (red, denoted as 2) within the input grid.
2. **Check for Target Presence:** If no pixels of the target color are found, return an output grid that matches the input grid size and is entirely filled with the background color (white, denoted as 0).
3. **Bounding Box:** If target color pixels are present, determine the bounding box around the target pixels.
4. **Extract Target Object**: Create new grid using the bounding box.
5. **Reduce:** Create an output grid where the dimensions are equal to the dimensions of the extracted grid from the previous step.
6. **Transfer and set color**: Copy the extracted grid to the output grid.
7. **Replace non target:** Replace all non-target color pixels in the output grid with the background color (white, 0).
"""

import numpy as np

def get_bounding_box(grid, target_color):
    """
    Finds the bounding box of the target color in the grid.
    Returns None if no target color is found.
    """
    coords = np.argwhere(grid == target_color)
    if coords.size == 0:
        return None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col), (max_row, max_col)

def extract_object(grid, target_color):
    """
    Extracts the object defined by the target color.
    Returns an empty array if no target color pixels are present.
    """
    bbox = get_bounding_box(grid, target_color)
    if bbox is None:
        return np.zeros((0, 0), dtype=int)  # Return an empty array
    (min_row, min_col), (max_row, max_col) = bbox
    return grid[min_row:max_row+1, min_col:max_col+1]

def replace_non_target(grid, target_color, background_color):
    """
    Replaces all pixels in the grid that are not the target color with the background color.
    """
    return np.where(grid == target_color, target_color, background_color)

def transform(input_grid):
    """
    Transforms the input grid by extracting, reducing, and centering a target color (red) shape.
    """
    target_color = 2  # Red
    background_color = 0  # White
    
    # Check for Target Presence
    if not np.any(input_grid == target_color):
        return np.full(input_grid.shape, background_color, dtype=int)
    
    # Extract Target Object
    extracted_object = extract_object(input_grid, target_color)

    # Reduce/Transfer: Output grid has same dimensions as extracted object
    output_grid = np.copy(extracted_object)

    # Replace Non-Target
    output_grid = replace_non_target(output_grid, target_color, background_color)

    return output_grid
```
