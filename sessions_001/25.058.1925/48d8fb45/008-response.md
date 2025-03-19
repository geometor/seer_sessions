# 48d8fb45 • 008 • refine_coder

---
```python
"""
1.  **Create Output Grid:** Create a 3x3 output grid filled with black (0) pixels.
2.  **Identify the Output Color**: Examine the colors present in the input grid. The color of the single pixel at the center of the output will be one of the non-black colors present in the *input grid*.
3. **Select Input Pixel**: The first non-black pixel present in the input will become the color of the center pixel in the output.
4.  **Place Color:** Place a single pixel of the identified color at the center of the 3x3 output grid (row 1, column 1).
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid with all zeros (black)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the first non-black pixel color in the input grid
    rows, cols = input_grid.shape
    output_color = 0  # Default to black if no non-black pixel is found
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                output_color = input_grid[r, c]
                break  # Stop after finding the first non-black pixel
        if output_color != 0:
            break

    # Place the identified color at the center of the output grid
    output_grid[1, 1] = output_color

    return output_grid
```

