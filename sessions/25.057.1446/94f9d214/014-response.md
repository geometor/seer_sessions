# 94f9d214 • 014 • example_3 • investigate_coder

---
```python
"""
1. **Halve the Height:** Divide the input grid into two equal halves vertically. Consider only the top half of the input grid (rows 1-4).
2. **Locate Green:** Within this top half, identify the locations (coordinates) of all green (3) pixels.
3. **Change to Red:** Replace each green pixel in the top half with a red (2) pixel.
4. **Fill Rest:** Fill the remaining pixels from the top half with white (0).
5. **Output:** The resulting 4x4 grid is the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # Get dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the height of the output grid (half of the input height)
    output_height = input_height // 2
    output_width = input_width

    # Initialize the output grid with all white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the top half of the input grid
    for row in range(output_height):
        for col in range(input_width):
            # Check if the pixel in the input grid is green (3)
            if input_grid[row, col] == 3:
                # Replace the corresponding pixel in the output grid with red (2)
                output_grid[row, col] = 2
            # else, it stays 0, which is handled on init

    return output_grid
```
