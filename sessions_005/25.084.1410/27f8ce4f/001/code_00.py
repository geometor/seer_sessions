import numpy as np
from collections import Counter

"""
Transforms an input grid into an output grid nine times its size (3x height, 3x width).
The transformation involves identifying the most frequent non-background (non-zero) color 
in the input grid. If there's a tie, the color with the lowest numerical value is chosen.
This chosen color is designated the "pattern color". 
The output grid is initially filled with the background color (0). Then, for each cell 
in the input grid that contains the pattern color, a copy of the entire input grid 
is placed onto the corresponding 3x3 subgrid location in the output grid.
"""

def find_pattern_color(grid):
    """
    Finds the most frequent non-background color in the grid.
    Breaks ties by choosing the smallest numerical value.
    Returns None if only background color (0) is present.
    """
    counts = Counter()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Exclude background color
                counts[color] += 1

    if not counts:
        return None  # No non-background colors found

    max_freq = 0
    for color in counts:
        if counts[color] > max_freq:
            max_freq = counts[color]

    most_frequent_colors = []
    for color in counts:
        if counts[color] == max_freq:
            most_frequent_colors.append(color)
            
    # Tie-breaking: choose the color with the minimum numerical value
    if not most_frequent_colors: # Should not happen if counts is not empty
        return None
        
    pattern_color = min(most_frequent_colors)
    return pattern_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    input_h, input_w = input_np.shape

    # Calculate output dimensions
    output_h = input_h * 3
    output_w = input_w * 3

    # Initialize output grid with background color (0)
    output_grid = np.zeros((output_h, output_w), dtype=int)

    # Step 1: Find the pattern color in the input grid
    pattern_color = find_pattern_color(input_np)

    # If no pattern color found (e.g., input is all zeros), return the empty output grid
    if pattern_color is None:
        return output_grid.tolist() # Return as list of lists

    # Step 2: Populate the output grid based on the pattern color locations
    for r in range(input_h):
        for c in range(input_w):
            # If the current input cell contains the pattern color
            if input_np[r, c] == pattern_color:
                # Calculate the top-left corner for placing the input grid copy
                start_row = r * input_h
                start_col = c * input_w
                end_row = start_row + input_h
                end_col = start_col + input_w

                # Copy the entire input grid to the calculated subgrid location
                output_grid[start_row:end_row, start_col:end_col] = input_np

    # Return the final output grid as a list of lists
    return output_grid.tolist()