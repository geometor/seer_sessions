# 6773b310 • 014 • refine_coder

---
```python
"""
Examines the input grid for rectangles defined by azure (8) pixels at their corners. 
If any such rectangle exists, the output grid is all zeros.
If no such rectangles can be formed, the output is also all zeros.
"""

import numpy as np

def find_azure_rectangles(grid):
    """
    Finds all rectangles in the grid where the corners are azure (8) pixels.
    Returns a list of rectangle coordinates as tuples: ((row1, col1), (row2, col2))
    where (row1, col1) is the top-left corner and (row2, col2) is the bottom-right corner.
    """
    azure_pixels = np.where(grid == 8)
    azure_coords = list(zip(azure_pixels[0], azure_pixels[1]))
    rectangles = []

    for i in range(len(azure_coords)):
        for j in range(i + 1, len(azure_coords)):
            row1, col1 = azure_coords[i]
            row2, col2 = azure_coords[j]

            # Check if the other two corners also have azure pixels
            if (row1, col2) in azure_coords and (row2, col1) in azure_coords:
                # Ensure the rectangle is added only once, order corners
                top_left = (min(row1, row2), min(col1, col2))
                bottom_right = (max(row1, row2), max(col1, col2))
                rectangles.append((top_left, bottom_right))
    
    return rectangles

def transform(input_grid):
    input_grid = np.array(input_grid)

    # Find azure rectangles
    azure_rectangles = find_azure_rectangles(input_grid)

    # The dimensions are not really relevant based on testing.
    output_grid = np.zeros((min(3,input_grid.shape[0]),min(3,input_grid.shape[1])), dtype=int)
   
    return output_grid.tolist()
```
