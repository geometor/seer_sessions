```python
"""
Transforms the input grid by moving single pixels (1x1 color blocks) adjacent to azure (color 8) rectangles.
Single pixels of any color other than azure or background are moved to empty cells that are adjacent to the azure rectangles.
If a single pixel is already adjacent to a rectangle, it is not moved.
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


def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find azure rectangles
    rectangles = find_azure_rectangles(input_grid)

    # Find single pixels
    single_pixels = find_single_pixels(input_grid)
    
    # Create a set of all azure rectangle cells for easy checking
    rectangle_cells = set()
    for rect_r, rect_c, rect_h, rect_w in rectangles:
        for r in range(rect_r, rect_r + rect_h):
            for c in range(rect_c, rect_c + rect_w):
              rectangle_cells.add((r,c))

    moved_pixels = set()

    # Iterate through each azure rectangle
    for rect_r, rect_c, rect_h, rect_w in rectangles:
        # Find valid adjacent positions around the current rectangle
        adjacent_positions = []
        for r in range(rect_r - 1, rect_r + rect_h + 1):
            for c in range(rect_c - 1, rect_c + rect_w + 1):
                if (0 <= r < rows and 0 <= c < cols and  # Within bounds
                    (r, c) not in rectangle_cells and  # Not part of the rectangle itself
                    output_grid[r, c] == 0): # and the cell is empty (background)
                  adjacent_positions.append((r,c))

        # Move adjacent single pixels
        for r, c in single_pixels:
              if (r,c) in moved_pixels:
                continue # skip pixels already moved

              # Check if near the rectangle
              if is_adjacent_to_rectangle(r,c, rect_r, rect_c, rect_h, rect_w):
                  # find an adjacent spot and move
                  if len(adjacent_positions) > 0:
                    adj_r, adj_c = adjacent_positions.pop(0)
                    output_grid[adj_r, adj_c] = input_grid[r,c]
                    output_grid[r,c] = 0 # clear original
                    moved_pixels.add((adj_r, adj_c)) # record as moved

    return output_grid
```