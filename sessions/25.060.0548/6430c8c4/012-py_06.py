"""
1.  **Initialization:** Create a 2x2 output grid filled with black (0) pixels.
2.  **Orange Pixel Check:** Examine the input grid. If there are *any* orange (7) pixels present, proceed to the next step.
3.  **Green Pixel Placement:** If orange pixels are present, place green (3) pixels at positions (0, 1) and (1, 0) in the output grid.
4. Examine input for any colors that are not orange, black or green. If any such colors exist, then do not place any green.
5.  **Output:** The 2x2 output grid is the final result.
"""

import numpy as np

def transform(input_grid):
    # Initialize 2x2 output grid with zeros
    output_grid = np.zeros((2, 2), dtype=int)
    
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Check for presence of orange pixels
    orange_present = np.any(input_grid == 7)

    # Check for presence of colors other than black, orange and green.
    other_colors_present = False
    unique_colors = np.unique(input_grid)
    for color in unique_colors:
      if color != 0 and color != 7 and color != 3:
        other_colors_present = True
        break

    # Place green pixels if orange is present AND other colors are not present
    if orange_present and not other_colors_present:
        output_grid[0, 1] = 3
        output_grid[1, 0] = 3

    return output_grid