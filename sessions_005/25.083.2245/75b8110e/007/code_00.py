"""
Transforms an input grid into a 4x4 output grid. The input grid is divided
into four quadrants. The most frequent non-zero color in each quadrant is
assigned to the corresponding corner of the output grid. Zeros are inserted
based on their position between identical non-zero colors in the input grid.
The remaining cells are filled based on adjacent neighbors.
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
  
def insert_zeros(input_grid, output_grid):
    """
    Inserts zeros into the output grid based on the input grid.
    If a zero exists between two identical non-zero colors,
    horizontally or vertically, insert a zero in the output.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)  # Make a copy to modify
    height, width = input_grid.shape
    output_height, output_width = output_grid.shape

    for r in range(height):
        for c in range(width):
            if input_grid[r,c] == 0:
              if c > 0 and c < width -1:
                if input_grid[r,c-1] == input_grid[r, c+1] and input_grid[r,c-1] !=0:
                    out_r = int(r / height * output_height)
                    out_c = int(c / width * output_width)
                    if 0<= out_r < output_height and 0 <= out_c < output_width:
                      output_grid[out_r,out_c]=0
              if r > 0 and r < height-1:
                if input_grid[r-1,c] == input_grid[r+1,c] and input_grid[r-1,c] != 0:
                    out_r = int(r / height * output_height)
                    out_c = int(c / width * output_width)
                    if 0<= out_r < output_height and 0 <= out_c < output_width:
                      output_grid[out_r, out_c]=0
    return output_grid.tolist()

def fill_remaining(output_grid):
    """Fills remaining cells based on adjacent cells (up, down, left, right)."""
    output_grid = np.array(output_grid)
    height, width = output_grid.shape
    
    # Iterate until no more changes are made
    changed = True
    while changed:
        changed = False
        for r in range(height):
            for c in range(width):
                if output_grid[r, c] == 0:  # Only fill empty cells
                    neighbors = []
                    if r > 0:
                        neighbors.append(output_grid[r - 1, c])
                    if r < height - 1:
                        neighbors.append(output_grid[r + 1, c])
                    if c > 0:
                        neighbors.append(output_grid[r, c - 1])
                    if c < width - 1:
                        neighbors.append(output_grid[r, c + 1])

                    # Filter out zeros from neighbors and find the most frequent
                    non_zero_neighbors = [n for n in neighbors if n != 0]
                    if non_zero_neighbors:
                        most_common = Counter(non_zero_neighbors).most_common(1)[0][0]
                        output_grid[r,c] = most_common
                        changed = True #Mark that there was a change
    return output_grid.tolist()


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
    
    output_grid = insert_zeros(input_grid, output_grid)

    output_grid = fill_remaining(output_grid)


    return output_grid