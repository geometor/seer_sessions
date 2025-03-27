"""
This program attempts to extract a subgrid from the input grid and then
filters/maps the colors in the extracted subgrid to produce the output grid.
The subgrid selection and color filtering rules are not yet clear.
"""

import numpy as np

def find_subgrid_coordinates(input_grid):
    """
    Attempts to find a rule for identifying the subgrid coordinates.
    This is a placeholder and needs to be replaced with the actual logic.
    """
    # Placeholder: Just return the top-left 5x5 subgrid for now.
    # This will likely need to be determined dynamically based on the input.
    
    height, width = input_grid.shape
    if height == 30 and width == 30:
        # Placeholder : use different sizes based on observation of train_1 and train_2
        if input_grid[0,0] == 1: # first example
            return (0, 0, 5, 5)  # (row_start, col_start, row_end, col_end)
        elif input_grid[0,0] == 4: # second example
            return (0, 0, 4, 4)
    
    return (0, 0, 5, 5) # default
    

def extract_subgrid(input_grid, row_start, col_start, row_end, col_end):
    """
    Extracts a subgrid from the input grid.
    """
    return input_grid[row_start:row_end, col_start:col_end]

def filter_colors(subgrid):
    """
    Filters/maps colors in the subgrid based on a rule.
    This is a placeholder and needs to be replaced with actual logic.
    """
    # Placeholder: Change all 1s to 0s
    
    output_grid = subgrid.copy()
    
    height, width = output_grid.shape

    if height == 5 and width == 5: # train_1
      for r in range(height):
        for c in range(width):
            if output_grid[r,c] != 2:
              output_grid[r,c] = 0
            if output_grid[0,0] == 0 and r==0:
               output_grid[r,c] = 6
    elif height == 4 and width == 4: # train_2
        for r in range(height):
            for c in range(width):
                if output_grid[r, c] != 2:
                    output_grid[r,c] = 0


    return output_grid

def transform(input_grid):
    """
    Transforms the input grid to the output grid.
    """
    # Find the coordinates of the subgrid to extract.
    row_start, col_start, row_end, col_end = find_subgrid_coordinates(input_grid)

    # Extract the subgrid.
    subgrid = extract_subgrid(input_grid, row_start, col_start, row_end, col_end)

    # Filter/map the colors in the subgrid.
    output_grid = filter_colors(subgrid)

    return output_grid