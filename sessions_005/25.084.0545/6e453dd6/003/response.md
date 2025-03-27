```python
"""
1.  **Identify Gray Stripe:** Find the single column of gray(5) pixels near the right edge of the input grid.
2.  **Store Original Magenta:** Record the positions of all magenta (6) pixels *before* any further modifications. These represent the original central shape.
3.  **Identify and Fill Background:** Perform a flood fill, starting from the edges of the grid.
    *   Target color: white (0)
    *   Replacement color: magenta (6)
    *   *Constraint:* The flood fill should *not* propagate through any pixels that were originally magenta (from step 2). It fills only the background.
4.  **Create Red Border:** For each pixel location stored in step 2 (original magenta pixels):
    *   Check if it's directly adjacent (horizontally) to the gray stripe identified in step 1.
    *   If it is, change its color to red (2).
5.  **Output:** The modified grid is the final output. All other pixels are unchanged.
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

def flood_fill_restricted(grid, x, y, target_color, replacement_color, original_magenta):
    """
    Performs a restricted flood fill.  It replaces 'target_color' with
    'replacement_color', starting from (x, y), but only on the exterior and
    it will not fill through original magenta pixels.
    """
    height, width = grid.shape
    if (x, y) in original_magenta:
        return

    stack = [(x, y)]
    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height or grid[y,x] != target_color:
            continue

        grid[y,x] = replacement_color;

        # Add adjacent cells, checking bounds
        if (x+1,y) not in original_magenta:
            stack.append((x + 1, y))
        if (x-1, y) not in original_magenta:
            stack.append((x - 1, y))
        if (x,y+1) not in original_magenta:    
            stack.append((x, y + 1))
        if (x, y-1) not in original_magenta:
            stack.append((x, y - 1))


def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    input_grid = np.array(input_grid) # Ensure numpy array
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 1. Find the gray stripe's x-coordinate
    gray_stripe_x = find_gray_stripe(output_grid)

    # 2. Store original magenta pixel locations
    original_magenta = set()
    for y in range(height):
        for x in range(width):
            if output_grid[y, x] == 6:
                original_magenta.add((x, y))

    # 3. Restricted Flood Fill from the edges
    for y in range(height):
        if output_grid[y, 0] == 0:
            flood_fill_restricted(output_grid, 0, y, 0, 6, original_magenta)
        if output_grid[y, width - 1] == 0:
            flood_fill_restricted(output_grid, width - 1, y, 0, 6, original_magenta)
    for x in range(width):
        if output_grid[0, x] == 0:
            flood_fill_restricted(output_grid, x, 0, 0, 6, original_magenta)
        if output_grid[height - 1, x] == 0:
            flood_fill_restricted(output_grid, x, height - 1, 0, 6, original_magenta)
            

    # 4. Create Red Border (only on original magenta)
    if gray_stripe_x != -1:
        for y in range(height):
            if (gray_stripe_x - 1, y) in original_magenta:
                output_grid[y, gray_stripe_x - 1] = 2
            if (gray_stripe_x + 1, y) in original_magenta:  # Check to the right (shouldn't happen, but for completeness)
                output_grid[y, gray_stripe_x + 1] = 2

    # 5. return result
    return output_grid.tolist()
```