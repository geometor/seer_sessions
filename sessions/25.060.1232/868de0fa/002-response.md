# 868de0fa • 002 • example_5 • investigate_coder

---
```python
"""
1. **Identify Blue Shapes:** Scan the input grid and identify all connected components of blue (1) pixels. These are the "blue shapes."

2. **Check for Closure:** For each identified blue shape, determine if it forms a closed boundary. A closed boundary completely encloses an internal region. There may be complex, nested closed shapes, each should be identified as separate objects and actions.

3. **Fill Enclosed Regions:** If a blue shape is closed, change the color of all pixels *inside* the enclosed region to red (2).

4. **Fill open blue shapes:** If a blue shape is open, change the color of all pixels of the open blue shape to orange (7).

5. **Output:** The output grid reflects these color changes, with other pixels retaining their original colors.
"""

import numpy as np
from scipy.ndimage import label, measurements

def get_objects(grid, color):
    """
    Identify connected components of a specific color in the grid.
    
    Parameters:
        grid (np.array): input grid
        color (int): color to identify
    
    Return:
        labeled_array (np.array): array with labeled objects, where different connected components of given color have different integer label
        num_objects (int): number of identified objects
    """
    mask = (grid == color).astype(int)
    labeled_array, num_objects = label(mask)
    return labeled_array, num_objects

def is_closed(grid, labeled_grid, object_label):
    """
    Check if object with an object_label in the labeled_grid is closed
    """
    # Extract the object's region.
    object_pixels = (labeled_grid == object_label)

    # Get bounding box coordinates
    coords = np.where(object_pixels)
    min_row, max_row = min(coords[0]), max(coords[0])
    min_col, max_col = min(coords[1]), max(coords[1])
    
    # Add a one-pixel border of zeros around the original grid for boundary checking
    padded_grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
    padded_object_pixels = np.pad(object_pixels, pad_width=1, mode='constant', constant_values=0)

    # Check for boundary intersection:
    # Create a mask for the object within the bounding box + 1
    object_mask = padded_object_pixels[min_row:max_row+3, min_col:max_col+3]
    object_region = padded_grid[min_row:max_row+3, min_col:max_col+3] * object_mask
    
    # If any non-blue(1) or 0 pixel are present along the expanded boundary, the shape is not closed
    rows, cols = object_region.shape
    for r in range(rows):
        if object_region[r, 0] != 1 and object_region[r, 0] != 0:
            return False
        if object_region[r, cols-1] != 1 and object_region[r, cols-1] != 0:
            return False            
    for c in range(cols):
        if object_region[0, c] != 1 and object_region[0, c] != 0:
            return False
        if object_region[rows-1, c] != 1 and object_region[rows-1, c] != 0:
                return False

    # Flood fill from the outside of the padded grid.  
    filled = padded_grid.copy()
    h, w = filled.shape
    stack = [(0,0)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < h and 0 <= c < w and filled[r, c] == 0:
            filled[r,c] = -1 # mark as visited
            stack.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])
            
    # If any pixels of value 0 remain inside the object mask region, the shape is closed
    object_region_in_filled = filled[min_row:max_row+3, min_col:max_col+3]
    if np.any((object_region_in_filled == 0) & (object_mask)):
        return True
    return False

def fill_enclosed(output_grid, labeled_grid, object_label, fill_color):
    """Fill the interior of a closed shape."""
    object_pixels = (labeled_grid == object_label)
    # Find boundary
    coords = np.where(object_pixels)
    min_row, max_row = min(coords[0]), max(coords[0])
    min_col, max_col = min(coords[1]), max(coords[1])

    # Add a one-pixel border of zeros
    padded_grid = np.pad(output_grid, pad_width=1, mode='constant', constant_values=0)
    padded_object_pixels = np.pad(object_pixels, pad_width=1, mode='constant', constant_values=0)    
    
    # Flood fill from the outside of the padded grid.  
    filled = padded_grid.copy()
    h, w = filled.shape
    stack = [(0,0)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < h and 0 <= c < w and filled[r, c] == 0:
            filled[r,c] = -1 # mark as visited
            stack.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])
            
    # Fill all 0 pixels inside the object mask region with fill color
    object_region_in_filled = filled[min_row:max_row+3, min_col:max_col+3]
    object_mask = padded_object_pixels[min_row:max_row+3, min_col:max_col+3]

    object_region_in_filled[(object_region_in_filled == 0) & (object_mask)] = fill_color
    
    filled[min_row:max_row+3, min_col:max_col+3] = object_region_in_filled
    
    # Remove padding
    output_grid[:,:] = filled[1:-1, 1:-1]
    
    return output_grid
    

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    labeled_grid, num_objects = get_objects(input_grid, 1)  # Find blue shapes

    for i in range(1, num_objects + 1):
        if is_closed(input_grid, labeled_grid, i):
            # Fill the closed shape's interior with red (2)
            output_grid = fill_enclosed(output_grid, labeled_grid, i, 2)
        else:
            # Fill open shapes with orange
            output_grid[labeled_grid == i] = 7
    return output_grid
```
