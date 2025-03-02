"""
1.  **Find Azure:** Locate the first occurrence of an azure (value 8) pixel within the input grid.
2.  **Extract Subgrid:** If an azure pixel is found, extract a subgrid centered on that pixel. The dimensions of the subgrid should match the available pixels, up to a maximum of 3x3.
3.  **Create Output.** Create 3x3 output grid.
4.  **Copy Centered:** Copy the extracted grid to the output grid, centering it. If no azure pixel exists the output should be all zeros. If there are less than 3 rows or 3 columns centered on the azure, the output will be less than 3x3, copy it centered within the 3x3.
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
    # Extract the subgrid centered on the given coordinates.

    if center_coord is None: # No azure
        return np.zeros((3, 3), dtype=int)

    row, col = center_coord
    
    start_row = row - 1
    start_col = col - 1
    end_row = row + 2
    end_col = col + 2

    extracted_grid = grid[max(0,start_row):min(grid.shape[0],end_row), max(0,start_col):min(grid.shape[1],end_col)]
    
    return extracted_grid
    

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the first azure pixel.
    azure_coord = find_first_azure_pixel(input_grid)

    # Extract the subgrid centered on the azure pixel.
    extracted_grid = extract_centered_subgrid(input_grid, azure_coord)

    # Create a 3x3 output grid of zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    if azure_coord is not None:
        # Calculate the starting row and column for centering the extracted grid.
        height, width = extracted_grid.shape
        start_row = (3 - height) // 2
        start_col = (3 - width) // 2

        # Copy the extracted grid into the center of the output grid.
        output_grid[start_row:start_row+height, start_col:start_col+width] = extracted_grid

    return output_grid.tolist()