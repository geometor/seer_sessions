"""
Maps non-white pixels from a partitioned input grid to a 3x3 output grid based on subgrid location.

The input grid is conceptually divided into a 3x3 grid of equally sized subgrids. 
Each subgrid in the input contains exactly one non-white pixel. 
The color of the non-white pixel found within an input subgrid is placed at the 
corresponding position in the 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on partitioning and mapping non-white pixels.

    Args:
        input_grid (list of lists): The input grid containing integer color values.

    Returns:
        list of lists: The transformed 3x3 output grid.
    """
    # Convert input list of lists to a numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    H, W = input_np.shape
    
    # Calculate subgrid dimensions
    # It's assumed H and W are divisible by 3 based on the examples
    sub_H = H // 3
    sub_W = W // 3
    
    # Initialize a 3x3 output grid with the background color (white, 0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Iterate through the 3x3 conceptual grid of subgrids
    for R_sub in range(3):
        for C_sub in range(3):
            # Define the boundaries of the current subgrid within the input grid
            start_row = R_sub * sub_H
            end_row = start_row + sub_H
            start_col = C_sub * sub_W
            end_col = start_col + sub_W
            
            # Extract the current subgrid
            subgrid = input_np[start_row:end_row, start_col:end_col]
            
            # Find the non-white pixel within the subgrid
            # Since we expect exactly one, we can find its value easily
            non_white_pixels = subgrid[subgrid > 0]
            
            # Check if exactly one non-white pixel was found (as expected)
            if len(non_white_pixels) == 1:
                pixel_value = non_white_pixels[0]
                # Place the found color value into the output grid at the corresponding position
                output_grid[R_sub, C_sub] = pixel_value
            else:
                # Handle unexpected cases (e.g., zero or multiple non-white pixels)
                # For this problem based on examples, we assume exactly one exists.
                # If not, this indicates an issue or a pattern mismatch.
                # We can leave the output cell as 0 or raise an error.
                # Let's leave it as 0 for now.
                pass 
                
    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()