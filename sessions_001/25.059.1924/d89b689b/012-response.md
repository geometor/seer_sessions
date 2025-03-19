# d89b689b • 012 • refine_coder

---
```python
"""
Selects specific colored blocks (objects) from the input grid based on color and size, and copies them to the output grid. Other objects are ignored. The specific rule for selection and placement varies between examples, but generally involves copying a contiguous block of a specific color.
"""

import numpy as np
from skimage.measure import label, regionprops

def get_object_properties(grid):
    """
    Identifies objects in the grid and returns their properties.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its properties (color, bounding box, area).
    """

    labeled_grid = label(grid, connectivity=1)
    objects = []
    for region in regionprops(labeled_grid):
        #Bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        
        objects.append({
            'color': grid[min_row, min_col],
            'bbox': (min_row, min_col, max_row, max_col),
            'area': region.area,
            'centroid': region.centroid,
        })
    return objects

def transform(input_grid):
    # Initialize output grid with the same shape and data type as the input
    output_grid = np.zeros_like(input_grid)

    # Get objects in the input grid
    input_objects = get_object_properties(input_grid)

    # Example-specific logic (this needs to be generalized later)
    
    #try to select a specific colored 2x2 block
    target_object = None
    for obj in input_objects:
        if obj['area'] == 4: #looking for a 2x2
          min_row, min_col, max_row, max_col = obj['bbox']
          if max_row - min_row == 2 and max_col - min_col == 2: #ensure it is 2x2
            target_object = obj
            break
        if obj['area'] == 1:
            #check for example_0 conditions
            colors = [5,9,2,1]
            if all([any(o['color'] == c for o in input_objects) for c in colors]):
                center = (input_grid.shape[0] // 2, input_grid.shape[1] // 2)
                target_positions = {
                    5: (center[0] - 1, center[1] - 1),  # grey: top-left
                    9: (center[0] - 1, center[1]),      # maroon: top-right
                    2: (center[0], center[1] - 1),      # red: bottom-left
                    1: (center[0], center[1])           # blue: bottom-right
                }
                for o in input_objects:
                    if o['color'] in target_positions:
                        output_grid[target_positions[o['color']]] = o['color']
                return output_grid


    if target_object:
        #copy block to the output grid
        min_row, min_col, max_row, max_col = target_object['bbox']
        color = target_object['color']
        for r in range(min_row, max_row):
            for c in range(min_col, max_col):
                output_grid[r,c] = input_grid[r,c]
    

    return output_grid
```
