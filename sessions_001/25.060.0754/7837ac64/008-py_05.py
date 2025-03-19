"""
Finds the first co-occurrence of blue (1) and green (3) pixels in the input grid, starting from the top-left.
Then, creates a 3x3 output grid: the top-left corner of output is always blue, and the top-right is always green.
Everything else is white.
"""

import numpy as np

def find_first_occurrence(grid, target_colors):
    """
    Finds the row and column indices of the first occurrence of target colors.
    
    Args:
        grid: input grid
        target_colors: list of colors we are searching for

    Returns:
        A tuple of tuples: ((row_1, col_1), (row_2, col_2)) for the first occurrence of each target color,
                           or (None, None) for a color if it's not found.
    """
    
    first_occurrences = {}
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value in target_colors and value not in first_occurrences:
                first_occurrences[value] = (row_index, col_index)
        
    for color in target_colors:
        if color not in first_occurrences:
            first_occurrences[color] = (None, None)  # Handle colors not found

    return (first_occurrences[target_colors[0]], first_occurrences[target_colors[1]])

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Initialize the output grid as all zeros (white)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find first occurrences of blue (1) and green (3)
    blue_first, green_first = find_first_occurrence(input_array, [1,3])
    
    if blue_first[0] is not None:
        output_grid[0,0] = 1
    if green_first[0] is not None:
        output_grid[0,2] = 3

    return output_grid.tolist()