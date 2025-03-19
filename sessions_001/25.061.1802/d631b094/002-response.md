# d631b094 • 002 • example_4 • investigate_coder

---
```python
"""
1. Identify all non-zero pixels within the input 3x3 grid.
2. Determine the color (numerical value) of the non-zero pixels. Note that within each input grid there is only ever a single color present.
3. Count the number of times this non-zero color appears in the input grid.
4. Create a new 1 x N output grid, where N is the count obtained in step 3.
5. Fill all cells of the output grid with the non-zero color value identified in step 2.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Find all non-zero pixels
    non_zero_pixels = input_array[input_array != 0]
    
    # If there are no non-zero pixels, return an empty grid (or a specific default value)
    if non_zero_pixels.size == 0:
        return [[]]  # Or return a default like [0]
    
    # Determine the color of the non-zero pixels (assuming all are the same color)
    color = non_zero_pixels[0]
    
    # Count the number of non-zero pixels
    count = non_zero_pixels.size
    
    # Create the output grid
    output_grid = np.full((1, count), color)

    return output_grid.tolist()
```
