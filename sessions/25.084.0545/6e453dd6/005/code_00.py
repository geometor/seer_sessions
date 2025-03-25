"""
1.  **Identify the Gray Stripe:** Locate the single vertical column of gray (5) pixels near the right edge of the input grid.
2.  **Record Original Magenta:** Store the (x, y) coordinates of all magenta (6) pixels in the input grid. These define the "central shape."
3.  **Exterior Flood Fill:** Starting from the edges of the grid, perform a flood fill operation.
    *   Replace white (0) pixels with magenta (6) pixels.
    *   *Crucially*, do *not* perform the fill on any pixel whose coordinates were stored in step 2 (the original magenta pixels).  This preserves the interior white areas of the central shape. Use a visited set to avoid cycles.
4.  **Apply Red Border:** Iterate through the (x, y) coordinates stored in step 2 (original magenta pixels).
    *   For each coordinate (x, y), check if the pixel at (x+1, y) is part of the gray stripe identified in step 1.
    *   If it is, change the color of the pixel at (x, y) to red (2).
5. The gray stripe itself should be unchanged.
6.  **Output:** The modified grid is the final output.
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

def flood_fill_restricted(grid, x, y, target_color, replacement_color, original_magenta, visited):
    """
    Performs a restricted flood fill.  It replaces 'target_color' with
    'replacement_color', starting from (x, y), but only on the exterior and
    it will not fill through original magenta pixels. Uses a visited set.
    """
    height, width = grid.shape
    if (x, y) in original_magenta or (x,y) in visited:
        return

    stack = [(x, y)]
    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height or grid[y,x] != target_color or (x,y) in visited:
            continue

        visited.add((x,y))
        grid[y,x] = replacement_color;

        # Add adjacent cells, checking bounds and original magenta
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
    visited = set()
    for y in range(height):
        if output_grid[y, 0] == 0:
            flood_fill_restricted(output_grid, 0, y, 0, 6, original_magenta, visited)
        if output_grid[y, width - 1] == 0:
            flood_fill_restricted(output_grid, width - 1, y, 0, 6, original_magenta, visited)
    for x in range(width):
        if output_grid[0, x] == 0:
            flood_fill_restricted(output_grid, x, 0, 0, 6, original_magenta, visited)
        if output_grid[height - 1, x] == 0:
            flood_fill_restricted(output_grid, x, height - 1, 0, 6, original_magenta, visited)
            

    # 4. Create Red Border (only on original magenta to the *left* of gray stripe)
    if gray_stripe_x != -1:
        for x, y in original_magenta:
            if x + 1 == gray_stripe_x:
                output_grid[y, x] = 2

    # 5. Return result (gray stripe unchanged implicitly)
    return output_grid.tolist()