import numpy as np

"""
Identify all white pixels (0) in the input grid. 
For each white pixel, check its eight neighbors (up, down, left, right, and the four diagonals). 
If any neighbor in the input grid is red (2), change the color of the corresponding pixel in the output grid to azure (8). 
All other pixels retain their original color.
"""

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels to azure if they are adjacent 
    (including diagonals) to any red pixel.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to a numpy array if it's not already
    input_grid_np = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid_np.copy()
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if input_grid_np[r, c] == 0:
                has_red_neighbor = False
                # Check all 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the pixel itself
                        if dr == 0 and dc == 0:
                            continue
                        
                        # Calculate neighbor coordinates
                        nr, nc = r + dr, c + dc
                        
                        # Check if neighbor coordinates are within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor is red (2) in the original input grid
                            if input_grid_np[nr, nc] == 2:
                                has_red_neighbor = True
                                break  # Found a red neighbor, no need to check others
                    if has_red_neighbor:
                        break # Exit the outer neighbor loop as well
                
                # If a red neighbor was found, change the pixel in the output grid to azure (8)
                if has_red_neighbor:
                    output_grid[r, c] = 8

    return output_grid.tolist() # Return as list of lists, matching ARC format