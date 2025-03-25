```python
"""
Transforms an input grid into a 4x4 output grid. The input grid is divided
into four quadrants. The most frequent non-zero color in each quadrant is
assigned to the corresponding corner of the output grid.
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
    # Flatten the quadrant and convert to a list
    colors = quadrant.flatten().tolist()
    # Count the occurrences of each color
    counts = Counter(colors)
    
    # Remove zero counts if present
    if 0 in counts:
        del counts[0]
    
    if not counts: #If no colors other than zero
      return 0

    # Find the maximum count
    max_count = max(counts.values())

    # Find all colors with the maximum count (potential ties)
    most_frequent = [color for color, count in counts.items() if count == max_count]

    # If there's a tie, return the smallest color
    return min(most_frequent)
  

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Initialize output grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Assign corner values based on most frequent colors in quadrants
    output_grid[0, 0] = most_frequent_nonzero(get_quadrant(input_grid, "top_left"))
    output_grid[0, 3] = most_frequent_nonzero(get_quadrant(input_grid, "top_right"))
    output_grid[3, 0] = most_frequent_nonzero(get_quadrant(input_grid, "bottom_left"))
    output_grid[3, 3] = most_frequent_nonzero(get_quadrant(input_grid, "bottom_right"))

    return output_grid.tolist()
```