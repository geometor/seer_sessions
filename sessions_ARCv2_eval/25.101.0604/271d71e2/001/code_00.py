import copy

"""
Transforms an input grid based on a neighborhood rule:
1. Creates a copy of the input grid to serve as the output grid.
2. Iterates through each cell of the *input* grid.
3. If a cell in the input grid contains the value 5:
   a. Checks its 8 neighbors (orthogonal and diagonal) in the *input* grid.
   b. If any of these neighbors in the input grid contain the value 7:
      i. The corresponding cell in the *output* grid is updated to 7.
4. Returns the modified output grid.

Note: This implementation focuses on the primary observed rule (5 -> 7 based on 7-neighbors).
It does not account for potential secondary rules or anomalies observed in some examples
(e.g., shapes filled entirely with 5s changing to 7s, or other color changes involving 0, 6, 9).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the 5-to-7 transformation rule based on neighboring 7s.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This ensures we check neighbors based on the original input state
    output_grid = copy.deepcopy(input_grid)

    # Define the 8 neighbor offsets (dx, dy) including diagonals
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the *input* grid is 5
            if input_grid[r][c] == 5:
                # Check the neighbors of this cell in the *input* grid
                found_neighbor_7 = False
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within grid bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the *input* grid is 7
                        if input_grid[nr][nc] == 7:
                            found_neighbor_7 = True
                            break # Stop checking neighbors once a 7 is found

                # If a neighboring 7 was found in the input grid, update the output grid
                if found_neighbor_7:
                    output_grid[r][c] = 7

    # Return the modified grid
    return output_grid