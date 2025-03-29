import numpy as np
from collections import Counter

"""
Identify the background color (most frequent color). 
Iteratively expand non-background colored areas into adjacent background areas.
In each iteration, scan the grid. If a background pixel is adjacent (up, down, left, or right) 
to a non-background pixel, change the background pixel's color to that of the non-background neighbor.
Repeat this process until no background pixels change color in a full iteration.
Assumes a background pixel will not be adjacent to multiple *different* non-background colors simultaneously;
if any non-background neighbor exists, the background pixel adopts that neighbor's color.
"""

def transform(input_grid):
    """
    Transforms the input grid by iteratively expanding non-background colors
    into adjacent background-colored cells until no further changes occur.
    """
    # Convert input list of lists to numpy array for easier handling and copying
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Handle edge case: if grid contains only one color, no transformation needed.
    unique_colors = np.unique(grid)
    if len(unique_colors) == 1:
        return input_grid # Return original list of lists format

    # Determine background color (assumed to be the most frequent color)
    counts = Counter(grid.flatten())
    # Ensure there are counts before accessing most_common
    if not counts:
        return input_grid # Should not happen with ARC constraints, but safe check
    background_color = counts.most_common(1)[0][0]

    # Initialize the grid state for iteration
    current_grid = grid.copy()

    # Iteratively expand non-background colors
    while True:
        changed_in_iteration = False
        # Create a copy to store the results of the current iteration's changes
        # We read from current_grid and write changes to next_grid to simulate simultaneous updates
        next_grid = current_grid.copy()
        
        # Iterate through each cell of the grid
        for r in range(height):
            for c in range(width):
                # Check if the cell in the current state is background color
                if current_grid[r, c] == background_color:
                    neighbor_color_to_assign = -1 # Use -1 as a sentinel for 'no non-background neighbor found'

                    # Check orthogonal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        
                        # Check if the neighbor coordinates are within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Get the color of the neighbor from the current grid state
                            neighbor_color = current_grid[nr, nc]
                            # Check if the neighbor has a non-background color
                            if neighbor_color != background_color:
                                # Found a non-background neighbor. Record its color.
                                # Assumption: The first one found is sufficient, or all relevant neighbors have the same color.
                                neighbor_color_to_assign = neighbor_color
                                break # Stop checking neighbors for this cell

                    # If a non-background neighbor was found (neighbor_color_to_assign is not -1)
                    if neighbor_color_to_assign != -1:
                         # Check if the cell's color in the next_grid is different from the neighbor's color
                         # If it is, update the cell in next_grid and mark that a change occurred
                         if next_grid[r, c] != neighbor_color_to_assign:
                            next_grid[r, c] = neighbor_color_to_assign
                            changed_in_iteration = True # A change was made in this iteration

        # After checking all cells, update the current grid state for the next iteration
        current_grid = next_grid

        # If no changes were made across the entire grid in this iteration, the expansion is complete
        if not changed_in_iteration:
            break

    # Convert the final numpy array back to a list of lists for the required output format
    return current_grid.tolist()