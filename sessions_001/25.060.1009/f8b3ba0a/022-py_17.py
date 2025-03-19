"""
1.  **Identify Subgrids:** Scan the input grid to locate all 3x2 subgrids where all pixels are non-zero.
2.  **Check for Uniform Region:** Within each identified 3x2 subgrid, check if there exists any 1x2 sub region made of a single, uniform, non-zero color.
3. **Extract Colors:** If step 2 is true, extract colors from this region.
4.  **Output List:** Create an ordered list of the colors, possibly ordering them by appearance from top to bottom.
"""

import numpy as np

def find_3x2_subgrids(grid):
    """Finds all 3x2 subgrids with non-zero pixels."""
    subgrids = []
    height, width = grid.shape
    for i in range(height - 2):
        for j in range(width - 1):
            subgrid = grid[i:i+3, j:j+2]
            if np.all(subgrid != 0):
                subgrids.append((i, j, subgrid))
    return subgrids

def check_uniform_1x2_region(subgrid):
    """Checks for a 1x2 uniform region within a 3x2 subgrid."""
    for i in range(3):
        # check horizontal
        if subgrid[i,0] == subgrid[i,1] and subgrid[i,0] != 0 :
            return subgrid[i,0]
        
    # Check vertical 1x2 regions
    for j in range(2):
      if subgrid[0,j] == subgrid[1,j] and subgrid[0,j] != 0:
        return subgrid[0,j]
      if subgrid[1,j] == subgrid[2,j] and subgrid[1,j] != 0:
        return subgrid[1,j]
            
    return None

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)

    # Find 3x2 subgrids
    subgrids = find_3x2_subgrids(grid)

    # Extract colors from uniform regions
    extracted_colors = []
    for i, j, subgrid in subgrids:
        color = check_uniform_1x2_region(subgrid)
        if color is not None:
            extracted_colors.append( (i, color) )

    # sort by row
    extracted_colors.sort()
    
    # Create output list
    output_list = [color for _, color in extracted_colors]
    
    # remove duplicates
    output_list_no_duplicates = []
    for color in output_list:
        if color not in output_list_no_duplicates:
            output_list_no_duplicates.append(color)

    return output_list_no_duplicates