```python
"""
1.  **Identify Gray Pixels:** Examine each pixel in the input grid. Focus on pixels that are gray (color value 5).

2.  **Check for Adjacent Gray Neighbors:** For each gray pixel, examine its eight neighbors (horizontal, vertical, and diagonal).

3.  **Determine Line Formation:** A gray pixel is considered part of a line if at least *two* other gray pixels are adjacent to it, forming a continuous line segment. This line can be horizontal, vertical, or diagonal. It is *not* required the gray pixel is the *center* of a line of three.

4.  **Change Color to Green:** If a gray pixel meets the line formation criteria (has at least two adjacent gray neighbors in a line), change its color to green (color value 3).

5.  **Output:** The output grid is the result of these transformations, with all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    def count_adjacent_gray(r, c):
        """Counts adjacent gray pixels (including diagonals)."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] == 5:
                    count += 1
        return count

    def check_line_neighbors(r,c):
      """check if at least two neighbors are gray, forming a line"""
      count = 0
      for dr in [-1,0,1]:
        for dc in [-1,0,1]:
          if dr == 0 and dc == 0:
            continue

          nr, nc = r + dr, c + dc
          if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr,nc] == 5:
            # check if there's another pixel in the same line direction
            nr2, nc2 = nr + dr, nc + dc
            if 0 <= nr2 < rows and 0 <= nc2 < cols and input_grid[nr2, nc2] == 5:
                return True

            # check opp direction
            nr2, nc2 = r-dr, c-dc
            if 0 <= nr2 < rows and 0 <= nc2 < cols and input_grid[nr2,nc2] == 5:
                return True


      return False
    # Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is gray (5).
            if input_grid[r, c] == 5:
                # Check for adjacent gray neighbors and line formation
                if check_line_neighbors(r,c):
                  output_grid[r,c] = 3


    return output_grid
```