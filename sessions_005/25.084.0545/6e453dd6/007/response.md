```python
"""
1.  **Identify the Gray Stripe:** Find the single vertical column of gray pixels located towards the right side of the grid.

2.  **Identify the Magenta Shape:** Locate all magenta pixels. These form the central shape (potentially with interior holes of white). We can consider the collection of magenta colored cells as an "object".

3.  **Exterior Flood Fill:** Perform a flood fill operation, starting from the edges of the grid.
    *   Replace white pixels with magenta pixels.
    *   Do *not* replace any white pixels that are part of the *interior* of the magenta shape identified in step 2.  To determine interior status, do not expand into any magenta pixels during the flood fill.

4.  **Red Border Application:** Iterate through all *original* magenta pixels.
    *   For each original magenta pixel, check if it is immediately to the left of the gray stripe identified in step 1.
    *   If it is *adjacent to and to the left* of the gray stripe, change its color to red.

5.  The gray stripe remains unchanged.

6. **Output** return the final grid
"""

import numpy as np

def find_gray_stripe(grid):
    """Finds the rightmost vertical gray (5) stripe (single column)."""
    height, width = grid.shape
    for x in reversed(range(width)):
        stripe_found = False
        for y in range(height):
            if grid[y, x] == 5:
                stripe_found = True
            elif stripe_found:  # Check for single column
                stripe_found = False;
                break;
        if stripe_found:
            return x
    return -1  # Stripe not found

def flood_fill_exterior(grid, original_magenta):
    """
    Performs a flood fill, replacing exterior white (0) pixels with magenta (6),
    but preserving the interior of the original magenta shape.
    """
    height, width = grid.shape
    visited = set()
    output_grid = np.copy(grid)

    def fill(x, y):
        if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
            return
        visited.add((x, y))

        if output_grid[y, x] == 0:
            output_grid[y, x] = 6
            # Recursively fill adjacent pixels, but not if they are original magenta
            if (x + 1, y) not in original_magenta:
                fill(x + 1, y)
            if (x - 1, y) not in original_magenta:
                fill(x - 1, y)
            if (x, y + 1) not in original_magenta:
                fill(x, y + 1)
            if (x, y - 1) not in original_magenta:
                fill(x, y - 1)


    # Start flood fill from the edges
    for y in range(height):
        fill(0, y)
        fill(width - 1, y)
    for x in range(width):
        fill(x, 0)
        fill(x, height - 1)

    return output_grid



def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Find the gray stripe's x-coordinate
    gray_stripe_x = find_gray_stripe(input_grid)

    # 2. Identify original magenta pixels
    original_magenta = set()
    for y in range(height):
        for x in range(width):
            if input_grid[y, x] == 6:
                original_magenta.add((x, y))

    # 3. Exterior Flood Fill
    output_grid = flood_fill_exterior(output_grid, original_magenta)

    # 4. Red Border Application
    if gray_stripe_x != -1:
        for x, y in original_magenta:
            if x + 1 == gray_stripe_x:  # Directly to the left of the gray stripe
                output_grid[y, x] = 2

    return output_grid.tolist()
```