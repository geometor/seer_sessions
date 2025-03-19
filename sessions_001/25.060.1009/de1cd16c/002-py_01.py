"""
The input grid is divided into four quadrants. The output is a single digit representing the background color of the lower-right quadrant.
"""

import numpy as np

def get_quadrant(grid, quadrant):
    """
    Extracts a specified quadrant from the input grid.

    Args:
        grid: The input grid (2D numpy array).
        quadrant: String, one of 'top-left', 'top-right', 'bottom-left', 'bottom-right'.

    Returns:
        A 2D numpy array representing the specified quadrant.
    """
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant == 'top-left':
        return grid[:mid_row, :mid_col]
    elif quadrant == 'top-right':
        return grid[:mid_row, mid_col:]
    elif quadrant == 'bottom-left':
        return grid[mid_row:, :mid_col]
    elif quadrant == 'bottom-right':
        return grid[mid_row:, mid_col:]
    else:
        raise ValueError("Invalid quadrant specified.")

def most_frequent_color(quadrant):
  """
    find most frequent value, ignoring zeros

  """
  # Flatten the quadrant and convert to a list
  flat_quadrant = quadrant.flatten().tolist()

  counts = {}
  for color in flat_quadrant:
      if color not in counts:
          counts[color] = 0
      counts[color] += 1
    
  max_count = 0
  mode = -1

  for color, count in counts.items():
    if count > max_count:
      max_count = count
      mode = color
    
  return mode


def transform(input_grid):
    """
    Transforms the input grid according to the rule: output is the background color of the lower-right quadrant.
    """
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # Get the lower-right quadrant
    lower_right_quadrant = get_quadrant(grid, 'bottom-right')

    # Determine the most frequent color in the lower-right quadrant
    background_color = most_frequent_color(lower_right_quadrant)
    
    # Return output 
    return background_color