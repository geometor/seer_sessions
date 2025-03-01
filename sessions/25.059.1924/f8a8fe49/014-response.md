# f8a8fe49 • 014 • refine_coder

---
```python
"""
1.  **Identify Red Structure:** Locate the contiguous region of red pixels, which forms a "C"-like shape.
2.  **Define Bounding Box:** Define a rectangular bounding box that encompasses the entire red structure.
3.  **Identify Vertical Sections:** Within the red structure, identify the leftmost and rightmost vertical "bars".
4.  **Identify Gray Pixels:** Find all gray pixels.
5.  **Determine Gray Pixel Location:** Determine which gray pixels are located *between* the vertical bars of the red structure, considering only the rows within the vertical extent of both bars.
6.  **Reposition Gray Pixels:**
    *   The gray pixels located between the vertical bars are moved.
    *   Create two new vertical lines of gray pixels: one immediately to the left of the left red bar and one immediately to the right of the right red bar.
    *   The *number* of gray pixels in each new vertical line is equal to the number of gray pixels that were originally between the vertical bars, with a maximum height defined next.
    *   The height of the new gray pixel lines should not exceed the height of the bounding box of the red structure. The top of the gray lines align with the top of the bounding box.
"""

import numpy as np

def find_red_structure(grid):
    """Finds the contiguous region of red pixels."""
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return []

    visited = set()
    structure = []

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != 2:
            return
        visited.add((row, col))
        structure.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    dfs(red_pixels[0][0], red_pixels[0][1])
    return structure

def get_bounding_box(structure):
    """Defines a bounding box around the given structure."""
    rows = [p[0] for p in structure]
    cols = [p[1] for p in structure]
    return min(rows), max(rows), min(cols), max(cols)

def get_vertical_sections(structure):
    """Identifies the leftmost and rightmost vertical bars."""
    if not structure:
        return [], []
    
    cols = [p[1] for p in structure]
    min_col = min(cols)
    max_col = max(cols)
    
    left_section = [(r, c) for r, c in structure if c == min_col]
    right_section = [(r, c) for r, c in structure if c == max_col]
    return left_section, right_section

def is_between_vertical_sections(gray_pixel, left_section, right_section):
    """Checks if a gray pixel is between the vertical sections."""
    if not left_section or not right_section:
      return False
    
    gray_row, gray_col = gray_pixel
    
    left_col = left_section[0][1]
    right_col = right_section[0][1]

    if gray_col > left_col and gray_col < right_col:
      #check for mostly vertical by comparing row extents
      left_rows = [p[0] for p in left_section]
      right_rows = [p[0] for p in right_section]

      min_row = max(min(left_rows), min(right_rows))
      max_row = min(max(left_rows), max(right_rows))
      if gray_row >= min_row and gray_row <= max_row:
        return True
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the red structure.
    red_structure = find_red_structure(input_grid)

    # Define the bounding box.
    min_row, max_row, min_col, max_col = get_bounding_box(red_structure)

    # Identify vertical sections.
    left_section, right_section = get_vertical_sections(red_structure)

    # Find gray pixels.
    gray_pixels = np.argwhere(input_grid == 5)

    # Determine gray pixels to move.
    gray_pixels_to_move = [gp for gp in gray_pixels if is_between_vertical_sections(gp, left_section, right_section)]

    # Reposition gray pixels.
    num_to_move = len(gray_pixels_to_move)
    if num_to_move > 0:
        # Clear original gray pixels.
        for r, c in gray_pixels_to_move:
            output_grid[r, c] = 0

        # Calculate new positions, constrained by bounding box height.
        new_left_col = min_col - 1
        new_right_col = max_col + 1
        height_to_use = min(num_to_move, max_row - min_row + 1)

        # Place new gray pixels.
        for i in range(height_to_use):
            output_grid[min_row + i, new_left_col] = 5
            output_grid[min_row + i, new_right_col] = 5

    return output_grid
```
