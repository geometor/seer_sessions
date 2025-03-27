"""
Transforms a 3x3 input grid to a 3x3 output grid based on these rules:

1.  **Identify the dominant color:** Find the non-zero color that appears most frequently in the input grid. If there are two non-zero colors that appear with equal frequency, select the top-left most one.
2.  **Color Mapping**: Transform the dominant color to its mapped pair:
    *   5 (gray) becomes 4 (yellow)
    *   8 (azure) becomes 2 (red)
    *   3 (green) becomes 1 (blue)
3.  **Rotate Counter-Clockwise:** Place the transformed color in the output grid by rotating *each* position of the input color 90 degrees counter-clockwise.  The rotation formula for a point (r,c) around a 3x3 grid is: (new_r, new_c) = (c, 2-r)
4.  **Zero the Center:** The center cell of the output grid is always 0.
"""

import numpy as np

def get_dominant_color(grid):
    # Count the occurrences of each non-zero color
    color_counts = {}
    for row in grid:
        for cell in row:
            if cell != 0:
                color_counts[cell] = color_counts.get(cell, 0) + 1

    # Return the most frequent color, tie goes to top-left
    if not color_counts:
        return 0
    
    max_count = max(color_counts.values())
    candidates = [color for color, count in color_counts.items() if count == max_count]
    
    if len(candidates) == 1:
        return candidates[0]
    
    # Handle ties by finding the color that appears first, top left
    for r_idx, row in enumerate(grid):
      for c_idx, cell in enumerate(row):
        if cell in candidates:
          return cell
    
    return 0 # should never get here, given task specs

def transform(input_grid):
    # Initialize output_grid as all zeros
    output_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Get the dominant color in the input grid
    dominant_color = get_dominant_color(input_grid)

    # Color mapping
    color_map = {
        5: 4,
        8: 2,
        3: 1
    }
    transformed_color = color_map.get(dominant_color, 0)

    # Rotate and transform
    for i in range(3):
        for j in range(3):
            if input_grid[i][j] == dominant_color:
                # Rotate 90 degrees counter-clockwise: (i, j) -> (j, 2 - i)
                new_i, new_j = j, 2 - i
                output_grid[new_i][new_j] = transformed_color

    # Set the center position to zero
    output_grid[1][1] = 0

    return output_grid