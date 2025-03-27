"""
1.  **Identify the Input Region:** Focus on the section of the input grid *above* the horizontal line of yellow (4) pixels.
2.  **Determine Output Size:** The output grid will have dimensions that are exactly half the height and half the width of the input region.
3.  **Extract and Transform:** Extract the upper-left quadrant of the input area, defined in terms of height and width by using the size calculation in step 2.
4.  **Recolor:** Within this extracted quadrant, change all blue (1) pixels to green (3). Leave the other color alone (white/0).
5. The output grid section corresponds to the colors of the selected area.
"""

import numpy as np

def find_yellow_row(grid):
    """Finds the row index of the first all-yellow (4) row."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return i
    return None

def transform(input_grid):
    # Find the row index separating the top section.
    yellow_row_index = find_yellow_row(input_grid)
    
    # Extract the top section of the grid.
    top_section = input_grid[:yellow_row_index]
    
    # Determine output dimensions (half height and width of the top section).
    output_height = top_section.shape[0] // 2
    output_width = top_section.shape[1] // 2
    
    # Initialize the output grid with the correct dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through the top-left quadrant and recolor.
    for i in range(output_height):
        for j in range(output_width):
            if top_section[i, j] == 1:  # If pixel is blue
                output_grid[i, j] = 3  # Change to green
            else:
                output_grid[i,j] = top_section[i,j] #copy all other

    return output_grid