# cdecee7f • 002 • example_3 • investigate_coder

---
```python
"""
1. **Extract:** Scan the input grid (10x10) and identify all non-zero (colored) pixels.  Record the color value and original (x, y) coordinates of each.
2. **Sort:** Sort the extracted colored pixels. It appears as though the sorting is first by the `y` and then by `x` coordinates, so pixels are effectively extracted in reading order (left-to-right, then top-to-bottom).
3. **Arrange:** Create a 3x3 output grid. Place the sorted colored pixels into the 3x3 grid. The placement follows row-major order (filling the first row from left to right, then the second row, and finally the third row, skipping a cell if a row in input does not have enough pixels.).
4. **Fill Remaining:**  Any remaining cells in the 3x3 grid that weren't filled with a colored pixel are set to 0, or kept empty.
"""

import numpy as np

def extract_colored_pixels(grid):
    """Extracts non-zero pixels and their coordinates."""
    colored_pixels = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] != 0:
                colored_pixels.append((grid[y, x], y, x))
    return colored_pixels

def sort_pixels(pixels):
    """Sorts pixels by y and then x coordinate."""
    return sorted(pixels, key=lambda p: (p[1], p[2]))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Extract non-zero pixels and their coordinates
    colored_pixels = extract_colored_pixels(input_grid)

    # Sort pixels by their original y and x coordinates
    sorted_pixels = sort_pixels(colored_pixels)

    # Arrange pixels into the 3x3 grid
    for i, (color, _, _) in enumerate(sorted_pixels):
        if i < 9:  # Ensure we don't go out of bounds
            row = i // 3
            col = i % 3
            output_grid[row, col] = color

    return output_grid
```
