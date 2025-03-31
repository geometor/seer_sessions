import numpy as np

"""
Transformation Rule Description (derived from train_1):

1. Initialize the output grid as a copy of the input grid.
2. Identify the significant source row in the input, which is row 3.
3. Iterate through each column index `c` from 0 to width-1.
4. Examine the pixel at the input location (3, `c`). Let its color be `v`.
5. If the color `v` is not the background color maroon (9):
    a. Determine the destination row `dest_r` based on the column index `c`.
       - If `c` modulo 8 is equal to 1, set `dest_r` to 6.
       - Otherwise (if `c` modulo 8 is not equal to 1), set `dest_r` to 0.
    b. Update the output grid:
       - Set the pixel at location (`dest_r`, `c`) to the color `v`.
       - Set the pixel at the original location (3, `c`) to the background color maroon (9).
6. Pixels not involved in this move operation remain unchanged from the initial copy.
7. Return the modified output grid.
"""

def transform(input_grid):
    """
    Moves specific pixels from row 3 to either row 0 or row 6 based on their column index modulo 8.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Define the source row and background color
    source_row = 3
    background_color = 9
    
    # Define destination rows based on the modulo condition
    dest_row_mod_1 = 6
    dest_row_other = 0
    
    # Define the modulo base
    mod_base = 8
    
    # Iterate through the columns of the source row
    for c in range(width):
        # Get the pixel color from the input grid at the source location
        pixel_color = input_grid[source_row, c]
        
        # Check if the pixel is not the background color
        if pixel_color != background_color:
            # Determine the destination row based on the column index modulo mod_base
            if c % mod_base == 1:
                dest_r = dest_row_mod_1
            else:
                dest_r = dest_row_other
                
            # Move the pixel color to the destination row in the output grid
            output_grid[dest_r, c] = pixel_color
            
            # Set the original pixel location in the output grid to the background color
            output_grid[source_row, c] = background_color
            
    return output_grid