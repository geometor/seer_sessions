import numpy as np

"""
Performs a flood fill operation on a grid.

The transformation identifies specific colors (1: blue, 3: green, 4: yellow, 6: magenta, 7: orange, 8: azure) as "source" colors.
These source colors spread iteratively into adjacent white (0) cells, including diagonally adjacent cells (Moore neighborhood).
Gray (5) cells act as barriers and do not change color, nor does the color spread across them.
The process repeats until no more white cells are adjacent to any source-colored cells (either original sources or cells that became colored during the fill).
It assumes that a white cell will not be simultaneously adjacent to two different source colors in a way that creates ambiguity; the first source color found during neighbor checking is used.
"""

def transform(input_grid):
    """
    Applies an iterative flood fill based on source colors spreading into background.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed grid.
    """
    # Make a copy to modify
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Define the colors involved in the transformation
    source_colors = {1, 3, 4, 6, 7, 8}
    barrier_color = 5 # Gray acts as a barrier
    background_color = 0 # White is the fillable background

    # Loop until no changes are made in a full pass
    while True:
        # List to store changes for the current iteration: (row, col, new_color)
        changes_in_iteration = []

        # Iterate through each cell to check if it's a background cell needing filling
        for r in range(height):
            for c in range(width):
                # Only consider changing background (white) cells
                if output_grid[r, c] == background_color:
                    found_source_color = -1 # Sentinel value: no adjacent source found yet

                    # Check all 8 neighbors (Moore neighborhood)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            # Skip checking the cell itself
                            if dr == 0 and dc == 0:
                                continue

                            nr, nc = r + dr, c + dc

                            # Check if neighbor coordinates are within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = output_grid[nr, nc]

                                # Check if the neighbor has a source color
                                if neighbor_color in source_colors:
                                    # Found a source neighbor. Store its color.
                                    # Based on examples, we assume no conflict where a cell is
                                    # adjacent to two *different* source colors simultaneously.
                                    found_source_color = neighbor_color
                                    # Break neighbor loops once a source is found
                                    break
                        if found_source_color != -1:
                             # Break outer neighbor loop as well
                             break

                    # If a source neighbor was found for this background cell,
                    # record the change to be applied.
                    if found_source_color != -1:
                        changes_in_iteration.append((r, c, found_source_color))

        # If no cells were identified to be changed in this pass, the fill is complete.
        if not changes_in_iteration:
            break

        # Apply all the identified changes for this iteration.
        # This ensures that changes within one iteration are based on the grid state
        # *at the beginning* of the iteration.
        for r, c, new_color in changes_in_iteration:
            output_grid[r, c] = new_color

    # Return the fully transformed grid
    return output_grid