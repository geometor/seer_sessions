"""
The transformation rule identifies all 3x3 subgrids within the input grid that consist entirely of white (0) pixels. 
It then iterates through these potential 3x3 white squares based on their top-left corner position, scanning rows from top to bottom, and columns from left to right within each row.
For each potential 3x3 white square found in the input:
1. It checks if any pixel within the corresponding 3x3 area in the *output grid* has already been changed to blue (1) by a previous step (indicating an overlap with a higher-priority square).
2. If the input 3x3 subgrid is all white AND the corresponding output 3x3 area contains NO blue pixels, then the 3x3 area in the output grid is filled with blue (1) pixels.
Otherwise, the area is left unchanged. Pixels outside of any transformed 3x3 area remain identical to the input grid. This process ensures that in cases of overlapping 3x3 white squares in the input, only the one encountered first during the scan (top-most, then left-most) gets transformed.
"""

import numpy as np

def transform(input_grid):
    """
    Identifies 3x3 blocks of white (0) pixels in the input grid. If found, checks if the 
    corresponding area in the output grid has already been modified (is blue). 
    If not modified, replaces the 3x3 block with blue (1) pixels in the output grid.
    This handles overlaps by prioritizing the first encountered block in a top-down, left-right scan.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    height, width = input_grid.shape
    
    # Define the target color (white) and replacement color (blue)
    target_color = 0
    replacement_color = 1
    
    # Iterate through all possible top-left corner positions (r, c) for a 3x3 subgrid
    # The loops stop at height-2 and width-2 to ensure the 3x3 subgrid fits within the grid boundaries.
    # The order of iteration (top-down, left-right) provides the priority mechanism.
    for r in range(height - 2):
        for c in range(width - 2):
            # Extract the 3x3 subgrid from the input grid
            input_subgrid = input_grid[r:r+3, c:c+3]
            
            # Extract the corresponding 3x3 subgrid from the *current* output grid
            # This is used to check for overlaps with previously transformed squares.
            output_subgrid = output_grid[r:r+3, c:c+3]
            
            # Check if the input subgrid is all the target color (white)
            is_target_subgrid = np.all(input_subgrid == target_color)
            
            # Check if the corresponding area in the output grid has already been modified (contains blue)
            # If any pixel is already the replacement color, it means an overlapping, higher-priority square
            # has already been processed.
            is_already_transformed = np.any(output_subgrid == replacement_color)
            
            # Perform the transformation only if:
            # 1. The input subgrid matches the target (all white).
            # 2. The corresponding output area has NOT already been transformed (no blue pixels yet).
            if is_target_subgrid and not is_already_transformed:
                # Replace the corresponding area in the output grid with the replacement color (blue)
                output_grid[r:r+3, c:c+3] = replacement_color
                
    # Return the final modified output grid
    return output_grid