"""
1.  **Identify Azure Pixels:** Locate all azure (8) pixels within the input grid.
2.  **Centering:** The output is always a 3x3 grid. The azure pixel, if it exists, will *always* be in the center of the 3x3 output grid (at position [1,1]).
3.  **Extraction:** Select the 3x3 subgrid centered *on* the *first* azure pixel found. If there are no azure pixels, return a 3x3 grid of all zeros. If the centering would cause the subgrid to go out of bounds, use available.
"""

import numpy as np

def find_first_azure_pixel(grid):
    # Find coordinates of all azure (8) pixels.
    azure_coords = np.argwhere(grid == 8)
    if len(azure_coords) > 0:
       return azure_coords[0]
    else:
      return None

def extract_centered_subgrid(grid, center_coord):
    # Extract the 3x3 subgrid centered on the given coordinates.

    if center_coord is None: # No azure
        return np.zeros((3, 3), dtype=int)

    row, col = center_coord
    
    start_row = row - 1
    start_col = col - 1
    end_row = row + 2
    end_col = col + 2

    extracted_grid = grid[max(0,start_row):min(grid.shape[0],end_row), max(0,start_col):min(grid.shape[1],end_col)]
    
    height, width = extracted_grid.shape
    new_grid = np.zeros((3, 3), dtype=int)

    # Copy, handling boundaries
    for i in range(min(3,height)):
       for j in range(min(3,width)):
          new_grid[i,j]=extracted_grid[i,j] 

    return new_grid
    

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the first azure pixel.
    azure_coord = find_first_azure_pixel(input_grid)

    # Extract the 3x3 subgrid centered on the azure pixel.
    output_grid = extract_centered_subgrid(input_grid, azure_coord)

    return output_grid.tolist()