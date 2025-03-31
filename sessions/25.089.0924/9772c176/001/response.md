```python
import numpy as np

"""
Transforms the input grid by adding yellow pixels (4) based on adjacency to azure pixels (8).
The rule is: A white pixel (0) becomes yellow (4) if it has exactly three azure neighbors
(including orthogonal and diagonal neighbors).
Azure pixels (8) remain unchanged. Other white pixels (0) remain unchanged. All other colors also remain unchanged.
"""

def find_neighbors(grid, r, c):
    """
    Finds orthogonal and diagonal neighbors for a cell (r, c) in the grid.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.

    Returns:
        list: A list of tuples, where each tuple contains the coordinates ((nr, nc))
              and the color (grid[nr, nc]) of a neighbor.
    """
    neighbors = []
    rows, cols = grid.shape
    # Iterate through the 3x3 neighborhood centered at (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(((nr, nc), grid[nr, nc]))
    return neighbors

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    A white pixel (0) becomes yellow (4) if it has exactly three azure (8) neighbors
    (including orthogonal and diagonal neighbors). Otherwise, pixels retain their
    original color.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to store the output
    output_grid_np = np.copy(input_grid_np)
    rows, cols = input_grid_np.shape
    
    # Define the relevant colors
    azure_color = 8
    white_color = 0
    yellow_color = 4

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is white
            if input_grid_np[r, c] == white_color:
                # Count the number of azure neighbors
                azure_neighbor_count = 0
                neighbors = find_neighbors(input_grid_np, r, c)
                for _, neighbor_color in neighbors:
                    if neighbor_color == azure_color:
                        azure_neighbor_count += 1
                
                # Apply the transformation rule: if exactly 3 azure neighbors, change to yellow
                if azure_neighbor_count == 3:
                    output_grid_np[r, c] = yellow_color
            # If the cell is not white, it remains unchanged in the output grid (already copied)

    # Convert the resulting numpy array back to a list of lists
    return output_grid_np.tolist()
```