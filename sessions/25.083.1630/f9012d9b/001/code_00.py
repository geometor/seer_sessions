"""
1.  **Analyze Input:** Examine the input grid, noting all colors and their arrangement.
2.  **Find most Frequent:** Find the single value that is most frequent. If the most frequent is not unique, proceed.
3.  **Identify Central Pattern:** Look for a repeating color pattern, particularly around the center of the grid, or extending out from the center.
4.  **Extract Representative Sub-grid:** Select the smallest sub-grid that captures this central pattern. If no clear central pattern is present:
5.  **Largest Area (Fallback):** Identify the color that occupies the largest contiguous area within the grid (excluding the "background" or border color if there is an obvious one).
6.  **Minimal Output:** extract a minimal pattern representation.
7.  **Return:** Create an output grid containing this sub-grid or minimal representation.
"""

import numpy as np
from collections import Counter

def get_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

def get_largest_contiguous_area_color(grid):
  """
  Finds the largest connected area of same color
  """
  rows, cols = grid.shape
  max_area = 0
  max_color = -1
  visited = np.zeros((rows, cols), dtype=bool)

  def dfs(row, col, color):
    if (row < 0 or row >= rows or col < 0 or col >= cols or
        visited[row, col] or grid[row, col] != color):
      return 0
    visited[row, col] = True
    return (1 + dfs(row + 1, col, color) +
            dfs(row - 1, col, color) +
            dfs(row, col + 1, color) +
            dfs(row, col - 1, color))
            # no diagonal
            #+ dfs(row + 1, col + 1, color)
            #+ dfs(row + 1, col -1, color)
            #+ dfs(row - 1, col - 1, color)
            #+ dfs(row - 1, col + 1, color)

  for r in range(rows):
    for c in range(cols):
      if not visited[r, c]:
        area = dfs(r, c, grid[r, c])
        if area > max_area:
          max_area = area
          max_color = grid[r,c]
  return max_color
    

def extract_central_pattern(grid):
    """Extracts a small sub-grid from the center."""
    rows, cols = grid.shape
    center_row, center_col = rows // 2, cols // 2

    if rows > 2 and cols > 2:    
        return grid[center_row-1:center_row+1, center_col-1:center_col+1]
    elif rows > 1 and cols > 1:
        return grid[center_row-1:center_row, center_col-1:center_col]
    else:
      return np.array([[grid[0,0]]])



def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    grid = np.array(input_grid)

    # Find the most frequent color.
    most_frequent = get_most_frequent_color(grid)
    
    counts = Counter(grid.flatten())

    if counts[most_frequent] == 1:
      return np.array([[most_frequent]])

    # check for unique
    unique = True
    for k in counts:
      if counts[k] == counts[most_frequent] and k != most_frequent:
        unique = False
        break

    if unique:
      return np.array([[most_frequent]]) # Return a 1x1 grid with the most frequent color.

    # Attempt to extract a central pattern.
    central_pattern = extract_central_pattern(grid)
    if central_pattern.size > 0:
      return central_pattern

    # Fallback: Largest contiguous area.
    largest_area_color = get_largest_contiguous_area_color(grid)

    return np.array([[largest_area_color]])