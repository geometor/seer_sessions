# d22278a0 • 026 • refine_coder

---
```python
"""
1.  **Identify Seed Pixels:** Find all non-white (non-zero) pixels in the input grid. These are the "seed" pixels.
2.  **Expand Seeds:** Each seed pixel expands its color outward based on these rules:
    *   **Blue (1):** Expands one step to the right, and down, and diagonally down/right until it hits a boundary or another color.
    *   **Red (2):** Expands one step to the left, and down, and diagonally down/left, until it hits a boundary or another color.
    *   **Azure (8):** Expands one step up, right, and diagonally up-right. Expansion stops when encountering another color or grid boundary. The azure pixel also fills the empty spaces directly up and right of itself, and diagonally up/right until a boundary or other color.
3. **Stopping Condition:** Expansion of all colors ceases upon reaching any grid boundary or encountering a pixel of a different color.
4. **Output:** Generate the output grid after expansion is completed for all seed pixels
"""

import numpy as np

def get_seed_pixels(grid):
    # Find the coordinates of all non-white pixels.
    seed_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                seed_pixels.append((r, c, grid[r, c]))
    return seed_pixels

def transform(input_grid):
    # Initialize the output grid with the same dimensions and filled with white (0).
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get the seed pixels and their colors.
    seed_pixels = get_seed_pixels(input_grid)

    # Controlled flood fill for each seed pixel.
    for r, c, color in seed_pixels:
        output_grid[r, c] = color  # original location

        if color == 1:  # Blue (1)
            # Right
            if c + 1 < cols and output_grid[r, c + 1] == 0:
                output_grid[r, c + 1] = color
            # Down
            if r + 1 < rows and output_grid[r + 1, c] == 0:
                output_grid[r + 1, c] = color
            # Diagonal down-right
            if r + 1 < rows and c + 1 < cols and output_grid[r + 1, c + 1] == 0:
                output_grid[r + 1, c + 1] = color

        elif color == 2:  # Red (2)
            # Left
            if c - 1 >= 0 and output_grid[r, c - 1] == 0:
                output_grid[r, c - 1] = color
            # Down
            if r + 1 < rows and output_grid[r + 1, c] == 0:
                output_grid[r + 1, c] = color
            # Diagonal down-left
            if r + 1 < rows and c - 1 >= 0 and output_grid[r + 1, c - 1] == 0:
                output_grid[r + 1, c - 1] = color

        elif color == 8:  # Azure (8)
            # Up
            if r - 1 >= 0 and output_grid[r - 1, c] == 0:
                output_grid[r - 1, c] = color
            # Right
            if c + 1 < cols and output_grid[r, c + 1] == 0:
                output_grid[r, c + 1] = color
            # Diagonal up-right
            if r - 1 >= 0 and c + 1 < cols and output_grid[r - 1, c + 1] == 0:
                output_grid[r - 1, c + 1] = color


    return output_grid
```
