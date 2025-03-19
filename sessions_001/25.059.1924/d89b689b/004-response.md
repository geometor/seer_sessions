# d89b689b • 004 • example_1 • investigate_coder

---
```python
"""
1. Identify single colored pixels: Locate all pixels in the input grid that are not part of a multi-pixel contiguous block of the same color.
2. Extract colors: Record the colors of these identified single pixels.
3. Create a new 2x2 block: Form a 2x2 block in the center of the output grid.
4. Populate the new block: Fill the new 2x2 block with the recorded colors. The arrangement is predetermined.
5. Clear other pixels: Set all other pixels of the output to 0 (white).
"""

import numpy as np

def find_single_pixels(grid):
    """Finds isolated pixels of unique colors, not part of larger same-color blocks."""
    rows, cols = grid.shape
    single_pixels = []
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color):
      
        count = 0
        stack = [(r,c)]
        elements = []

        while stack:
          row, col = stack.pop()

          if not is_valid(row, col) or visited[row, col] or grid[row,col] != color:
            continue
          
          visited[row,col] = True
          count += 1
          elements.append((row,col))

          neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
          for nr, nc in neighbors:
            stack.append((nr, nc))
        
        return count, elements
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r,c] != 0:
              color = grid[r,c]
              count, elements = dfs(r,c, color)
              if count == 1:
                single_pixels.append((r, c, color))
    return single_pixels


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Find single pixels
    single_pixels = find_single_pixels(input_grid)
  
    # Extract colors and their original positions
    colors = {}
    for r, c, color in single_pixels:
        if color == 6: #magenta
            colors['magenta'] = color
        elif color == 7:
            colors['orange'] = color
        elif color == 4:
            colors['yellow'] = color
        elif color == 9:
            colors['maroon'] = color

    # Create the 2x2 block in the center of the output grid
    center_row = output_grid.shape[0] // 2 -1
    center_col = output_grid.shape[1] // 2 -1
    
    #put the colors into the output grid
    output_grid[center_row, center_col] = colors.get('magenta',0)
    output_grid[center_row, center_col + 1] = colors.get('orange',0)
    output_grid[center_row + 1, center_col] = colors.get('yellow',0)
    output_grid[center_row + 1, center_col + 1] = colors.get('maroon',0)
    
    return output_grid
```
