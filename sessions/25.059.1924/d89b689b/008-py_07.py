"""
1.  **Identify Single Pixels:** Examine the input grid to find all pixels that are not adjacent (horizontally or vertically) to any other pixel of the same color. These are "single pixels".

2.  **Record Colors:** Note the colors of the single pixels. We are interested in orange (7), yellow (4), and maroon (9). Magenta (6) is *not* relevant to constructing the output.

3.  **Create Output Block:** Create a 2x2 block of pixels in the center of the output grid, regardless of the size of the overall grid.
    *   Calculate the center row index: `output_grid.shape[0] // 2 - 1`
    *   Calculate the center column index: `output_grid.shape[1] // 2 - 1`

4.  **Populate Output Block (Conditional):**
    *   Fill the 2x2 block with the colors recorded from the single pixels in a predefined order:
        *   Top-right: orange (7)
        *   Bottom-left: yellow (4)
        *   Bottom-right: maroon (9)
    *   The top-left position of the 2x2 block is always empty (or black, color 0).
    *   If any of the colors orange, yellow, or maroon are *not* found among the single pixels, leave the corresponding position in the 2x2 block as black(0).

5. **Clear Remaining Pixels:** Set all pixels outside the central 2x2 block to black (0).
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
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Find single pixels (Step 1)
    single_pixels = find_single_pixels(input_grid)
  
    # Extract relevant colors, defaulting to 0 (Step 2)
    colors = {
        'orange': 0,
        'yellow': 0,
        'maroon': 0
        }
    for r, c, color in single_pixels:
        if color == 7:
            colors['orange'] = color
        elif color == 4:
            colors['yellow'] = color
        elif color == 9:
            colors['maroon'] = color

    # Calculate center for the 2x2 block (Step 3)
    center_row = output_grid.shape[0] // 2 - 1
    center_col = output_grid.shape[1] // 2 - 1
    
    # Populate Output Block (Step 4)
    output_grid[center_row, center_col + 1] = colors['orange']  # Top-right
    output_grid[center_row + 1, center_col] = colors['yellow']  # Bottom-left
    output_grid[center_row + 1, center_col + 1] = colors['maroon'] # Bottom-right
    
    return output_grid