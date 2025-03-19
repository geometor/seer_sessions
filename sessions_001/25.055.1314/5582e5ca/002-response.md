# 5582e5ca • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to identify the most frequent color in the top-left 2x2 subgrid of the input grid and then create an output grid of the same dimensions where every cell is filled with that dominant color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling the output grid with the most frequent color
    found in the top-left 2x2 subgrid of the input.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Extract the top-left 2x2 subgrid
    subgrid = input_array[:2, :2]
    
    # Find the most frequent color in the subgrid
    unique, counts = np.unique(subgrid, return_counts=True)
    most_frequent_color = unique[np.argmax(counts)]
    
    # Create an output grid of the same dimensions, filled with the most frequent color
    output_grid = np.full(input_array.shape, most_frequent_color)
    
    return output_grid.tolist()
```
