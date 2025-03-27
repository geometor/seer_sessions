"""
Recolors a main shape based on the color of the pixel at the bottom-left corner, 
then sets the bottom-left corner pixel to the background color (0).

1. Determine the height (H) of the input grid.
2. Get the color (SourceColor) of the pixel located at coordinates (H-1, 0) in the input grid.
3. Create a copy of the input grid to serve as the initial output grid.
4. Iterate through each cell (pixel) of the input grid at row R and column C.
5. If the input pixel at (R, C) is *not* the background color (0) AND the coordinates (R, C) are *not* (H-1, 0), then update the corresponding pixel at (R, C) in the output grid to SourceColor.
6. Set the pixel at (H-1, 0) in the output grid to the background color (0).
7. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the recoloring transformation based on the bottom-left pixel.

    Args:
        input_grid (list of lists): The input grid representing the task state.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier indexing
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the grid
    height, width = input_np.shape
    
    # Check if the grid has at least one row to access the bottom-left corner
    if height == 0 or width == 0:
        # Return an empty grid or handle as appropriate for edge cases
        return [[]] * height 
        
    # Get the SourceColor from the pixel at (H-1, 0) - bottom-left corner
    source_color_row = height - 1
    source_color_col = 0
    source_color = input_np[source_color_row, source_color_col]
    
    # Create the output grid, starting as a copy of the input
    output_np = np.copy(input_np)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is part of the main shape
            # i.e., it's not background (0) and not the source color pixel itself
            is_main_shape_pixel = (input_np[r, c] != 0) and not (r == source_color_row and c == source_color_col)
            
            if is_main_shape_pixel:
                # Recolor the corresponding pixel in the output grid with the SourceColor
                output_np[r, c] = source_color

    # Set the source color pixel location in the output grid to background color (0)
    output_np[source_color_row, source_color_col] = 0
            
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_np.tolist()
    
    return output_grid
