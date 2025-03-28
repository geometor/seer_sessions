"""
Color adjacent white pixels based on proximity to azure pixels.

1. Initialize the output grid as an identical copy of the input grid.
2. Iterate through each pixel (cell) of the input grid, identifying its row and column index.
3. For the current pixel at (row, col):
    a. Check if the color of the pixel in the *input* grid is white (0).
    b. If it is white (0), then examine its orthogonal neighbors (up, down, left, right).
    c. Check if any of these orthogonal neighbors in the *input* grid are azure (8).
    d. If at least one orthogonal neighbor is azure (8), change the color of the pixel at (row, col) in the *output* grid to red (2).
    e. Otherwise, the pixel in the output grid keeps its original color.
4. Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by coloring white pixels red if they are
    orthogonally adjacent to an azure pixel.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Define orthogonal neighbor offsets
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
    
    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input is white (0)
            if input_np[r, c] == 0:
                # Check its orthogonal neighbors
                is_adjacent_to_azure = False
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the input grid is azure (8)
                        if input_np[nr, nc] == 8:
                            is_adjacent_to_azure = True
                            break # Found an azure neighbor, no need to check others
                            
                # If an orthogonal azure neighbor was found, change the pixel in the output grid to red (2)
                if is_adjacent_to_azure:
                    output_grid[r, c] = 2
                    
    return output_grid.tolist() # Return as list of lists if preferred, or keep as np.ndarray