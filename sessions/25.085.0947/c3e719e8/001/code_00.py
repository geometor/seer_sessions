"""
Transforms a 3x3 input grid into a 9x9 output grid based on the most frequent color in the input.

1.  Analyze the 3x3 input grid to find the color that appears most frequently (MFC).
2.  Create a 9x9 output grid, initialized to white (0).
3.  Iterate through each cell (r, c) of the 3x3 input grid.
4.  If the color of the input cell input_grid[r][c] matches the MFC, copy the entire 3x3 input grid into the corresponding 3x3 tile in the output grid. The top-left corner of this tile is at (r*3, c*3).
5.  If the color does not match the MFC, leave the corresponding 3x3 tile in the output grid as white (0).
6.  Return the completed 9x9 output grid.
"""

import numpy as np
from collections import Counter

def find_most_frequent_color(grid):
    """Finds the most frequent color in a grid."""
    # Flatten the grid into a single list of colors
    colors = grid.flatten()
    # Count occurrences of each color
    counts = Counter(colors)
    # Find the color with the highest count
    # most_common(1) returns a list of [(element, count)], so we take the first element's element
    if not counts:
        return 0 # Default to white if grid is empty? Or handle error. Assuming non-empty based on task.
    mfc = counts.most_common(1)[0][0]
    return mfc

def transform(input_grid_list):
    """
    Transforms the input grid based on the most frequent color rule.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Get dimensions (expected to be 3x3)
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 3

    # Find the most frequent color in the input grid
    mfc = find_most_frequent_color(input_grid)

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid to determine the pattern
    for r in range(input_height):
        for c in range(input_width):
            # Check if the color of the current input cell matches the most frequent color
            if input_grid[r, c] == mfc:
                # If it matches, copy the entire input grid to the corresponding tile in the output grid
                start_row = r * input_height
                start_col = c * input_width
                end_row = start_row + input_height
                end_col = start_col + input_width
                
                output_grid[start_row:end_row, start_col:end_col] = input_grid
            else:
                # If it doesn't match, the corresponding tile remains white (0), 
                # which is the default initialization value. No action needed.
                pass 

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
