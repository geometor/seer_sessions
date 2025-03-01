# 88a62173 • 002 • example_3 • investigate_coder

---
```python
"""
Extracts a 2x2 grid from a 5x5 input grid based on a specific pattern. The pattern involves identifying two alternating colors (one being white/0) and extracting a 2x2 representation where the top-left, top-right, bottom-right, and bottom-left values form a spiral clockwise pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 5x5 input grid into a 2x2 output grid.
    """
    input_array = np.array(input_grid)
    output_array = np.zeros((2, 2), dtype=int)

    # Identify the two distinct colors.
    unique_colors = np.unique(input_array)
    non_zero_color = unique_colors[unique_colors != 0][0]

    # Extract the relevant elements to form the output.
    output_array[0, 0] = input_array[0, 0] if input_array[0,0] != 0 else input_array[0,1]
    output_array[0, 1] = input_array[0, 3] if input_array[0,3] != 0 else input_array[1,3]
    output_array[1, 0] = input_array[3, 0] if input_array[3,0] != 0 else input_array[3,1]
    output_array[1, 1] = input_array[3, 3] if input_array[3,3] != 0 else input_array[4,3]
    
    return output_array.tolist()
```
