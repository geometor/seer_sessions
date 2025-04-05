```python
import numpy as np
import copy

"""
Transforms an input grid based on the following rule:
1. Cells with value 9 remain unchanged.
2. Cells with value 0 are transformed to 3 if they are adjacent (horizontally, vertically, or diagonally) to a cell with value 9 in the input grid.
3. Cells with value 0 that are not adjacent to any 9 remain 0.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Get grid dimensions
    height, width = input_np.shape
    # Initialize the output grid as a deep copy of the input grid
    # This handles preserving the 9s and the initial state of 0s
    output_np = input_np.copy()

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the *input* grid is 0
            if input_np[r, c] == 0:
                # Assume initially that no neighbor is 9
                is_neighbor_9 = False
                # Check all 8 neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is 9
                        if input_np[nr, nc] == 9:
                            is_neighbor_9 = True
                            # Found a 9 neighbor, no need to check others for this cell
                            break
                
                # If a neighbor was 9, change the corresponding cell in the *output* grid to 3
                if is_neighbor_9:
                    output_np[r, c] = 3
            # If the input cell was 9, it's already copied to output_np
            # If the input cell was 0 and had no 9 neighbors, it remains 0 in output_np

    # Convert the NumPy array back to a list of lists for the return value
    output_grid = output_np.tolist()
    return output_grid
```