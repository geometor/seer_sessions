"""
1.  **Identify Rectangles:** Scan the input grid and identify all contiguous blocks of non-zero pixels. Each block represents a rectangle. Record the color, size (width and height), and top-left corner position of each rectangle.

2.  **Select Target Rectangle**:
    *   In the first example, select the magenta (6) rectangle.
    *   In the second example, select the yellow (4) rectangle.
    *   In the third example, select the gray (5) rectangle.
    The selection appears to be made choosing a unique color on the input grid.

3.  **Extract and Resize:** Extract the selected rectangle. Remove any rows and columns along the edges of the extracted rectangle that consist entirely of '0' (white/background) pixels.

4. **Output** The output is the smallest possible sub-grid containing the chosen rectangle.
"""

import numpy as np

def find_rectangles(grid):
    """Finds all rectangles in a grid."""
    rectangles = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_rectangle):
        if not is_valid(r, c) or (r, c) in visited or grid[r, c] != color:
            return
        visited.add((r, c))
        current_rectangle.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_rectangle)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_rectangle = []
                dfs(r, c, grid[r, c], current_rectangle)
                if current_rectangle:
                    # Find top-left and bottom-right
                    min_row = min(cell[0] for cell in current_rectangle)
                    max_row = max(cell[0] for cell in current_rectangle)
                    min_col = min(cell[1] for cell in current_rectangle)
                    max_col = max(cell[1] for cell in current_rectangle)

                    rectangles.append({
                        'color': grid[r, c],
                        'top_left': (min_row, min_col),
                        'bottom_right': (max_row, max_col),
                        'width': max_col - min_col + 1,
                        'height': max_row - min_row + 1
                    })
    return rectangles

def select_unique_rectangle(rectangles):
  """ selects the rectangle with a unique color """
  color_counts = {}
  for rect in rectangles:
      color = rect['color']
      color_counts[color] = color_counts.get(color, 0) + 1

  for rect in rectangles:
      if color_counts[rect['color']] == 1:
            return rect

  return None # if no unique color found



def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find all rectangles in the grid
    rectangles = find_rectangles(grid)
    
    #select unique rectangle by color
    target_rectangle = select_unique_rectangle(rectangles)

    if target_rectangle is None:
       return [[]]

    # Extract the selected rectangle
    top_left = target_rectangle['top_left']
    bottom_right = target_rectangle['bottom_right']
    extracted_rectangle = grid[top_left[0]:bottom_right[0] + 1, top_left[1]:bottom_right[1] + 1]
    
    return extracted_rectangle.tolist()