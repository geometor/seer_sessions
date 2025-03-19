"""
Compares all input and output grid pairs to identify the color that changes to
green (3). Then, in the input grid, it changes only the pixels in the first
column that match the identified target color to green (3). Pixels not matching
the target color are kept unchanged.
"""

import numpy as np

def find_target_color(input_grid, output_grid):
    """
    Finds the color in the input grid that changes to green (3) in the output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != output_grid[i, j] and output_grid[i,j] == 3:
                return input_grid[i, j]
    return None

def transform(input_grid, examples):
    """
    Transforms the input grid based on the observed pattern.
    Identifies the color that changes to green (3) and applies the
    transformation:  change only the first column that matches the
    target color to green (3).
    """
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid_np = np.array(input_grid)

    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid_np)

    #find the target color for this input, based on examples.
    target_colors = []
    for example in examples:
        target_color = find_target_color(example['input'], example['output'])
        if target_color is not None:
            target_colors.append(target_color)
    # Determine what our target color *should* be.
    target_color = None
    for color in target_colors:
        if color == input_grid_np[0,0]:
            target_color = color
            break

    #if we found the target color - replace the leftmost
    if target_color is not None:
        for i in range(output_grid.shape[0]):
            if output_grid[i, 0] == target_color:
                output_grid[i, 0] = 3

    return output_grid