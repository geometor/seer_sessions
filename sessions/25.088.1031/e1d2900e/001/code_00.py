import numpy as np

"""
Transform the input grid by changing the color of white pixels (0) to blue (1) 
if they are directly adjacent (horizontally or vertically) to any red pixel (2). 
All original red (2) and blue (1) pixels, as well as white pixels not adjacent 
to red pixels, remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define relative coordinates for adjacent neighbors (up, down, left, right)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the input grid is white (0)
            if input_grid[r, c] == 0:
                # Check its adjacent neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is red (2)
                        if input_grid[nr, nc] == 2:
                            # If a red neighbor is found, change the corresponding
                            # cell in the *output* grid to blue (1)
                            output_grid[r, c] = 1
                            # Once changed, no need to check other neighbors for this cell
                            break 
                            
    # Return the modified grid
    return output_grid
