import numpy as np

"""
The transformation rule takes an input grid and generates an output grid of the same dimensions.
The process involves identifying all non-white pixels in the input grid and using them to draw symmetrical patterns in the output grid.

1. Initialize an output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Iterate through each pixel (r, c) of the input grid.
3. If the pixel at (r, c) has a non-white color C:
    a. Calculate the coordinates of its reflections:
        - Vertical reflection row: r_v = height - 1 - r
        - Horizontal reflection column: c_h = width - 1 - c
    b. Draw four lines of color C onto the output grid:
        i.   A horizontal line at row `r` connecting columns `c` and `c_h`.
        ii.  A horizontal line at row `r_v` connecting columns `c` and `c_h`.
        iii. A vertical line at column `c` connecting rows `r` and `r_v`.
        iv.  A vertical line at column `c_h` connecting rows `r` and `r_v`.
4. The final output grid is the result of drawing all these lines. Subsequent drawing operations overwrite previous pixel values at the same location if colors differ, but in this specific task, lines of the same color originating from different input pixels might overlap.
"""

def transform(input_grid):
    """
    Transforms the input grid by drawing horizontal and vertical lines 
    connecting each non-white pixel with its reflections.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    height, width = input_np.shape
    
    # Initialize the output grid with white (0)
    output_np = np.zeros((height, width), dtype=int)
    
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            color = input_np[r, c]
            
            # Check if the current pixel is non-white
            if color != 0:
                # Calculate the coordinates for the reflections
                r_v = height - 1 - r  # Vertical reflection row
                c_h = width - 1 - c   # Horizontal reflection column
                
                # Determine start and end columns/rows for line drawing
                c_start = min(c, c_h)
                c_end = max(c, c_h)
                r_start = min(r, r_v)
                r_end = max(r, r_v)

                # Draw horizontal line at original row r
                output_np[r, c_start:c_end+1] = color
                
                # Draw horizontal line at vertically reflected row r_v
                output_np[r_v, c_start:c_end+1] = color
                
                # Draw vertical line at original column c
                output_np[r_start:r_end+1, c] = color
                
                # Draw vertical line at horizontally reflected column c_h
                output_np[r_start:r_end+1, c_h] = color
                
    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid