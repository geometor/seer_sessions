import numpy as np

def count_azure_neighbors(grid, r, c):
    """Counts the number of azure (8) neighbors for a given cell."""
    rows, cols = grid.shape
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check boundary conditions
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is azure
                if grid[nr, nc] == 8:
                    count += 1
    return count

def transform(input_grid):
    """
    Transforms an input grid based on the parity of azure neighbors.
    
    Rule:
    - White (0) pixels remain white (0).
    - Azure (8) pixels are transformed based on their Moore neighborhood (8 neighbors).
    - If an azure pixel has an EVEN number of azure neighbors, it becomes red (2).
    - If an azure pixel has an ODD number of azure neighbors, it becomes gray (5).
    """
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape
    
    # Initialize the output grid as a copy of the input grid
    # We will modify this grid based on the rules
    output_grid = np.copy(input_grid)
    
    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is azure (8)
            if input_grid[r, c] == 8:
                # Count the number of azure neighbors for this cell
                num_neighbors = count_azure_neighbors(input_grid, r, c)
                
                # Apply the transformation rule based on parity
                if num_neighbors % 2 == 0:  # Even number of neighbors
                    output_grid[r, c] = 2  # Change to red
                else:  # Odd number of neighbors
                    output_grid[r, c] = 5  # Change to gray
            # If the cell is white (0), it remains white (0) - no action needed
            
    return output_grid