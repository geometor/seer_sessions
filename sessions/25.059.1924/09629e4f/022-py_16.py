"""
The transformation rule is as follows:

1.  **Identify Constant Lines:** Recognize the horizontal lines of '5' (grey) pixels at rows 4 and 8 (using 1-based indexing). These lines remain unchanged in the output.

2.  **Divide into Regions:** Divide the input grid into three regions based on the constant lines:
    *   Region 1: Rows 1-3
    *   Region 2: Rows 5-7
    *   Region 3: Rows 9-11

3.  **Process Each Region:** For each of the three regions:
    *   Identify the columns with non-zero values, ignoring the gray '5' columns. Let's call this 'active_columns'
    *   Create 3x3 blocks with all colors set to 0 and the input columns marked by color '5' are the same in the ouput.
    *   Find the non-zero colors within active columns.
    *    Create a block that combines these colors using a 3x3 block, keeping the relative position.
    *   Fill output for the region with these blocks and zero background.

4.  **Combine Regions:** Combine the processed regions and the constant lines to form the final output grid.

"""

import numpy as np

def get_regions(grid):
    """Divides the grid into regions based on constant lines."""
    regions = []
    constant_lines = []
    for i, row in enumerate(grid):
        if np.all(row == 5):
            constant_lines.append(i)
    regions.append(grid[:constant_lines[0]])
    regions.append(grid[constant_lines[0]+1:constant_lines[1]])
    regions.append(grid[constant_lines[1]+1:])

    return regions, constant_lines

def process_region(region):
     #Create an output region initialized to 0
    output_region = np.zeros_like(region)
    
    #Identify active (non-zero and non-5) columns
    active_columns = []
    for j in range(region.shape[1]):
         if any(region[i][j] != 0 and region[i][j] !=5 for i in range(region.shape[0])):
              active_columns.append(j)

    # fill in 3x3 blocks
    if len(active_columns) > 0 :
      #find the center for the block
      center_col = active_columns[len(active_columns)//2]
      #iterate 3 times
      for row_index in range(3):
        #find columns and distinct colors
        colors = []
        for col_index in range(region.shape[1]):
            if region[row_index][col_index] != 0 and region[row_index][col_index] != 5:
                if region[row_index][col_index] not in colors:
                    colors.append(region[row_index][col_index])

        #fill in the output matrix
        for idx,color in enumerate(colors):
          if(len(colors) > 0):
              output_region[row_index,center_col-1+idx] = color

      #copy '5' column to output
      for col_index in range(region.shape[1]):
            if 5 in region[:, col_index]:
              output_region[:,col_index] = 5
    
    return output_region

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Get regions and constant lines
    regions, constant_lines = get_regions(input_grid)

    # Initialize output grid
    output_grid = np.zeros_like(input_grid)

    # Process each region
    processed_regions = []
    for region in regions:
        processed_regions.append(process_region(region))

    # Combine regions and constant lines
    output_grid[:constant_lines[0]] = processed_regions[0]
    output_grid[constant_lines[0]] = input_grid[constant_lines[0]]  # Constant line
    output_grid[constant_lines[0]+1:constant_lines[1]] = processed_regions[1]
    output_grid[constant_lines[1]] = input_grid[constant_lines[1]] # Constant line
    output_grid[constant_lines[1]+1:] = processed_regions[2]
    
    return output_grid.tolist()