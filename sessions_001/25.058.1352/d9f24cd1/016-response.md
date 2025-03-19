# d9f24cd1 • 016 • refine_coder

---
```python
"""
1. Identify and Preserve Gray: Locate all gray pixels (value 5) in the input grid. These pixels will remain unchanged in the output grid.
2. Identify Red Pixels: Locate all red pixels (value 2) in the input.
3. Column Fill:  For every red pixel, change all pixels in the same column to red.
4. Horizontal Spread (Gray Influence): Find all empty (value 0) pixels that are horizontally adjacent (left or right) to any gray pixel. Change these empty pixels to red. Continue this horizontal spread until no more horizontally adjacent empty pixels connected to the gray region exist.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify and Preserve Gray (Step 1)
    gray_pixels = np.where(input_grid == 5)
    # gray_pixels remain unchanged due to the copy

    # Identify Red Pixels (Step 2)
    red_pixels = np.where(input_grid == 2)

    # Column Fill (Step 3)
    for col in np.unique(red_pixels[1]):
        output_grid[:, col] = 2

    # Horizontal Spread (Gray Influence) (Step 4)
    while True:
        changed = False
        empty_adjacent_to_gray = []

        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 0: # Check if it's empty
                    # Check for horizontal adjacency to gray
                    if (c > 0 and output_grid[r, c-1] == 5) or \
                       (c < cols - 1 and output_grid[r, c+1] == 5):
                        empty_adjacent_to_gray.append((r, c))

        for r, c in empty_adjacent_to_gray:
            output_grid[r, c] = 2
            changed = True

        if not changed:
            break # Exit loop when no more changes occur

    return output_grid
```

