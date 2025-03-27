"""
Counts the total number of red (2) and yellow (4) pixels in the entire input grid.
Performs a weighted comparison: if 5 times the count of red pixels is greater than or equal 
to 3 times the count of yellow pixels, the output is a 2x2 grid filled with red (2). 
Otherwise, the output is a 2x2 grid filled with yellow (4).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a weighted count of red and yellow pixels 
    across the entire grid.
    """
    # Convert the input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Scan the entire input grid to count the total number of red pixels (color 2).
    total_red = np.sum(input_np == 2)

    # 2. Scan the entire input grid to count the total number of yellow pixels (color 4).
    total_yellow = np.sum(input_np == 4)

    # 3. Perform a weighted comparison: calculate 5 * total_red and 3 * total_yellow.
    weighted_red = 5 * total_red
    weighted_yellow = 3 * total_yellow

    # 4. If 5 * total_red is greater than or equal to 3 * total_yellow, set the output color to red (2).
    # 5. Otherwise (if 5 * total_red is less than 3 * total_yellow), set the output color to yellow (4).
    if weighted_red >= weighted_yellow:
        output_color = 2 # red
    else:
        output_color = 4 # yellow

    # 6. Create a new 2x2 grid and fill all its pixels with the determined output color.
    output_grid = np.full((2, 2), output_color, dtype=int)

    # Return as list of lists as per standard ARC format
    return output_grid.tolist() 