import numpy as np
import copy

"""
Identifies pairs of cardinally adjacent Green(3) and Red(2) pixels in the input grid. 
Cardinal adjacency means sharing an edge (up, down, left, or right), not just a corner (diagonal).
For each identified pair, the Green(3) pixel is changed to Azure(8) and the Red(2) pixel is changed to White(0) in the output grid. 
Pixels not involved in such a pair remain unchanged. 
Changes are determined based on the initial state of the grid and applied simultaneously.
"""

def get_cardinal_neighbors(r, c, height, width):
    """
    Generates coordinates for the 4 cardinal neighbors (up, down, left, right) of a cell.
    Yields only valid coordinates within the grid boundaries.
    """
    neighbors = []
    # Check Up
    if r > 0:
        neighbors.append((r - 1, c))
    # Check Down
    if r < height - 1:
        neighbors.append((r + 1, c))
    # Check Left
    if c > 0:
        neighbors.append((r, c - 1))
    # Check Right
    if c < width - 1:
        neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid based on cardinally adjacent Green(3) and Red(2) pixels.

    Args:
        input_grid (list of lists or np.array): The input grid representing colors.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert to numpy array for easier access and manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a deep copy of the input grid
    # Changes will be applied to this grid based on findings in the input_np
    output_np = np.copy(input_np)

    # Create sets to store the coordinates of pixels that need transformation
    # Using sets automatically handles duplicates if a pixel is involved in multiple pairs
    green_to_azure_coords = set()
    red_to_white_coords = set()

    # Iterate through each cell (r, c) of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is Green (3)
            if input_np[r, c] == 3:
                # Examine the 4 cardinal neighbors
                for nr, nc in get_cardinal_neighbors(r, c, height, width):
                    # Check if the neighbor's color is Red (2)
                    if input_np[nr, nc] == 2:
                        # Record the coordinates of the Green pixel (r, c) to change to Azure
                        green_to_azure_coords.add((r, c))
                        # Record the coordinates of the Red pixel (nr, nc) to change to White
                        red_to_white_coords.add((nr, nc))

    # Apply the recorded transformations to the output grid
    for r, c in green_to_azure_coords:
        output_np[r, c] = 8 # Change Green to Azure

    for r, c in red_to_white_coords:
        output_np[r, c] = 0 # Change Red to White

    # Convert back to list of lists format for consistency with ARC standard
    output_grid = output_np.tolist()
    
    # Return the final output grid
    return output_grid