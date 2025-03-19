# 995c5fa3 • 014 • refine_coder

---
```python
"""
Divides the input grid into nine equal sections.
For each section, it checks if all pixels are 0.
The output grid's corresponding cell value is based on pre-defined mapping,
with conditional changes based on the presence of non-zero pixels in sections 1, 7, and 8.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Define section boundaries dynamically
    section_width = input_width // 3
    section_height = input_height // 3

    # Define output mapping: section_index -> color
    output_mapping = {
        1: 4,
        2: 4,
        3: 4,
        4: 4,
        5: 4,
        6: 4,
        7: 3,
        8: 3,
        9: 3,
    }
    
    # Check section 1 for non-zero pixels
    row_start = 0
    row_end = section_height
    col_start = 0
    col_end = section_width
    section1 = input_grid[row_start:row_end, col_start:col_end]
    if np.any(section1):
        output_mapping[1] = 3

    # Check sections 7 and 8 for non-zero pixels
    for i in [6, 7]:  # Section indices 7 and 8 (0-indexed)
        row_index = (i) // 3
        col_index = (i) % 3
        row_start = row_index * section_height
        row_end = row_start + section_height
        col_start = col_index * section_width
        col_end = col_start + section_width
        section = input_grid[row_start:row_end, col_start:col_end]
        if np.any(section):
            output_mapping[i + 1] = 2

    # Process each section and populate output grid
    for i in range(9):
        row_index = (i) // 3
        col_index = (i) % 3
        output_grid[row_index, col_index] = output_mapping.get(i + 1, 0)


    return output_grid.tolist()
```
