```python
"""
The function identifies all non-zero (non-white) pixels in the input grid and
reconstructs them in a dense, square-like output grid. The dimensions of the
output grid depend on the total number of non-white pixels, effectively
repeating those pixels the number of times the color is present.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Identify non-zero pixels
    non_zero_pixels = input_grid[input_grid != 0]

    # Count the occurrences of each non-zero color
    color_counts = {}
    for color in non_zero_pixels:
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1

    # Create the output grid by repeating each color based on its count
    output_list = []
    for color, count in color_counts.items():
        output_list.extend([color] * count)
            
    output_grid = np.array(output_list)

    return output_grid.tolist()
```