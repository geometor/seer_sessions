# c0f76784 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Gray Regions:** Locate all contiguous blocks of gray (value 5) pixels in the input grid.
2.  **Inner Most Pixel Identification:** Within each gray, identify the inner most pixels.
3.  **Conditional Replacement (Top Region):**
    a. Locate the three horizontally adjacent, inner most gray pixels and replace them with azure (8).
    b. Find one inner most gray pixel surrounded on top, right and left by 5s, and replace with magenta (6)
4. **Conditional Replacement (Bottom region):** Locate a 2 x 2 group of inner most gray pixels, and replace with orange (7).
5.  **Preserve Other Pixels:** All other pixels in the grid that are not gray, or a targeted inner gray, remain unchanged.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore contiguous regions."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def find_inner_pixels(region, grid):
    """Identifies 'inner' pixels within a region."""
    inner_pixels = []
    for row, col in region:
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        is_inner = True
        for n_row, n_col in neighbors:
            if not (0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1] and grid[n_row,n_col] == 5):
                is_inner = False #If not all neighbors are 5 and in the grid.
                break
        if is_inner:
                inner_pixels.append((row, col))
    return inner_pixels

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    gray_regions = find_contiguous_regions(input_grid, 5)

    for region in gray_regions:
        inner_pixels = find_inner_pixels(region, input_grid)

        #Conditional Replacement for Top Region
        if len(inner_pixels) >= 3:
          #Sort inner pixels by row then column
          inner_pixels.sort(key=lambda x: (x[0], x[1]))

          #Check for three horizontally adjacent pixels
          for i in range(len(inner_pixels) - 2):
              if (inner_pixels[i][0] == inner_pixels[i+1][0] == inner_pixels[i+2][0] and #Same row
                  inner_pixels[i][1] + 1 == inner_pixels[i+1][1] and               #Adjacent columns
                  inner_pixels[i+1][1] + 1 == inner_pixels[i+2][1]):

                  output_grid[inner_pixels[i]] = 8
                  output_grid[inner_pixels[i+1]] = 8
                  output_grid[inner_pixels[i+2]] = 8

                  #Check for a pixel below, with adjacent neighbors
                  for j in range(len(inner_pixels)):
                      if (inner_pixels[j][0] == inner_pixels[i][0] + 1 and           # One row below
                          inner_pixels[i][1] <= inner_pixels[j][1] <= inner_pixels[i+2][1]): #Within top row cols.

                          #Check direct neighbours to see if we match the criteria.
                          neighbors = [(inner_pixels[j][0], inner_pixels[j][1] - 1),
                                       (inner_pixels[j][0], inner_pixels[j][1] + 1),
                                       (inner_pixels[j][0] - 1, inner_pixels[j][1])]

                          is_surrounded = True
                          for nr, nc in neighbors:
                              if not(0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1] and
                                     output_grid[nr, nc] == 5):
                                  is_surrounded = False
                                  break
                          if is_surrounded:
                              output_grid[inner_pixels[j]] = 6
                              break #Only one such pixel.
                  break # Move to the next region

        # Conditional Replacement (Bottom region)
        if len(inner_pixels) >= 4:
          inner_pixels.sort(key=lambda x: (x[0], x[1]))

          for i in range(len(inner_pixels)-1):
              for j in range(i+1, len(inner_pixels)):
                if (inner_pixels[i][0] == inner_pixels[j][0] -1 and
                   inner_pixels[i][1] == inner_pixels[j][1]):

                    # Check if there is one directly to the right.
                    right_neighbor_i = (inner_pixels[i][0], inner_pixels[i][1] + 1)
                    right_neighbor_j = (inner_pixels[j][0], inner_pixels[j][1] + 1)

                    if right_neighbor_i in inner_pixels and right_neighbor_j in inner_pixels:
                        output_grid[inner_pixels[i]] = 7
                        output_grid[right_neighbor_i] = 7
                        output_grid[inner_pixels[j]] = 7
                        output_grid[right_neighbor_j] = 7

                        break # Move on after finding the first.
              else: #Inner loop finished
                  continue
              break #Outer loop break if we matched a pair

    return output_grid
```
