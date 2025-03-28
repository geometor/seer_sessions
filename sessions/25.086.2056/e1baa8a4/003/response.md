```python
"""
Transforms an input grid composed of solid-colored rectangular blocks into a smaller 
output grid where each cell represents one block from the input. The transformation 
identifies the grid structure based on color changes between adjacent cells, 
determines the dimensions of the block layout, and samples the color from the 
top-left corner of each block region in the input grid to create the output grid.

Workflow:
1. Convert the input list of lists into a NumPy array.
2. Identify Row Boundaries: Find all unique row indices `r` (including 0) where 
   a vertical color change occurs (i.e., the color at `(r, c)` is different 
   from `(r-1, c)` for any column `c`, or `r=0`). Sort these indices.
3. Identify Column Boundaries: Find all unique column indices `c` (including 0) 
   where a horizontal color change occurs (i.e., the color at `(r, c)` is 
   different from `(r, c-1)` for any row `r`, or `c=0`). Sort these indices.
4. Determine Output Dimensions: The output grid height is the number of unique 
   row boundaries found. The output grid width is the number of unique column 
   boundaries found.
5. Create Output Grid: Initialize an empty NumPy array with the calculated 
   output dimensions.
6. Populate Output Grid: Iterate through the output grid cells `(out_r, out_c)`. 
   For each cell, find the corresponding input grid start row `in_r` (the 
   `out_r`-th sorted row boundary) and start column `in_c` (the `out_c`-th 
   sorted column boundary). Assign the color from the input grid at `(in_r, in_c)` 
   to the output grid cell `(out_r, out_c)`.
7. Convert the NumPy output grid back to a list of lists and return it.
"""

import numpy as np
from typing import List

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Summarizes a grid of colored rectangular blocks into a smaller grid 
    representing the block layout and colors by sampling at boundary intersections.
    """
    # Convert input to NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # --- 1. Identify Row Boundaries ---
    row_boundaries = {0} # Always include the first row
    # Check for color changes between row r and r-1
    for r in range(1, height):
        if np.any(input_np[r, :] != input_np[r - 1, :]):
            row_boundaries.add(r)
    sorted_row_boundaries = sorted(list(row_boundaries))

    # --- 2. Identify Column Boundaries ---
    col_boundaries = {0} # Always include the first column
    # Check for color changes between column c and c-1
    for c in range(1, width):
         if np.any(input_np[:, c] != input_np[:, c - 1]):
            col_boundaries.add(c)
    sorted_col_boundaries = sorted(list(col_boundaries))

    # --- 3. Determine Output Dimensions ---
    output_height = len(sorted_row_boundaries)
    output_width = len(sorted_col_boundaries)

    # --- 4. Create Output Grid ---
    # Initialize with zeros, assuming 0 is background or not a block color. 
    # This matches the previous code's initialization.
    output_np = np.zeros((output_height, output_width), dtype=int) 

    # --- 5. Populate Output Grid ---
    # Iterate through the indices of the boundary lists, which correspond to output coordinates
    for out_r, in_r in enumerate(sorted_row_boundaries):
        for out_c, in_c in enumerate(sorted_col_boundaries):
            # Sample the color from the input grid at the boundary intersection
            output_np[out_r, out_c] = input_np[in_r, in_c]

    # --- 6. Return Output ---
    # Convert back to list of lists format
    output_grid = output_np.tolist()
    
    return output_grid
```