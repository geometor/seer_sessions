import copy

"""
Transforms an input grid based on the neighborhood of cells with value 5.
A cell with value 5 changes to 2 if it has more than 5 non-zero neighbors (including diagonals).
Cells with value 0 remain 0.
"""

def _is_valid(r, c, num_rows, num_cols):
    """Check if coordinates are within grid boundaries."""
    return 0 <= r < num_rows and 0 <= c < num_cols

def _count_nonzero_neighbors(grid: list[list[int]], r: int, c: int) -> int:
    """Counts the non-zero neighbors (including diagonals) for a given cell."""
    num_rows = len(grid)
    num_cols = len(grid[0])
    count = 0
    # Define the 8 relative neighbor coordinates (dr, dc)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through all 8 neighbors
    for dr, dc in neighbor_offsets:
        nr, nc = r + dr, c + dc
        # Check if the neighbor is within grid bounds
        if _is_valid(nr, nc, num_rows, num_cols):
            # Check if the neighbor's value is non-zero
            if grid[nr][nc] != 0:
                count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: change 5 to 2 if it has > 5 non-zero neighbors.
    """
    # Get grid dimensions
    num_rows = len(input_grid)
    if num_rows == 0:
        return []
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)]

    # Initialize output_grid as a deep copy of the input to preserve original values
    # during neighbor counting and only modify the necessary cells.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Get the value of the current cell in the *original* input grid
            cell_value = input_grid[r][c]

            # Only process cells with value 5
            if cell_value == 5:
                # Count non-zero neighbors in the *original* input grid
                neighbor_count = _count_nonzero_neighbors(input_grid, r, c)

                # Apply the transformation rule
                if neighbor_count > 5:
                    # Update the corresponding cell in the output grid
                    output_grid[r][c] = 2
            # If cell_value is 0, it remains 0 (already handled by deepcopy)
            # If cell_value is 5 and neighbor_count <= 5, it remains 5 (already handled by deepcopy)

    # Return the modified grid
    return output_grid