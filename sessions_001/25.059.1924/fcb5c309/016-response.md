# fcb5c309 • 016 • example_3 • investigate_coder

---
```python
"""
1. **Identify Target Shape:** Locate all red (2) pixels within the input grid. Consider these pixels as forming the target shape.
2.  **Extract:** Isolate the target shape (red pixels) from other elements (green pixels and white background).
3.  **Reduce and Center:** Reduce the size of the extracted shape while approximately preserving its original form. Imagine finding a bounding box around the red pixels and shrinking it, keeping only internal parts.
4. **Create Output Grid**: Create a smaller, empty output grid with all white (0) values
5. **Transfer and set color:** Place the reduced red shape onto the output grid. Replace all non red values with white (0)
6. **Complete Output** The output grid is now complete, it contains the reduced and centered red pixels surrounded by white.
"""

import numpy as np

def get_bounding_box(grid, color):
    # Find coordinates of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle cases with no target color
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col), (max_row, max_col)

def extract_shape(grid, color):
    # Extract the shape defined by the specified color
    bbox = get_bounding_box(grid, color)
    if bbox is None:
      return np.zeros((0,0))
    (min_row, min_col), (max_row, max_col) = bbox
    return grid[min_row:max_row+1, min_col:max_col+1]
    

def reduce_and_center_shape(shape):
    # Reduce the shape and center it - the tricky part, simplification for this iteration
    height, width = shape.shape
    
    # Find rows and cols with red pixels
    red_rows = np.any(shape == 2, axis=1)
    red_cols = np.any(shape == 2, axis=0)

    # Extract the core by removing empty rows/cols at edges
    cropped_shape = shape[red_rows][:, red_cols]  #Boolean indexing

    cropped_height, cropped_width = cropped_shape.shape
    
    # Create a new output grid, targeting approximately 7x7, adjust if necessary
    out_height, out_width = 7, 7
    output_grid = np.zeros((out_height, out_width), dtype=int)

    #Calculate start position to center
    start_row = max(0, (out_height - cropped_height) // 2)
    start_col = max(0, (out_width - cropped_width) // 2)
        
    #Copy the cropped shape
    for r in range(min(cropped_height, out_height)):
      for c in range(min(cropped_width, out_width)):
        output_grid[start_row + r, start_col + c] = cropped_shape[r,c]

    return output_grid

def replace_non_red(grid, red_value=2, other_value=0):
    # replaces any value that is not red with the other value
    
    reds = (grid == red_value)
    grid = np.where(reds, red_value, other_value)

    return grid

def transform(input_grid):
    """
    Transforms the input grid by extracting, reducing, and centering the red shape.
    """
    # Extract red shape
    extracted_red_shape = extract_shape(input_grid, 2)

    # Reduce and center the extracted shape
    reduced_shape = reduce_and_center_shape(extracted_red_shape)

    # replace remaining non-red with 0
    output_grid = replace_non_red(reduced_shape)
    
    return output_grid
```
