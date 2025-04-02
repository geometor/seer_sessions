import numpy as np

"""
Identifies solid 3x3 squares of any non-white color within the input grid.
For each identified square, it transforms the square in the output grid by setting the four edge pixels (top-middle, bottom-middle, left-middle, right-middle) to white (0), while keeping the four corner pixels and the center pixel the original color. All other pixels in the grid remain unchanged.
"""

def transform(input_grid):
    """
    Transforms solid 3x3 non-white squares in the grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid_np)
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape
    
    # Iterate through each possible top-left corner (r, c) of a 3x3 square
    # We subtract 2 because a 3x3 square needs 3 rows and 3 columns
    for r in range(height - 2):
        for c in range(width - 2):
            # Extract the 3x3 subgrid from the input grid
            subgrid = input_grid_np[r:r+3, c:c+3]
            
            # Get the color of the top-left pixel of the subgrid
            color = subgrid[0, 0]
            
            # Check if the color is not white (0)
            if color != 0:
                # Check if all pixels in the 3x3 subgrid are the same color (i.e., it's a solid square)
                is_solid_square = np.all(subgrid == color)
                
                # If it is a solid square of a non-white color
                if is_solid_square:
                    # Apply the transformation to the corresponding area in the output grid
                    # Set edge pixels (not corners) to white (0)
                    output_grid[r, c+1] = 0     # Top-middle
                    output_grid[r+1, c] = 0     # Left-middle
                    output_grid[r+1, c+2] = 0   # Right-middle
                    output_grid[r+2, c+1] = 0   # Bottom-middle
                    
                    # Corner and center pixels implicitly retain their original color
                    # because output_grid started as a copy of input_grid.
                    # output_grid[r, c] = color     (Top-left corner)
                    # output_grid[r, c+2] = color   (Top-right corner)
                    # output_grid[r+1, c+1] = color (Center)
                    # output_grid[r+2, c] = color   (Bottom-left corner)
                    # output_grid[r+2, c+2] = color (Bottom-right corner)

    # Return the modified output grid (converting back to list of lists if necessary, though numpy array is often preferred)
    return output_grid.tolist()