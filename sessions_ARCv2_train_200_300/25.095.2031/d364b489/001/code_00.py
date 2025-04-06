import copy

"""
Transforms an input 10x10 grid containing 0s and 1s into an output 10x10 grid.
Each '1' in the input grid generates a cross-shaped pattern in the output grid centered at the '1's location.
The pattern consists of:
- '1' at the center (original '1' location).
- '2' in the cell directly above.
- '8' in the cell directly below.
- '7' in the cell directly to the left.
- '6' in the cell directly to the right.
The pattern elements are only placed if they fall within the grid boundaries.
If patterns overlap, the value from the last applied pattern overwrites previous values.
Cells not part of any pattern remain 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the cross-shaped pattern transformation to the input grid.

    Args:
        input_grid: A 10x10 list of lists containing 0s and 1s.

    Returns:
        A 10x10 list of lists representing the transformed grid.
    """
    # Ensure input is not empty and get dimensions
    if not input_grid or not input_grid[0]:
        return []
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid with zeros, ensuring it's a deep copy structure
    # or a completely new structure to avoid modifying the input unintentionally.
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is a '1' (pattern seed)
            if input_grid[r][c] == 1:
                # Apply the pattern centered at (r, c) to the output grid

                # Center: Place '1' at the seed location
                output_grid[r][c] = 1

                # Above: Place '2' if within bounds
                if r > 0:
                    output_grid[r - 1][c] = 2

                # Below: Place '8' if within bounds
                if r < rows - 1:
                    output_grid[r + 1][c] = 8

                # Left: Place '7' if within bounds
                if c > 0:
                    output_grid[r][c - 1] = 7

                # Right: Place '6' if within bounds
                if c < cols - 1:
                    output_grid[r][c + 1] = 6

    # Return the fully transformed grid
    return output_grid