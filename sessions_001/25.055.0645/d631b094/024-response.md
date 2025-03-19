# d631b094 • 024 • refine_coder

---
```python
"""
The input may consist of one or more grids. For each input grid, the program counts the occurrences of each unique color present.
If there is one input grid, it creates a single-row output grid and populates it with the counted number of pixels for each color,
maintaining the order in which the colors appear. If there are multiple input grids, the program creates a corresponding number of rows
in the output grid, with the width being equal to the widest input grid. It then populates each row with the counted number of pixels for each unique
color found in the corresponding input grid, padding shorter rows with zeros as needed.
"""

import numpy as np

def count_colors(grid):
    """Counts the occurrences of each unique color in a grid."""
    unique_colors = np.unique(grid)
    color_counts = {}
    for color in unique_colors:
        color_counts[color] = np.sum(grid == color)
    return color_counts

def transform(grids):
    # Handle the case where 'grids' is a single NumPy array.
    if isinstance(grids, np.ndarray):
        grids = [grids]

    num_grids = len(grids)
    max_width = 0

    # Count colors and find the maximum width for multiple grids.
    all_color_counts = []
    for grid in grids:
      color_counts = count_colors(grid)
      all_color_counts.append(color_counts)
      total_pixels = sum(color_counts.values())
      max_width = max(max_width, total_pixels)


    # Create output grid based on the number of input grids
    if num_grids == 1:
        output_grid = np.zeros((1, max_width), dtype=int)
        current_index = 0
        color_counts = all_color_counts[0]
        for color in sorted(color_counts.keys(), key=lambda k: np.where(grids[0] == k)[1][0] if np.any(grids[0] == k) else -1 ): #find first index where a color appears and sort by that
            count = color_counts[color]
            output_grid[0, current_index:current_index + count] = color
            current_index += count

    else:
        output_grid = np.zeros((num_grids, max_width), dtype=int)
        for i, color_counts in enumerate(all_color_counts):
            current_index = 0
            for color in sorted(color_counts.keys(), key=lambda k: np.where(grids[i] == k)[1][0] if np.any(grids[i] == k) else -1 ): #sort color by first appearance
                count = color_counts[color]
                output_grid[i, current_index:current_index + count] = color
                current_index += count

    return output_grid
```
