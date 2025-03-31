import numpy as np

"""
Transformation Rule Natural Language Description:

1. Start with the input grid. The grid contains orange (7) background pixels, magenta (6) source pixels, and red (2) barrier pixels.
2. Initialize the output grid as a copy of the input grid.
3. Identify all pixels that are initially magenta (color 6). These are the starting points for propagation.
4. Repeatedly perform the following expansion step until no more orange pixels can be changed to magenta in a full iteration:
    a. Find all orange (7) pixels that are cardinally adjacent (up, down, left, or right) to any existing magenta (6) pixel (either initial or one filled in a previous step).
    b. Change all such identified orange pixels to magenta (6). Red (2) pixels act as barriers and are never changed, nor do they allow propagation through them. Grid boundaries also act as barriers.
5. The resulting grid, after the propagation process stabilizes (no more changes occur), is the final output grid.
"""

def transform(input_grid):
    """
    Applies a flood-fill transformation originating from magenta (6) pixels.
    The fill spreads cardinally into adjacent orange (7) pixels,
    stopping at red (2) pixels and grid boundaries.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid with magenta areas filled.
    """
    # Define color constants
    ORANGE = 7
    MAGENTA = 6
    RED = 2 # Although not explicitly used in the filling logic, it acts as an implicit barrier because we only fill ORANGE

    # Convert input list of lists to a NumPy array for easier manipulation
    output_grid = np.array(input_grid, dtype=int)
    height, width = output_grid.shape

    # Use a loop that continues as long as changes are being made
    while True:
        # List to store coordinates of orange pixels to be changed to magenta in this iteration
        pixels_to_fill = []

        # Iterate through each cell in the grid
        for r in range(height):
            for c in range(width):
                # We are looking for ORANGE cells that need to be filled
                if output_grid[r, c] == ORANGE:
                    # Check cardinal neighbors (up, down, left, right)
                    is_adjacent_to_magenta = False
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc

                        # Check if the neighbor is within grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor is magenta
                            if output_grid[nr, nc] == MAGENTA:
                                is_adjacent_to_magenta = True
                                break # Found a magenta neighbor, no need to check others for this cell

                    # If this orange cell is adjacent to a magenta cell, mark it for filling
                    if is_adjacent_to_magenta:
                        pixels_to_fill.append((r, c))

        # If no orange pixels were found adjacent to magenta in this pass, the fill is complete
        if not pixels_to_fill:
            break
        
        # Change the marked orange pixels to magenta
        # This is done after checking all cells to ensure propagation happens in waves
        for r, c in pixels_to_fill:
            output_grid[r, c] = MAGENTA

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_grid.tolist()