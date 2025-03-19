"""
The transformation involves manipulating two shapes, one azure (8) and one yellow (4), on a white (0) background grid. The yellow shape remains unchanged. The azure shape's vertical element is extended horizontally and moved upwards, while its horizontal part remains the same.

"""

import numpy as np

def find_shape(grid, color):
    # Find the coordinates of pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
      return None
    return coords

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure (8) and yellow (4) shapes.
    azure_coords = find_shape(input_grid, 8)
    yellow_coords = find_shape(input_grid, 4)

    # maintain yellow shape
    #for coord in yellow_coords:
    #    output_grid[coord[0], coord[1]] = 4

    # Transform the azure shape.
    if azure_coords is not None:
        # Find the vertical and horizontal parts of azure
        min_row = np.min(azure_coords[:, 0])
        max_row = np.max(azure_coords[:, 0])
        min_col = np.min(azure_coords[:, 1])
        max_col = np.max(azure_coords[:, 1])

        vertical_azure = []
        horizontal_azure = []
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r,c] == 8:
                    if (r == min_row):
                        vertical_azure.append( (r,c))
                    else:
                        horizontal_azure.append( (r,c))
        
        # remove the original vertical azure
        for r, c in vertical_azure:
           output_grid[r,c] = 0

        # move azure vertical parts, if found
        if len(vertical_azure) > 0:

            r, c = vertical_azure[0] # only expecting 1

            # extend one to left and right
            if c > 0:
                output_grid[r , c - 1] = 8  # Left
                output_grid[r -1, c - 1] = 8  # move up one

            if c < output_grid.shape[1] - 1:
                output_grid[r , c + 1] = 8  # Right
                output_grid[r - 1, c + 1] = 8  # move up one
                

        # maintain horizontal azure
        #for r, c in horizontal_azure:
        #    output_grid[r,c] = 8
    

    return output_grid