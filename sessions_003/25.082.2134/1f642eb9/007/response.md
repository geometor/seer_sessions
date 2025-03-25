```python
"""
Transforms the input grid by moving single pixels (1x1 color blocks) that are *not* already adjacent to azure (color 8) rectangles.
These single pixels are moved to empty cells that *are* adjacent to the azure rectangles.
"""

import numpy as np

def find_azure_rectangles(grid):
    """Finds the top-left corner coordinates of all azure rectangles (3x2 or 2x3)."""
    rectangles = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 8:
                if (grid[r:r+2, c:c+3] == 8).all() and grid[r:r+2, c:c+3].size == 6:  # Check for 2x3
                    rectangles.append((r, c, 2, 3))
                elif (grid[r:r+3, c:c+2] == 8).all() and grid[r:r+3, c:c+2].size == 6:  # Check for 3x2
                    rectangles.append((r, c, 3, 2))
    return rectangles

def find_single_pixels(grid):
    """Finds the coordinates of all single pixels (excluding color 8 and 0)."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r,c] != 8:
                # Check if it's a single pixel (not part of a larger object)
                is_single = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == grid[r, c]:
                            is_single = False
                            break
                    if not is_single:
                        break
                if is_single:
                    pixels.append((r, c))
    return pixels

def is_adjacent_to_rectangle(r, c, rect_r, rect_c, rect_h, rect_w):
    """Checks if a cell (r, c) is adjacent to the rectangle."""
    if (rect_r -1 <= r <= rect_r + rect_h) and (rect_c - 1 <= c <= rect_c + rect_w):
      # now check it is NOT within rectangle
      if (rect_r <= r < rect_r + rect_h) and (rect_c  <= c < rect_c + rect_w):
          return False # inside the rectangle
      else:
        return True # adjacent
    else:
      return False
    
def find_non_adjacent_single_pixels(grid, rectangles):
    """Finds single pixels that are NOT adjacent to any azure rectangle."""
    single_pixels = find_single_pixels(grid)
    non_adjacent_pixels = []
    for r, c in single_pixels:
        adjacent = False
        for rect_r, rect_c, rect_h, rect_w in rectangles:
            if is_adjacent_to_rectangle(r, c, rect_r, rect_c, rect_h, rect_w):
                adjacent = True
                break
        if not adjacent:
            non_adjacent_pixels.append((r, c))
    return non_adjacent_pixels

def get_adjacent_empty_cells(grid, rect_r, rect_c, rect_h, rect_w):
    """Finds empty cells adjacent to a rectangle."""
    rows, cols = grid.shape
    empty_cells = []
    for r in range(rect_r - 1, rect_r + rect_h + 1):
        for c in range(rect_c - 1, rect_c + rect_w + 1):
            if (0 <= r < rows and 0 <= c < cols and
                grid[r, c] == 0 and
                not (rect_r <= r < rect_r + rect_h and rect_c <= c < rect_c + rect_w)):
                empty_cells.append((r, c))
    return empty_cells

def transform(input_grid):
    """Transforms the input grid by moving single pixels not adjacent to azure rectangles to empty cells adjacent to azure rectangles."""
    output_grid = np.copy(input_grid)
    rectangles = find_azure_rectangles(output_grid)
    non_adjacent_single_pixels = find_non_adjacent_single_pixels(output_grid, rectangles)

    pixel_index = 0  # Keep track of which pixel to move
    for rect_r, rect_c, rect_h, rect_w in rectangles:
        empty_cells = get_adjacent_empty_cells(output_grid, rect_r, rect_c, rect_h, rect_w)
        for empty_r, empty_c in empty_cells:
            if pixel_index < len(non_adjacent_single_pixels):
                pixel_r, pixel_c = non_adjacent_single_pixels[pixel_index]
                output_grid[empty_r, empty_c] = output_grid[pixel_r, pixel_c]
                output_grid[pixel_r, pixel_c] = 0
                pixel_index += 1
            else:
                break  # No more pixels to move

    return output_grid
```