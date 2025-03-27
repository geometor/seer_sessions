"""
The transformation involves identifying vertical runs of gray pixels, replacing all gray pixels in those runs with blue pixels, and adding a red pixel at the bottom of the rightmost run. If the rightmost run contains only one gray pixel, a red pixel is placed at the bottom of the leftmost run instead.
"""

import numpy as np

def get_vertical_runs(grid, color):
    """
    Finds all contiguous vertical runs of a specified color in the grid.
    Returns a list of runs, where each run is a list of (row, col) tuples.
    """
    height, width = grid.shape
    runs = []
    for col in range(width):
        current_run = []
        for row in range(height):
            if grid[row, col] == color:
                current_run.append((row, col))
            else:
                if current_run:
                    runs.append(current_run)
                    current_run = []
        if current_run:  # Handle run at the end of the column
            runs.append(current_run)
    return runs

def transform(input_grid):
    """
    Transforms the input grid by changing the color of all gray pixels in vertical runs to blue,
    and adds a red pixel to the right-most vertical run of the replaced pixels, unless
    the run has only one gray pixel, in which case the red is added to the bottom of the
    left-most run.
    """
    output_grid = np.copy(input_grid)
    gray_runs = get_vertical_runs(input_grid, 5)

    # Replace all gray pixels in runs with blue
    for run in gray_runs:
        for row, col in run:
            output_grid[row, col] = 1  # blue

    # Add red pixel
    if gray_runs:
        #find right-most run by last element's column
        rightmost_run = max(gray_runs, key=lambda run: run[-1][1])
        #find left-most run
        leftmost_run = min(gray_runs, key=lambda run: run[0][1])

        if len(rightmost_run) == 1:
          target_run = leftmost_run
        else:
          target_run = rightmost_run

        last_row, last_col = target_run[-1]
        #add only if not exceeding bounds
        if last_row + 1 < output_grid.shape[0]:
           output_grid[last_row + 1, last_col] = 2


    return output_grid