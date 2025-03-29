import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies gray pixels (5) that are orthogonally adjacent to exactly two yellow 
    pixels (4) and changes their color to red (2). All other pixels remain 
    unchanged.
    """

    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is gray (5)
            if input_grid[r, c] == 5:
                # Count the number of yellow (4) orthogonal neighbors
                yellow_neighbor_count = 0
                
                # Define orthogonal neighbor coordinates (dr, dc)
                neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
                
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is yellow (4)
                        if input_grid[nr, nc] == 4:
                            yellow_neighbor_count += 1
                            
                # If the gray pixel has exactly two yellow neighbors, change it to red (2) in the output grid
                if yellow_neighbor_count == 2:
                    output_grid[r, c] = 2
            
            # If the pixel is not gray, or if it's gray but doesn't meet the condition,
            # its value in the output_grid remains unchanged (as it was copied initially).

    # Return the modified grid
    return output_grid