# dc0a314f • 006 • refine_coder

---
```python
"""
Extracts a sub-grid from the input grid. The sub-grid corresponds to the smallest
rectangular region enclosing a contiguous object of a single color within the input.
The size of output is same as the target object.
"""

import numpy as np

def find_smallest_bounding_object(input_grid):
    """
    Finds the smallest bounding box enclosing a single-color object.
    Prioritizes inner objects if multiple objects exist.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1
    target_color = None

    # Iterate through the grid to find potential target pixels
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            
            # Check for contiguity and update bounding box
            is_contiguous = False
            if r > 0 and input_grid[r-1, c] == color:
                is_contiguous = True
            if r < rows - 1 and input_grid[r+1, c] == color:
                is_contiguous=True
            if c > 0 and input_grid[r, c-1] == color:
                is_contiguous = True
            if c < cols - 1 and input_grid[r, c+1] == color:
                is_contiguous = True
                
            if is_contiguous:
                if target_color is None:
                    target_color = color

                if target_color == color: #only update if the contiguous object has the same color
                    min_row = min(min_row, r)
                    min_col = min(min_col, c)
                    max_row = max(max_row, r)
                    max_col = max(max_col, c)

    if target_color is None:
        return None  # No object found

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid by extracting the smallest bounding box 
    enclosing a single-color contiguous object.
    """
    bounding_box = find_smallest_bounding_object(input_grid)
    
    if bounding_box is None:
      return None # Or some other default/error handling.
      
    min_row, min_col, max_row, max_col = bounding_box

    # Extract the sub-grid
    output_grid = np.array(input_grid)[min_row:max_row + 1, min_col:max_col + 1]

    return output_grid.tolist() # Convert back to list
```
