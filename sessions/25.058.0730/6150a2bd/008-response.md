# 6150a2bd • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule is a 180-degree rotation of the input grid. The non-white pixels in the input grid are rotated 180 degrees, and the output grid is constructed by placing these rotated pixels in their new positions while keeping their original colors, with the white pixels at their respective location..
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees, maintaining pixel values.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    height, width = input_array.shape

    # Initialize the output grid with zeros
    output_array = np.zeros_like(input_array)

    # Iterate through the input grid
    for r in range(height):
        for c in range(width):
            # Calculate the new position after 180-degree rotation
            new_r = height - 1 - r
            new_c = width - 1 - c

            # Copy the pixel value to the new position in the output grid
            output_array[new_r, new_c] = input_array[r, c]

    return output_array.tolist()
```
