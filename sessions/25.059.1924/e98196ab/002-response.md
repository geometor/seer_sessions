# e98196ab • 002 • example_3 • investigate_coder

---
```python
"""
Copy the top section of the input grid to the output. 
Remove the solid gray row. 
Copy rows from the bottom section that contain non-zero elements to the output, placing them after the top section.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    
    # Find the solid gray row (all 5s)
    gray_row_index = -1
    for i, row in enumerate(input_grid):
        if np.all(row == 5):
            gray_row_index = i
            break

    # Divide the grid into top, middle, and bottom sections
    top_section = input_grid[:gray_row_index]
    bottom_section = input_grid[gray_row_index + 1:]

    # Filter bottom section rows, keeping only rows with non-zero elements
    filtered_bottom_rows = []
    for row in bottom_section:
        if np.any(row != 0):
            filtered_bottom_rows.append(row)
   
    # Combine top and filtered bottom sections
    output_grid = np.vstack([top_section, filtered_bottom_rows]) if len(filtered_bottom_rows)>0 else top_section
    
    return output_grid.tolist()
```
