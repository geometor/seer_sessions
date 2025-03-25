"""
1.  **Divide:** Split the input grid into two sections at the horizontal line of yellow (4) pixels.
2.  **Identify Top Section:** Focus on the section *above* the yellow line.
3. **Determine Output Grid:** Create new output grid of white (0) pixels that has 4 columns and the number of rows equal to the top section.
4.  **Locate Shape Pixels:** Within the top section, find all orange (7) pixels.
5.  **Define Shape:** Determine the shape formed by those orange pixels and change them to green(3), set other values in the top section to white(0).
6. **Replicate the shape:** Copy the green shape to the output grid.
"""

import numpy as np

def get_top_section(grid):
    """Finds the row index of '4's and returns the grid section above it."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return grid[:i]
    return grid  # Return entire grid if no row of '4's, as per updated logic

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Divide and 2. Identify Top Section
    top_section = get_top_section(input_grid)
    
    # 3. Determine Output Grid Dimensions
    rows = len(top_section)
    output_grid = np.zeros((rows, 4), dtype=int)

    # 4. Locate Shape Pixels and 5. Define Shape, and 6. Replicate.
    for i in range(rows):
        for j in range(top_section.shape[1]):
            if top_section[i, j] == 7:
                if j < 4 :
                  output_grid[i, j] = 3
            
    return output_grid