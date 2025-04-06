import copy

"""
Transforms a 2D grid based on the following rule: For each cell containing a 4 in the input grid, project outwards orthogonally (up, down, left, right). Change any 0 encountered along these projection paths to 2 in the output grid. The projection stops in a given direction if it hits the grid boundary or encounters a non-zero cell (e.g., another 4) in the input grid. Original 4s and 0s not reached by any projection remain unchanged.
"""

def is_within_bounds(r, c, height, width):
  """Checks if the given row and column are within the grid boundaries."""
  return 0 <= r < height and 0 <= c < width

def transform(input_grid):
    """
    Applies the projection transformation rule to the input grid.

    Args:
      input_grid: A list of lists representing the input 2D grid.

    Returns:
      A list of lists representing the transformed output 2D grid.
    """
    # Handle empty grid cases
    if not input_grid:
        return []
    height = len(input_grid)
    if height == 0 or not input_grid[0]:
         return [[] for _ in range(height)] # Return grid of empty rows if rows exist but are empty
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This preserves original 4s and 0s that won't be changed.
    # Importantly, projection checks are based on the *original* input_grid state.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid to find the '4's (sources)
    for r in range(height):
        for c in range(width):
            # If the current cell in the input grid is a source (value 4)
            if input_grid[r][c] == 4:

                # --- Project Upwards ---
                nr = r - 1 # Start one cell above
                nc = c
                # Continue as long as within bounds and hitting 0s in the *input* grid
                while is_within_bounds(nr, nc, height, width) and input_grid[nr][nc] == 0:
                    output_grid[nr][nc] = 2 # Change the cell in the *output* grid
                    nr -= 1 # Move to the next cell upwards

                # --- Project Downwards ---
                nr = r + 1 # Start one cell below
                nc = c
                # Continue as long as within bounds and hitting 0s in the *input* grid
                while is_within_bounds(nr, nc, height, width) and input_grid[nr][nc] == 0:
                    output_grid[nr][nc] = 2 # Change the cell in the *output* grid
                    nr += 1 # Move to the next cell downwards

                # --- Project Leftwards ---
                nr = r
                nc = c - 1 # Start one cell left
                # Continue as long as within bounds and hitting 0s in the *input* grid
                while is_within_bounds(nr, nc, height, width) and input_grid[nr][nc] == 0:
                    output_grid[nr][nc] = 2 # Change the cell in the *output* grid
                    nc -= 1 # Move to the next cell leftwards

                # --- Project Rightwards ---
                nr = r
                nc = c + 1 # Start one cell right
                # Continue as long as within bounds and hitting 0s in the *input* grid
                while is_within_bounds(nr, nc, height, width) and input_grid[nr][nc] == 0:
                    output_grid[nr][nc] = 2 # Change the cell in the *output* grid
                    nc += 1 # Move to the next cell rightwards

    # Return the modified output grid
    return output_grid