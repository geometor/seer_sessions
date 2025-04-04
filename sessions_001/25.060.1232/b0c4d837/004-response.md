# b0c4d837 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Target:** Locate all azure (8) pixels within the input grid.
2.  **Bounding Box:** Determine the smallest rectangular region (bounding box) that encloses all the identified azure pixels.
3.  **Extraction:** Extract the sub-grid defined as follows.
    *   The top row of the sub-grid should be the row that contains the azure pixels.
    *   The sub-grid should have 3 columns, starting from the first column containing azure.
4. **Output Construction:** The extracted sub-grid and resize/crop it to a 3x3, keeping only original pixels in the process.
"""

import numpy as np

def find_azure_pixels(grid):
    # Find coordinates of all azure (8) pixels.
    azure_coords = np.argwhere(grid == 8)
    return azure_coords

def extract_subgrid(grid, azure_coords):
    # Extract the relevant subgrid based on azure pixel locations.

    if len(azure_coords) == 0: # No azure
        return np.zeros((3, 3), dtype=int)

    min_row = np.min(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])

    
    start_row = min_row
    start_col = min_col
    end_row = start_row+3
    end_col = start_col+3

    #print (f'{start_row=}')
    #print (f'{start_col=}')
    #print (f'{end_row=}')
    #print (f'{end_col=}')

    extracted_grid = grid[start_row:end_row, start_col:end_col]

    height, width = extracted_grid.shape

    # Create a new 3x3 grid
    new_grid = np.zeros((3, 3), dtype=int)
    
    # Copy the values from the extracted grid
    for i in range(min(3,height)):
       for j in range(min(3,width)):
          new_grid[i,j]=extracted_grid[i,j]    

    return new_grid

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find azure pixels.
    azure_coords = find_azure_pixels(input_grid)

    # Extract the subgrid.
    output_grid = extract_subgrid(input_grid, azure_coords)

    return output_grid.tolist()
```
