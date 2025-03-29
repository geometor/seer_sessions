import numpy as np

"""
1. Create a copy of the input grid to serve as the output grid.
2. Identify all columns that contain azure (8) pixels in the input grid.
3. For each identified column `c`:
    a. Find the row index `r_start` of the lowest azure (8) pixel in column `c` in the input grid.
    b. Iterate through the rows `r` starting from `r_start + 1` down to the last row of the grid.
    c. Examine the pixel at position `(r, c)` in the *input* grid.
    d. If the pixel at `(r, c)` in the input grid is red (2), stop the extension process for this column `c` (do not modify this row `r` or any subsequent rows in this column).
    e. If the pixel at `(r, c)` in the input grid is *not* red (2), change the pixel at position `(r, c)` in the *output* grid to azure (8).
4. Return the modified output grid.
"""

def transform(input_grid):
    """
    Extends vertical azure lines downwards until they hit a red pixel 
    in the same column or the bottom edge of the grid.
    """
    # Convert input_grid list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Define colors
    azure = 8
    red = 2
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Iterate through each column
    for c in range(width):
        # Find the row indices of azure pixels in the current column
        azure_indices = np.where(input_np[:, c] == azure)[0]
        
        # Check if there are any azure pixels in this column
        if azure_indices.size > 0:
            # Find the row index of the lowest azure pixel in this column
            r_start = np.max(azure_indices)
            
            # Iterate downwards from the row below the lowest azure pixel
            for r in range(r_start + 1, height):
                # Check the pixel in the original input grid at the current position
                if input_np[r, c] == red:
                    # If a red pixel is encountered, stop extending in this column
                    break
                else:
                    # Otherwise, change the corresponding pixel in the output grid to azure
                    output_grid[r, c] = azure
                    
    # Convert the result back to a list of lists
    return output_grid.tolist()
