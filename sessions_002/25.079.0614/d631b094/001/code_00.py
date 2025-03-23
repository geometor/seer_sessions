"""
1. **Identify the Prominent Color:** Examine the input grid and find the single non-zero color (the "prominent color").
2. **Count Occurrences:** Count the number of times the prominent color appears in the input grid.
3. **Determine Output Size:** The count from step 2 determines size. Specifically the output will have x * x cells, where x is the number of non zero input cells
4. **Create Output Grid:** Create a new grid filled with the prominent color.
5. **Return:** output the generated grid.
"""

import numpy as np

def get_prominent_color(grid):
    # Flatten the grid and get unique values
    unique_values = np.unique(grid)
    # Find the non-zero color
    for value in unique_values:
        if value != 0:
            return value
    return 0  # Return 0 if no prominent color is found

def transform(input_grid):
    # Find prominent color
    prominent_color = get_prominent_color(input_grid)

    # Handle case where there is no prominent color.
    if prominent_color == 0:
      return np.array([[0]])

    # Count the number of times prominent color appears
    count = np.count_nonzero(input_grid == prominent_color)

    # determine dimensions
    if count > 0 :
        width = count
    
    # Create the output grid and populate
    output_grid = np.full((1,width), prominent_color)


    return output_grid