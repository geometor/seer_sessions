# ed36ccf7 • 020 • example_4 • investigate_coder

---
```python
"""
The output is created by rotating the input 90 degrees clockwise, while maintaining the positions of all white pixels (0).
"""

import numpy as np

def rotate_grid_90_clockwise(grid):
    return np.rot90(grid, k=-1)

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise, preserving white pixels.
    """
    # Convert input_grid to a NumPy array
    input_np = np.array(input_grid)

    # Create a copy of the input to store white pixel positions
    output_grid = np.copy(input_np)
    
    #rotate the entire grid
    rotated_grid = rotate_grid_90_clockwise(input_np)

    # Iterate and place rotated non-white pixel in output if they were not white
    for i in range(input_np.shape[0]):
      for j in range(input_np.shape[1]):
        if input_np[i,j] != 0:
          output_grid[i,j] = rotated_grid[i,j]

    return output_grid.tolist()
```
