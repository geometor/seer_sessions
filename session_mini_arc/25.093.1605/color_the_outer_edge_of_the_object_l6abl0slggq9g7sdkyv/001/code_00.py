import numpy as np

"""
Transforms an input grid by identifying background cells (value 0) that are adjacent 
(horizontally, vertically, or diagonally - Moore neighborhood) to object cells (value 4) 
and changing the value of these adjacent background cells to 6 in the output grid. 
Original object cells (4) and background cells (0) not adjacent to any object cell 
remain unchanged.
"""

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list or numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid)
    rows, cols = input_np.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Define the 8 directions for the Moore neighborhood (relative coordinates)
    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the input grid is a background cell (0)
            if input_np[r, c] == 0:
                # Assume initially that it's not adjacent to an object cell (4)
                is_adjacent_to_4 = False
                # Check all 8 neighbors
                for dr, dc in neighbor_deltas:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are valid (within grid bounds)
                    if _is_valid(nr, nc, rows, cols):
                        # Check if the neighbor in the input grid is an object cell (4)
                        if input_np[nr, nc] == 4:
                            is_adjacent_to_4 = True
                            break # Found a '4' neighbor, no need to check further

                # If any neighbor was a '4', change the corresponding cell in the output grid to 6
                if is_adjacent_to_4:
                    output_grid[r, c] = 6
            # If the cell was not 0 (i.e., it was 4), or if it was 0 but not adjacent to 4,
            # its value in output_grid remains the same as it was copied from input_np.

    return output_grid.tolist() # Return as a list of lists if required, or keep as numpy array