# 234bbc79 • 024 • refine_coder

---
```python
"""
1.  **Identify and Remove:** Identify all pixels with the color gray (5) and remove them from the grid.
2. **Retain and Count:** Keep all pixels of color blue (1) and red (2), and keep track of how many exist of each in each row.
3.  **Arrange:** In the output grid, within each row, place all blue pixels (if any) to the left of all red pixels (if any). Fill any remaining cells in the row with black(0). The height and width of the grid are dynamic, based on the occurrences of colors 1 and 2.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Identify and remove gray pixels, retain and count blue and red.
    filtered_pixels = []
    for r in range(rows):
        row_pixels = []
        for c in range(cols):
            if input_grid[r, c] != 5:
                row_pixels.append(input_grid[r, c])
        filtered_pixels.append(row_pixels)

    # Determine output grid dimensions.
    max_width = 0
    for row in filtered_pixels:
        max_width = max(max_width, len(row))
    output_rows = len(filtered_pixels)

    output_grid = np.zeros((output_rows, max_width), dtype=int)
    
    # Arrange pixels in output grid: blue to the left of red.
    for r, row_pixels in enumerate(filtered_pixels):
        blue_pixels = [p for p in row_pixels if p == 1]
        red_pixels = [p for p in row_pixels if p == 2]
        new_row = blue_pixels + red_pixels
        output_grid[r, :len(new_row)] = new_row

    return output_grid.tolist()
```
