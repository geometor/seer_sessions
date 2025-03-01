# 39a8645d • 006 • example_1 • investigate_coder

---
```python
"""
The output grid is a 3x3 representation where each cell corresponds to approximately a section of the original image. An azure pixel is present in the output if the relative section contained one or more azure pixels. Red pixels in the input are disregarded.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to a 3x3 output grid representing the presence of azure clusters.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Define section boundaries.
    row_sections = [rows // 3, 2 * rows // 3, rows]
    col_sections = [cols // 3, 2 * cols // 3, cols]

    # Iterate through each section
    for i in range(3):
        for j in range(3):
            # Calculate section boundaries
            row_start = (rows // 3) * i
            row_end = row_sections[i]
            col_start = (cols//3) * j
            col_end = col_sections[j]

            # Extract the section from the input grid.
            section = input_grid[row_start:row_end, col_start:col_end]

            # Check for the presence of azure (8) pixels in the section.
            if 8 in section:
                output_grid[i, j] = 8

    return output_grid.tolist()
```
