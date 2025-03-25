```python
"""
1.  **Identify the Object:** Locate the contiguous region of non-zero pixels (the "object") within the 8x8 input grid. Note its color.
2.  **Bounding box:** Find the bounding box of this non-zero object, cropping away any all-zero rows/columns.
3. **Create Output:** Generate a new grid that has the height of the bounding box, with all the non-zero values from each row concatenated together, repeating values when a row has more than one pixel, with the final row being the sum of the pixels of each column.
"""

import numpy as np

def get_bounding_box(grid):
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax

def transform(input_grid):
    # convert input to numpy array
    input_grid = np.array(input_grid)

    # Find object
    rmin, rmax, cmin, cmax = get_bounding_box(input_grid)
    object_color = input_grid[rmin, cmin]

    # Create the cropped grid
    cropped = input_grid[rmin:rmax+1, cmin:cmax+1]
    
    height = cropped.shape[0]
    width = cropped.shape[1] #unused
    
    output_grid = np.zeros((3,6),dtype=int)
    
    for i in range(height):
      row_values = cropped[i,:][cropped[i,:]!=0]
      for j in range(len(row_values)):
        output_grid[i,j*2] = row_values[j]
        output_grid[i,j*2+1] = row_values[j]
    
    
    col_counts = np.sum(cropped != 0, axis=0)
    for k in range(len(col_counts)):
        if col_counts[k] >0:
            output_grid[height-1,k] = object_color
        

    return output_grid.tolist()
```