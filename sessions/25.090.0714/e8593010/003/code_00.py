import numpy as np

"""
Transforms white pixels in a grid based on the count of their white neighbors.
Gray pixels remain unchanged. The color assigned to a white pixel depends on
the specific counts of its cardinal (adjacent) and diagonal white neighbors.

Rule Set:
- If (Cardinal, Diagonal) white neighbors == (0, 0) -> Green (3)
- If (Cardinal, Diagonal) white neighbors == (0, 1) -> Green (3)
- If (Cardinal, Diagonal) white neighbors == (2, 0) -> Blue (1)
- If (Cardinal, Diagonal) white neighbors == (1, 2) -> Blue (1)
- If (Cardinal, Diagonal) white neighbors == (1, 3) -> Blue (1)
- If (Cardinal, Diagonal) white neighbors == (2, 1) -> Blue (1)
- For all other combinations (default, includes (1,0), (1,1)) -> Red (2)
"""

def count_neighbors_separated(grid, r, c):
    """Counts cardinal and diagonal neighbors of a specific color (0) for a given cell."""
    rows, cols = grid.shape
    cardinal_count = 0
    diagonal_count = 0
    target_color = 0 # We are only interested in white neighbors

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is the target color
                if grid[nr, nc] == target_color:
                    # Check if cardinal or diagonal
                    if abs(dr) + abs(dc) == 1: # Cardinal
                        cardinal_count += 1
                    else: # Diagonal
                        diagonal_count += 1
                        
    return cardinal_count, diagonal_count

def transform(input_grid):
    """
    Applies the transformation rule based on white neighbor counts to the input grid.
    """
    # Ensure input is a numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid_np)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is white (0)
            if input_grid_np[r, c] == 0:
                # Count cardinal (C) and diagonal (D) white neighbors
                cardinal_neighbors, diagonal_neighbors = count_neighbors_separated(input_grid_np, r, c)
                
                # Apply the transformation rules based on (C, D) counts
                if cardinal_neighbors == 0 and diagonal_neighbors == 0:
                    output_grid[r, c] = 3 # Green
                elif cardinal_neighbors == 0 and diagonal_neighbors == 1:
                    output_grid[r, c] = 3 # Green
                elif cardinal_neighbors == 2 and diagonal_neighbors == 0:
                    output_grid[r, c] = 1 # Blue
                elif cardinal_neighbors == 1 and diagonal_neighbors == 2:
                    output_grid[r, c] = 1 # Blue
                elif cardinal_neighbors == 1 and diagonal_neighbors == 3:
                    output_grid[r, c] = 1 # Blue
                elif cardinal_neighbors == 2 and diagonal_neighbors == 1:
                     output_grid[r, c] = 1 # Blue
                else:
                    # Default case for all other combinations (e.g., (1,0), (1,1))
                    output_grid[r, c] = 2 # Red
            
            # If the cell is not white (e.g., gray 5), it remains unchanged 
            # as the output grid was initialized as a copy.

    # Return the transformed grid as a list of lists, matching ARC format
    return output_grid.tolist()