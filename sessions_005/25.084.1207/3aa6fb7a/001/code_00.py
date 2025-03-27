import numpy as np

"""
This program transforms an input grid based on specific neighborhood conditions.
It identifies white pixels (0) that are horizontally adjacent to exactly one azure pixel (8). 
If that adjacent azure pixel is part of a vertical segment (i.e., has another azure pixel directly above or below it), 
the white pixel is changed to blue (1) in the output grid. All other pixels retain their original color.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    A white pixel (0) becomes blue (1) if it's horizontally adjacent to exactly one 
    azure pixel (8), and that azure pixel has at least one vertical azure neighbor.
    
    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is white (0)
            if input_grid[r, c] == 0:
                
                azure_h_neighbors = [] # Store coordinates of azure horizontal neighbors
                
                # Check left neighbor
                if c > 0 and input_grid[r, c-1] == 8:
                    azure_h_neighbors.append((r, c-1))
                    
                # Check right neighbor
                if c < width - 1 and input_grid[r, c+1] == 8:
                    azure_h_neighbors.append((r, c+1))
                    
                # Check if there is exactly one horizontal azure neighbor
                if len(azure_h_neighbors) == 1:
                    # Get the coordinates of the single azure neighbor
                    nr, nc = azure_h_neighbors[0]
                    
                    has_vertical_azure_neighbor = False
                    
                    # Check neighbor above
                    if nr > 0 and input_grid[nr-1, nc] == 8:
                        has_vertical_azure_neighbor = True
                        
                    # Check neighbor below (only if above check failed)
                    if not has_vertical_azure_neighbor and nr < height - 1 and input_grid[nr+1, nc] == 8:
                        has_vertical_azure_neighbor = True
                        
                    # If the azure neighbor has a vertical azure neighbor, change the white cell to blue
                    if has_vertical_azure_neighbor:
                        output_grid[r, c] = 1

    # Return the modified grid
    return output_grid