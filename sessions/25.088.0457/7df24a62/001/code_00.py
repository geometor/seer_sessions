import numpy as np
import itertools

"""
Fill rectangular areas defined by pairs of yellow pixels.

The transformation rule identifies all yellow pixels (color 4) in the input grid. 
For every unique pair of yellow pixels, it defines the smallest bounding rectangle 
that encloses both pixels. Then, it iterates through all cells within each 
bounding rectangle. If a cell within a rectangle corresponds to a white pixel (color 0) 
in the original input grid, that cell's color is changed to blue (color 1) in the 
output grid. Original yellow and blue pixels are preserved. This process is 
applied cumulatively for all pairs of yellow pixels.
"""

def find_pixels_by_color(grid, color_value):
    """
    Finds the coordinates of all pixels with a specific color value.

    Args:
        grid (np.array): The input grid.
        color_value (int): The color value to search for.

    Returns:
        list: A list of (row, col) tuples for pixels matching the color_value.
    """
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Transforms the input grid by filling bounding boxes defined by pairs of 
    yellow pixels with blue pixels, where the original pixel was white.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the coordinates of all yellow pixels (color 4)
    yellow_pixels = find_pixels_by_color(input_grid, 4)
    
    # If there are fewer than 2 yellow pixels, no boxes can be formed.
    if len(yellow_pixels) < 2:
        return output_grid

    # Iterate through all unique pairs of yellow pixel coordinates
    for (r1, c1), (r2, c2) in itertools.combinations(yellow_pixels, 2):
        
        # Determine the bounding box coordinates
        min_r = min(r1, r2)
        max_r = max(r1, r2)
        min_c = min(c1, c2)
        max_c = max(c1, c2)
        
        # Iterate through all cells within this bounding box
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Check the color in the original input grid
                if input_grid[r, c] == 0:  # If the pixel was white
                    # Change the corresponding pixel in the output grid to blue (1)
                    output_grid[r, c] = 1
                    
    return output_grid