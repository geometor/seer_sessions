# c8cbb738 • 014 • refine_coder

---
```python
"""
1. Identify the Background: Find the most frequent color in the input grid. This is the background color.
2. Find the Object: Identify the connected region (object) of pixels that are *not* the background color.
3. Locate the Object's Center: Calculate the center of mass of this region. Round the row and column of the center of mass to the nearest whole number. This gives the center pixel coordinates.
4. Extract 3x3 Subgrid: Extract the 3x3 subgrid centered at the calculated center coordinates.
5. Handle Edge Cases: If the 3x3 subgrid extends beyond the boundaries of the input grid, pad the missing cells with the background color.
"""

import numpy as np
from scipy.ndimage import label, center_of_mass

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    values, counts = np.unique(grid, return_counts=True)
    return values[np.argmax(counts)]

def find_object_center(grid, background_color):
    """Finds the center of the object, handling cases with no object."""
    non_background_mask = grid != background_color
    labeled_array, num_features = label(non_background_mask)
    
    if num_features > 0:
        center = center_of_mass(non_background_mask)
        return int(round(center[0])), int(round(center[1]))
    else:
        return None

def extract_subgrid(grid, center, background_color):
    """Extracts a 3x3 subgrid centered at the given coordinates, padding if necessary."""
    rows, cols = grid.shape
    if center is None:
      return np.full((3,3), background_color)
    
    center_row, center_col = center
    start_row = max(0, center_row - 1)
    end_row = min(rows, center_row + 2)
    start_col = max(0, center_col - 1)
    end_col = min(cols, center_col + 2)

    extracted_grid = grid[start_row:end_row, start_col:end_col]

    if extracted_grid.shape != (3, 3):
        padded_grid = np.full((3, 3), background_color)
        pr_start_row = max(0, 1 - center_row)
        pr_end_row = min(3, rows + (2 - center_row))
        pc_start_col = max(0, 1 - center_col)
        pc_end_col = min(3, cols + (2-center_col))
        padded_grid[pr_start_row:pr_end_row, pc_start_col:pc_end_col] = extracted_grid
        return padded_grid

    return extracted_grid

def transform(input_grid):
    """Transforms the input grid to the output grid based on object centering."""
    input_grid = np.array(input_grid)

    # Find the background color.
    background_color = find_background_color(input_grid)

    # Find the center of the object.
    center = find_object_center(input_grid, background_color)

    # Extract the 3x3 subgrid centered on the object, or a zero-filled grid if no object.
    output_grid = extract_subgrid(input_grid, center, background_color)
    
    return output_grid.tolist()
```
