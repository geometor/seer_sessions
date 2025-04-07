import numpy as np

"""
Apply a cellular automaton growth rule iteratively to an initial pattern.
The rule is B3/S_all (Birth=3 neighbors, Survival=always):
- A white (0) cell becomes azure (8) in the next step if it has exactly 3 azure neighbors (including diagonals) in the current step.
- An azure (8) cell remains azure (8) in the next step.
- All other white (0) cells remain white (0).
The rule is applied iteratively for k steps, where k = floor(max(grid_height, grid_width) / 2).
"""

def count_azure_neighbors(grid, r, c):
    """
    Counts the number of azure (8) neighbors for a cell at (r, c).
    Includes 8 neighbors (horizontal, vertical, and diagonal).
    Handles grid boundaries.
    """
    height, width = grid.shape
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            # Check boundaries
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr, nc] == 8:
                    count += 1
    return count

def transform(input_grid):
    """
    Applies the B3/S_all cellular automaton rule iteratively.

    Args:
        input_grid (list of lists): The initial grid state.

    Returns:
        list of lists: The grid state after applying the rule for k iterations.
    """
    # Convert input to numpy array for easier manipulation
    current_grid = np.array(input_grid, dtype=int)
    height, width = current_grid.shape

    # Calculate the number of iterations
    k = max(height, width) // 2

    # Apply the cellular automaton rule for k iterations
    for _ in range(k):
        # Create a copy to store the next state
        # Existing azure cells (S_all) are preserved by default
        next_grid = current_grid.copy()

        # Iterate through each cell to apply the birth rule (B3)
        for r in range(height):
            for c in range(width):
                # Only check white cells for potential birth
                if current_grid[r, c] == 0:
                    # Count azure neighbors
                    neighbor_count = count_azure_neighbors(current_grid, r, c)
                    # Apply the birth rule: become azure if exactly 3 neighbors
                    if neighbor_count == 3:
                        next_grid[r, c] = 8

        # Update the grid for the next iteration
        current_grid = next_grid

    # Convert the final numpy array back to a list of lists
    output_grid = current_grid.tolist()
    return output_grid
