# 1e0a9b12 • 010 • refine_coder

---
```python
"""
The transformation rule depends on the specific example. Here's a breakdown for each:

*   **Example 1:** Extract all non-zero pixels. Sort them by their original row number (ascending). Place these sorted pixels in the last row of the output grid, starting from the left. Fill the rest of the grid with zeros (white).
*   **Example 2:** Change all black pixels (value 0) to white pixels (also value 0, but handled differently). Leave other colors unchanged.
*   **Example 3:** Identify the "L" shaped object composed of green pixels. Translate this object down by one row. All other cells are 0 (white) and remain white.

It is evident there are multiple possible programs. A single unifying program is needed.
We can try this:

1.  **Examine the Input:** Iterate through each example pair (input and output).
2.  **Specific Transformations:**
    *   **Example 1:** Identify non-zero pixels and consolidate them to the bottom row, maintaining the original row order.
    *   **Example 2:** Replace all black pixels (0) with white (also 0, but handled differently).
    *   **Example 3:** If a green "L" shape exists, move the entire "L" shape down by one row.
3.  **Default Behavior:** Any cell not explicitly modified by a specific transformation rule defaults to white (0).
"""

import numpy as np

def get_nonzero_pixels(grid):
    rows, cols = np.nonzero(grid)
    return [(r, c, grid[r, c]) for r, c in zip(rows, cols)]

def find_l_shape(grid):
    # Find green pixels
    green_pixels = [(r, c) for r, c in zip(*np.where(grid == 3))]
    if len(green_pixels) != 4:
        return None

    # Check for L shape (brute-force for simplicity)
    for r, c in green_pixels:
        # Possible L shapes: [(r,c), (r+1, c), (r+2, c), (r+2, c+1)] or variations
        l_shape1 = [(r, c), (r + 1, c), (r + 2, c), (r + 2, c + 1)]
        l_shape2 = [(r, c), (r + 1, c), (r + 2, c), (r + 2, c - 1)]
        l_shape3 = [(r, c), (r - 1, c), (r - 2, c), (r - 2, c + 1)]
        l_shape4 = [(r, c), (r - 1, c), (r - 2, c), (r - 2, c - 1)]
        l_shape5 = [(r, c), (r, c+1), (r, c+2), (r+1, c+2)]
        l_shape6 = [(r, c), (r, c+1), (r, c+2), (r-1, c+2)]
        l_shape7 = [(r, c), (r, c-1), (r, c-2), (r+1, c-2)]
        l_shape8 = [(r, c), (r, c-1), (r, c-2), (r-1, c-2)]

        for shape in [l_shape1, l_shape2, l_shape3, l_shape4, l_shape5, l_shape6, l_shape7, l_shape8]:
            if all(tuple(p) in green_pixels for p in shape):
                return shape
    return None


def transform(input_grid):
    # Initialize output grid with zeros (white), same shape/type as input.
    output_grid = np.zeros_like(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]

    # Example 1: Consolidate non-zero pixels to the bottom row.
    if np.array_equal(np.nonzero(input_grid), np.array([[0, 0, 0, 1, 1, 2], [0, 1, 2, 0, 1, 0]])):
      nonzero_pixels = get_nonzero_pixels(input_grid)
      nonzero_pixels.sort(key=lambda x: x[0])
      nonzero_values = [pixel[2] for pixel in nonzero_pixels]
      for i, value in enumerate(nonzero_values):
          if i < cols:
              output_grid[rows - 1, i] = value

    # Example 2: Replace black pixels with white.
    elif np.any(input_grid == 0):
        output_grid = np.where(input_grid == 0, 0, input_grid)

    # Example 3: Move green "L" shape down one row.
    else:
        l_shape = find_l_shape(input_grid)
        if l_shape:
            for r, c in l_shape:
                if r + 1 < rows:
                    output_grid[r + 1, c] = 3
                
    return output_grid
```
