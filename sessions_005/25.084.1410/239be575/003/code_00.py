import numpy as np

"""
This program determines the output based on the orthogonal (edge) adjacency of red (2) and azure (8) pixels in the input grid.
If any red pixel shares an edge with any azure pixel, the output is 0.
Otherwise (if adjacency exists only diagonally, or not at all), the output is 8.
"""

def transform(input_grid):
    """
    Checks for orthogonal (edge) adjacency between red (2) and azure (8) pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        int: 0 if any red pixel is orthogonally adjacent to an azure pixel, 
             8 otherwise.
    """
    
    grid = np.array(input_grid)
    height, width = grid.shape

    # Define the 4 relative orthogonal neighbor coordinates
    neighbors = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is red (value 2)
            if grid[r, c] == 2:
                # Check the 4 orthogonal neighbors of the red cell
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor cell is azure (value 8)
                        if grid[nr, nc] == 8:
                            # Found an orthogonally adjacent red and azure pixel, return 0
                            return 0

    # If the loops complete without finding any orthogonally adjacent red and azure pixels, return 8
    return 8