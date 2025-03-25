```python
"""
Transforms input grids based on identified rectangular regions of uniform color, applying specific rules for blue, red, and azure rectangles, and handling surrounding conditions.

1. Identify Rectangles: Find all rectangular regions of uniform color.
2. Blue Removal: Remove blue (1) rectangles (set to white/0).
3. Surrounded Green Removal: Remove green (3) if surrounded by blue (1).
4. Red Transformation: Change the interior of red (2) rectangles to gray (5), preserving the red edge.
5. Azure Transformation: For azure (8) rectangles with width and height > 2, if surrounded by yellow (4)/magenta(6):
    - Fill the interior with green (3).
    - Bottom edge becomes green if touches another object
6. Other Colors: Leave unchanged unless specified above.
"""

import numpy as np

def find_rectangles(grid):
    """
    Finds all rectangular regions of uniform color in a grid.
    Returns a list of tuples: (color, (row_start, col_start), (row_end, col_end)).
    """
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                r_start, c_start = r, c
                r_end, c_end = r, c

                # Expand right
                while c_end + 1 < cols and grid[r, c_end + 1] == color and not visited[r, c_end+1]:
                    c_end += 1

                # Expand down
                while r_end + 1 < rows and all(grid[r_end + 1, c_start:c_end + 1] == color) and not any(visited[r_end+1, c_start:c_end+1]):
                    r_end += 1

                # Mark visited
                visited[r_start:r_end + 1, c_start:c_end + 1] = True
                rectangles.append((color, (r_start, c_start), (r_end, c_end)))
    return rectangles

def is_surrounded_by(grid, r_start, c_start, r_end, c_end, surrounding_color):
    """
    Checks if a rectangular region is surrounded by a specific color.
    """
    rows, cols = grid.shape

    # Check top
    if r_start > 0 and not all(grid[r_start - 1, c_start:c_end + 1] == surrounding_color):
        return False
    # Check bottom
    if r_end < rows - 1 and not all(grid[r_end + 1, c_start:c_end + 1] == surrounding_color):
        return False
    # Check left
    if c_start > 0 and not all(grid[r_start:r_end + 1, c_start - 1] == surrounding_color):
        return False
    # Check right
    if c_end < cols - 1 and not all(grid[r_start:r_end + 1, c_end + 1] == surrounding_color):
        return False

    # Check corners (top-left)
    if r_start > 0 and c_start > 0 and grid[r_start-1, c_start-1] != surrounding_color:
        return False
    # Check corners (top-right)
    if r_start > 0 and c_end < cols - 1 and grid[r_start-1, c_end+1] != surrounding_color:
      return False
    # Check corners (bottom-left)
    if r_end < rows - 1 and c_start > 0 and grid[r_end+1, c_start -1] != surrounding_color:
      return False
    # Check corners (bottom-right)
    if r_end < rows -1 and c_end < cols - 1 and grid[r_end+1, c_end+1] != surrounding_color:
      return False

    return True

def remove_surrounded(grid, color_to_remove, surrounding_color):
  """Removes contiguous regions of color_to_remove if surrounded by surrounding_color."""
  rows, cols = grid.shape
  output_grid = grid.copy()
  visited = np.zeros_like(grid, dtype=bool)

  for r in range(rows):
      for c in range(cols):
          if not visited[r, c] and grid[r, c] == color_to_remove:
              # BFS to find connected region
              region = []
              queue = [(r, c)]
              visited[r, c] = True
              
              while queue:
                curr_r, curr_c = queue.pop(0)
                region.append((curr_r, curr_c))

                neighbors = [(curr_r-1, curr_c), (curr_r+1, curr_c), (curr_r, curr_c-1), (curr_r, curr_c+1)]
                for nr, nc in neighbors:
                  if(0 <= nr < rows and 0 <= nc < cols and not visited[nr,nc] and grid[nr,nc] == color_to_remove):
                    visited[nr,nc] = True
                    queue.append((nr,nc))

              # Check if surrounded
              surrounded = True
              for curr_r, curr_c in region:
                neighbors = [(curr_r-1, curr_c), (curr_r+1, curr_c), (curr_r, curr_c-1), (curr_r, curr_c+1),
                            (curr_r-1, curr_c-1), (curr_r+1, curr_c-1), (curr_r-1, curr_c+1), (curr_r+1, curr_c+1)]
                for nr, nc in neighbors:
                  if not (0 <= nr < rows and 0 <= nc < cols and (grid[nr, nc] == surrounding_color or (nr,nc) in region)):
                      surrounded = False
                      break

                if not surrounded:
                  break


              # Remove if surrounded
              if surrounded:
                  for curr_r, curr_c in region:
                      output_grid[curr_r, curr_c] = 0

  return output_grid

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = input_grid.copy()

    # Remove green surrounded by blue
    output_grid = remove_surrounded(output_grid, 3, 1)

    # Find all rectangular regions
    rectangles = find_rectangles(output_grid)
    
    # Iterate through each rectangle and apply transformation rules
    for color, (r_start, c_start), (r_end, c_end) in rectangles:
        # Rule 1: Remove blue (1) regions
        if color == 1:
            output_grid[r_start:r_end+1, c_start:c_end+1] = 0

        # Rule 2: Red (2) regions to gray (5) inside
        elif color == 2:
            output_grid[r_start+1:r_end, c_start+1:c_end] = 5

        # Rule 3: Modify azure (8) regions based on size and surrounding
        elif color == 8:
            if r_end - r_start + 1 > 2 and c_end - c_start + 1 > 2:
                #check if surrounding is 4 or 6
                if is_surrounded_by(input_grid, r_start, c_start, r_end, c_end, 4) or is_surrounded_by(input_grid, r_start, c_start, r_end, c_end, 6):
                    # Fill interior with green (3)
                    output_grid[r_start+1:r_end, c_start+1:c_end] = 3
                    #check bottom
                    rows, cols = output_grid.shape
                    if r_end < rows - 1:
                      for col in range(c_start, c_end + 1):
                        if output_grid[r_end+1,col] != 8 and output_grid[r_end+1,col] != 0:
                            output_grid[r_end,col] = 3
                            break

    return output_grid
```