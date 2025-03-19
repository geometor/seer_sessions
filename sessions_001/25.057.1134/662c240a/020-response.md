# 662c240a • 020 • example_4 • investigate_coder

---
```python
"""
The input grid is vertically divided into three equal sections. Each section is extracted to form the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid (it will just be a subset of input in this case so no need)
    input_grid = np.array(input_grid)
    height = input_grid.shape[0]
    subgrid_height = height // 3
    
    # Extract the first subgrid (rows 0-2)
    output_grid = input_grid[0:subgrid_height, :]

    return output_grid.tolist()
```
