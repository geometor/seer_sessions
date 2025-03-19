# f9012d9b • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Target Region:** Locate a 2x2 region within the input grid.
2.  **Extract:** extract this region in it's spatial arrangement.
3.  **Output the region:** The program takes this identified 2x2 region and creates it as output. It appears the location is a function of the location and arrangement of like colored pixels.
4. The upper left of the output grid is at row 0, column 2 of input.
"""

import numpy as np

def get_subgrid(grid, row_start, col_start, size):
    """Extracts a subgrid of specified size from the given grid."""
    return grid[row_start:row_start+size, col_start:col_start+size]

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    
    # The upper left of the output grid is at row 0, column 2 of input.
    output_grid = get_subgrid(input_grid, 0, 2, 2)
    
    return output_grid.tolist()
```
