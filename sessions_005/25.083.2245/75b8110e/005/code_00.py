"""
Transforms an input grid into a 4x4 output grid. The input grid is divided
into four quadrants. The most frequent non-zero color in each quadrant is
assigned to the corresponding corner of the output grid, and then spread
following an alternating pattern.
"""

import numpy as np
from collections import Counter

def get_quadrant(input_grid, quadrant):
    """Divides the input grid into four quadrants and returns the specified quadrant."""
    grid = np.array(input_grid)
    height, width = grid.shape
    center_y = height // 2
    center_x = width // 2

    if quadrant == "top_left":
        return grid[:center_y, :center_x]
    elif quadrant == "top_right":
        return grid[:center_y, center_x:]
    elif quadrant == "bottom_left":
        return grid[center_y:, :center_x]
    elif quadrant == "bottom_right":
        return grid[center_y:, center_x:]
    else:
        raise ValueError("Invalid quadrant specified.")

def most_frequent_nonzero(quadrant):
    """
    Finds the most frequent non-zero color in a quadrant, with a tie-breaker.
    If a quadrant only consists of zeros, returns 0.
    """
    colors = quadrant.flatten().tolist()
    counts = Counter(colors)
    
    if 0 in counts:
        del counts[0]
    
    if not counts: #If no colors other than zero
      return 0

    max_count = max(counts.values())
    most_frequent = [color for color, count in counts.items() if count == max_count]
    return min(most_frequent)
  

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Initialize output grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Get most frequent colors for each quadrant
    top_left_color = most_frequent_nonzero(get_quadrant(input_grid, "top_left"))
    top_right_color = most_frequent_nonzero(get_quadrant(input_grid, "top_right"))
    bottom_left_color = most_frequent_nonzero(get_quadrant(input_grid, "bottom_left"))
    bottom_right_color = most_frequent_nonzero(get_quadrant(input_grid, "bottom_right"))

    # Assign corner values based on most frequent colors in quadrants
    output_grid[0, 0] = top_left_color
    output_grid[0, 3] = top_right_color
    output_grid[3, 0] = bottom_left_color
    output_grid[3, 3] = bottom_right_color

    # Fill the rest of the grid in the alternating pattern.
    for row in range(4):
        for col in range(4):
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                if (row == 0 and col == 0) or (row == 3 and col == 3) :
                    continue #Skip, already set

                if output_grid[0,0] != 0 or (row == 3 and col == 3) :
                  output_grid[row,col] = output_grid[0,0] if (row==0 and col==0) or (row==3 and col ==3) else output_grid[3,3]
            else:
                if (row == 0 and col == 3) or (row == 3 and col == 0) :
                    continue  #Skip, already set
                if output_grid[0,3] != 0 or (row==3 and col ==0):
                    output_grid[row,col] = output_grid[0,3] if (row==0 and col==3) else output_grid[3,0]

    return output_grid.tolist()