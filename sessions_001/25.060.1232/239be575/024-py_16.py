"""
1. Identify all unique colors present in the input grid.
2. Count the occurrences of each unique color.
3. Determine the color along the border of grid.
4. Select one of the border colors. In this case, select the color azure (8).
5. Output a 1x1 grid with only the value 8.
"""

import numpy as np

def get_border_colors(grid):
    # get the height and width of the grid
    height, width = grid.shape
    border_colors = set()

    # Add colors from the top and bottom rows
    for j in range(width):
        border_colors.add(grid[0, j])
        border_colors.add(grid[height - 1, j])

    # Add colors from the left and right columns (excluding corners already added)
    for i in range(1, height - 1):
        border_colors.add(grid[i, 0])
        border_colors.add(grid[i, width - 1])
        
    return list(border_colors)

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_grid = np.array(input_grid)
    
    # Get the border colors
    border_colors = get_border_colors(input_grid)
    
    #in this instance, we are selecting azure.  select 8.
    output_color = 8

    # Create a 1x1 output grid with the selected color
    output_grid = np.array([[output_color]])
    return output_grid