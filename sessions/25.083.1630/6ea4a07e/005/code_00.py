"""
Transforms a 3x3 input grid to a 3x3 output grid based on these rules:

1.  **Input Grid:** Receive a 3x3 grid of colored pixels.
2.  **Dominant Color:** Identify the most frequent non-zero color in the input grid.  Handle ties by prioritizing the top-leftmost color.
3.  **Conceptual Rotation:** Mentally rotate the entire input grid 90 degrees counter-clockwise.
4.  **Color Mapping:** Map the original dominant color to its new color:
    *   5 (gray) becomes 4 (yellow)
    *   8 (azure) becomes 2 (red)
    *   3 (green) becomes 1 (blue)
5.  **Replacement:** In the rotated grid, replace the original dominant color with its mapped color.
6.  **Zero Center:** Set the center cell of the rotated grid to 0.
7.  **Output Grid:** Return the resulting 3x3 grid.
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

def rotate_grid(grid):
    # Rotate the grid 90 degrees counter-clockwise
    rotated_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            rotated_grid[j][2 - i] = grid[i][j]
    return rotated_grid

def transform(input_grid):
    # Initialize output_grid as all zeros
    output_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Get the dominant color in the input grid
    dominant_color = get_dominant_color(input_grid)

    # Rotate the grid conceptually
    rotated_grid = rotate_grid(input_grid)

    # Color mapping
    color_map = {
        5: 4,
        8: 2,
        3: 1
    }
    transformed_color = color_map.get(dominant_color, 0)  # Default to 0 if not found

    # Replace the original dominant color with the transformed color in the rotated grid
    for i in range(3):
        for j in range(3):
            if input_grid[i][j] == dominant_color:
                rotated_grid[j][2-i] = transformed_color

    # Set the center position to zero
    rotated_grid[1][1] = 0
    
    output_grid = rotated_grid

    return output_grid