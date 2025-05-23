```python
import numpy as np

def get_neighbors(grid, r, c):
    """
    Gets the 8 Moore neighbors of a cell (r, c) in the grid.
    Handles boundary conditions by excluding neighbors outside the grid.
    """
    neighbors = []
    height, width = grid.shape
    for i in range(max(0, r - 1), min(height, r + 2)):
        for j in range(max(0, c - 1), min(width, c + 2)):
            if (i, j) != (r, c):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    A gray pixel (color 5) changes to azure (color 8) if and only if it has 
    at least one gray (5) neighbor AND at least one orange (7) neighbor 
    in its 8-cell Moore neighborhood. Otherwise, the pixel retains its original color.
    """
    # Convert input_grid to a numpy array for easier manipulation
    grid = np.array(input_grid)
    height, width = grid.shape
    # Create a copy of the input grid to modify
    output_grid = np.copy(grid)

    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is gray (5)
            if grid[r, c] == 5:
                # Get the values of the 8 neighbors
                neighbors = get_neighbors(grid, r, c)
                
                # Check if there is at least one gray neighbor (5)
                has_gray_neighbor = any(n == 5 for n in neighbors)
                
                # Check if there is at least one orange neighbor (7)
                has_orange_neighbor = any(n == 7 for n in neighbors)
                
                # If both conditions are met, change the pixel to azure (8)
                if has_gray_neighbor and has_orange_neighbor:
                    output_grid[r, c] = 8
                    
    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
```