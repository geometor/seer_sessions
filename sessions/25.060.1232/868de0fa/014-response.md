# 868de0fa • 014 • refine_coder

---
```python
"""
1.  **Identify the Blue Shape:** Find the contiguous region of blue (1) pixels in the input grid. This is the "blue shape."

2.  **Locate Top-Left:** Find the top-left pixel of the blue shape.

3.  **Change Top-Left to Orange:** Change the color of the *top-left* pixel of the blue shape to orange (7).

4.  **Conditional Red Rectangle:**
    *   If the blue shape occupies only the first few rows, then create a red rectangle within the blue shape as described below.
    *   Create a 2x2 red (2) rectangle *inside* the blue shape.
        *   The red rectangle's columns will be the *last two* columns of the *blue shape*.
        *   The red rectangle will be positioned vertically to begin at the second row of the blue shape, and end at the second to last row of the blue shape.
    *   If the blue shape is very tall, then instead of creating a rectangle, remove the bottom-right pixel of the blue shape.

5. **Gray Pixel Expansion (If Present):**
   * If there's a single gray (5) pixel and the blue shape occupies a larger area of the grid, remove the blue shape.
   * Expand the gray pixel to include any pixels previously occupied by the blue shape.
"""

import numpy as np

def find_contiguous_region(grid, color):
    # Find all pixels of the specified color.
    pixels = np.argwhere(grid == color)
    if len(pixels) == 0:
        return []

    # Start with the first pixel as the seed.
    seed = tuple(pixels[0])
    region = set()
    region.add(seed)
    queue = [seed]

    # Perform a breadth-first search to find all connected pixels.
    while queue:
        x, y = queue.pop(0)
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nx, ny in neighbors:
            if (0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and
                grid[nx, ny] == color and (nx, ny) not in region):
                region.add((nx, ny))
                queue.append((nx, ny))

    return list(region)

def find_top_left(region):
    # Find the top-left pixel within a region.
    if not region:
      return None

    min_row = min(pixel[0] for pixel in region)
    min_col_candidates = [pixel for pixel in region if pixel[0] == min_row]
    min_col = min(pixel[1] for pixel in min_col_candidates)
    return (min_row,min_col)

def get_bounding_box(region):
    if not region:
        return None
    min_row = min(r for r, c in region)
    max_row = max(r for r, c in region)
    min_col = min(c for r, c in region)
    max_col = max(c for r, c in region)
    return (min_row, min_col, max_row, max_col)

def find_bottom_right(region):
    # Find the bottom-right pixel of a region
    if not region:
        return None
    max_row = max(pixel[0] for pixel in region)
    max_col_candidates = [pixel for pixel in region if pixel[0] == max_row]
    max_col = max(pixel[1] for pixel in max_col_candidates)
    return (max_row, max_col)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the contiguous region of blue (1) pixels.
    blue_region = find_contiguous_region(input_grid, 1)

    # Find and change top-left pixel to orange
    top_left = find_top_left(blue_region)
    if top_left:
      output_grid[top_left] = 7

    # Conditional Red Rectangle or Bottom-Right Removal.
    if blue_region:
        min_row, min_col, max_row, max_col = get_bounding_box(blue_region)

        if max_row - min_row < input_grid.shape[0] * 0.7 :  # "first few rows" heuristic
            # Calculate red rectangle coordinates.
            red_start_row = min_row + 1
            red_end_row = max_row - 1
            red_start_col = max_col - 1
            red_end_col = max_col

            # Ensure red rectangle is within bounds.
            if red_start_row <= red_end_row and red_start_col <= red_end_col:
                for r in range(red_start_row, red_end_row + 1):
                    for c in range(red_start_col, red_end_col + 1):
                        if (r,c) in blue_region:
                            output_grid[r, c] = 2
        else:
            # Remove bottom-right pixel of the blue shape.
            bottom_right = find_bottom_right(blue_region)
            if bottom_right:
                output_grid[bottom_right] = input_grid[bottom_right] # set to input grid color

    # Gray Pixel Expansion.
    gray_region = find_contiguous_region(input_grid, 5)
    if len(gray_region) == 1 and len(blue_region) > 1:
        # get the gray pixel
        gray_pixel = gray_region[0]
        # Remove the blue shape and expand gray.
        for r, c in blue_region:
            output_grid[r, c] = 5
        # put the gray pixel back
        output_grid[gray_pixel] = 5

    return output_grid
```
