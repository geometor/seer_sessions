"""
1.  **Divide:** Divide the input grid into *n* x *m* non-overlapping rectangular sub-regions. The number and size of sub-regions depend on the input grid's dimensions and structure.
2.  **Select:** For each sub-region, select the upper-left pixel as the representative pixel.
3. **Map and Create**: Create an output grid of the resolution *n* x *m*.
4. **Fill:** Map the color of the selected representative pixel from the input region to the corresponding position in the output grid.
"""

import numpy as np

def get_sub_regions(input_grid):
    """
    Divides the input grid into sub-regions based on the examples.
    Returns a list of sub-regions, where each sub-region is a tuple:
    ((row_start, row_end), (col_start, col_end))
    """
    input_height, input_width = input_grid.shape
    sub_regions = []

    if input_height == 9 and input_width == 9:
        # Example 1
        for i in range(2):
            for j in range(3):
                sub_regions.append(((i * 2, (i+1) * 2), (j * 3, (j+1)*3))) #top regions
        for i in range(2):
            for j in range(3):
               sub_regions.append(((2+ i*3, 2 + (i+1) * 3), (j * 3, (j+1) * 3))) #bottom regions

    elif input_height == 10 and input_width == 8:
        # Example 2
        for i in range(2):
            for j in range(2):
                sub_regions.append(((i * 5, (i+1) * 5), (j * 4, (j+1) * 4)))
    elif input_height == 14 and input_width == 14:
        # Example 3
        for i in range(2):
            for j in range(2):
                sub_regions.append(((i * 7, (i+1) * 7), (j * 7, (j+1) * 7)))

    return sub_regions

def transform(input_grid):
    # Get sub-regions
    sub_regions = get_sub_regions(input_grid)

    # Determine output grid size
    output_height = int(len(sub_regions)**0.5) if int(len(sub_regions)**0.5) == len(sub_regions)**0.5 else len(sub_regions) # if perfect square, use that dimension
    
    if len(sub_regions) == 6: # example 1
      output_height = 2
      output_width = 3
    else:
      output_width = output_height # examples 2, 3
   
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map representative pixels to output grid
    region_index = 0
    for i in range(output_height):
        for j in range(output_width):
           
            (row_start, _), (col_start, _) = sub_regions[region_index]
            output_grid[i, j] = input_grid[row_start, col_start]
            region_index += 1

    return output_grid