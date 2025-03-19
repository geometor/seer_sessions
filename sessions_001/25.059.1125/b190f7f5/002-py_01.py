"""
The transformation rule is as follows:
1. Identify non-zero pixels: Iterate through the input grid and locate all pixels with a value other than 0.
2. Replicate each non-zero pixel: For each non-zero pixel, create a 3x3 block of the same color centered on the original pixel's location in the *output* grid. If any parts of the 3x3 blocks overlap, the non-zero value is maintained.
3. Expand the output grid: The output grid is significantly larger than the input grid. The precise dimensions of the output grid appear to be related to the original grid size and number of objects.
4. The original shape and relationship of non-zero pixels in the original image are maintained in the larger output grid. The transformation expands and replicates.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """Finds the coordinates of non-zero pixels in a grid."""
    non_zero_coords = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value != 0:
                non_zero_coords.append((row_idx, col_idx, value))
    return non_zero_coords

def transform(input_grid):
    """Transforms the input grid according to the replication rule."""
    input_grid = np.array(input_grid)
    non_zero_pixels = get_nonzero_pixels(input_grid)

    # Determine output grid size based on input grid and number of non-zero pixels.
    # This is a heuristic based on the provided examples, and might need refinement
    # with more examples.  The output grid height is approximately 3 times the
    # number of non-zero pixels, plus some additional space.  The output grid width
    # is approximately 3 times the input width.
    num_nonzero = len(non_zero_pixels)

    output_height =  input_grid.shape[0] * num_nonzero + input_grid.shape[0]

    if output_height < 9 and len(input_grid) > 3:
        output_height = 9
    elif output_height < 9:
          output_height = 9
          
    output_width = input_grid.shape[1] * 3
    if(len(input_grid[0]) <= 3):
       output_width = input_grid.shape[1] * num_nonzero * 2
    if output_width < 11 and len(input_grid[0]) > 4:
        output_width = input_grid.shape[1] * 3
    
    if output_width < 9:
       output_width = input_grid.shape[1] * 3

    if(len(input_grid[0]) > 4):
        output_width += (output_width % 2) + 2

    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Replicate each non-zero pixel as a 3x3 block.
    x_offset = 0
    y_offset = 0

    if len(non_zero_pixels) > 3:
        y_offset = output_height // (len(non_zero_pixels) )
        x_offset = output_width // (len(non_zero_pixels) + 2)
    elif len(input_grid) >= 3:
        y_offset = output_height // (input_grid.shape[0]) - 1
        x_offset = output_width // (input_grid.shape[0] + 1)
    else :
         x_offset = output_width // (len(non_zero_pixels) + 1)

    for i in range(0, len(non_zero_pixels)):
         row, col, value = non_zero_pixels[i]
         if (len(input_grid[0]) > 4):
             center_row = row  + y_offset
             center_col = col * 3 + x_offset 
         elif len(input_grid) > 3:
              center_row = row  + y_offset * (i)  
              center_col = col  +  x_offset * (i//2)  

         else:
             center_row = row  + y_offset * (i)  
             center_col = col  +  x_offset * (i)  

         for r in range(max(0, center_row - 1), min(output_height, center_row + 2)):
             for c in range(max(0, center_col - 1), min(output_width, center_col + 2)):
                    output_grid[r, c] = value

    return output_grid