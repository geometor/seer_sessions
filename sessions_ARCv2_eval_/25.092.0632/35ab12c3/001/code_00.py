import numpy as np

"""
Identifies non-white pixels (seeds) in the input grid.
Determines a "fill color" for each seed: magenta (6) seeds use orange (7), others use their own color.
Simultaneously expands each seed's fill color into adjacent white (0) pixels iteratively.
Expansion stops at grid boundaries, existing non-white pixels, or where expansions from different fill colors would meet.
The process continues until no more white pixels can be filled.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by expanding seed pixels into adjacent white space.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 1. Identify seeds and determine their fill colors
    # We also need a way to track the fill color associated with *any* filled cell,
    # not just the original seeds, to correctly propagate colors.
    # fill_color_grid stores the 'effective' color (magenta->orange) for propagation.
    fill_color_grid = np.zeros_like(input_grid, dtype=int)
    initial_seeds = []
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            if color != 0:
                fill_color = 7 if color == 6 else color
                initial_seeds.append((r, c))
                fill_color_grid[r, c] = fill_color # Store the fill color

    # 2. Initialize the set of active coordinates (pixels filled in the previous step)
    active_coords = set(initial_seeds)

    # 3. Iterative expansion process
    while active_coords:
        # Dictionary to store potential fills for white cells in the next step.
        # Key: (r, c) of a white cell
        # Value: set of fill colors proposed by neighbors
        potential_fills = {}
        
        # Set to store coordinates that get filled in *this* iteration
        next_active_coords = set()

        # a. Check neighbors of currently active pixels
        for r, c in active_coords:
            # Get the fill color associated with the *current* active pixel
            # This ensures correct propagation from newly filled areas
            current_fill_color = fill_color_grid[r, c]
            if current_fill_color == 0: # Should not happen if logic is correct, but safety check
                continue

            # Check cardinal neighbors (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # Check if neighbor is within bounds and is white
                if 0 <= nr < height and 0 <= nc < width and output_grid[nr, nc] == 0:
                    # Add the current fill color to the set of potential fills for this neighbor
                    potential_fills.setdefault((nr, nc), set()).add(current_fill_color)

        # b. Process potential fills
        made_change_this_iteration = False
        for (r, c), colors_set in potential_fills.items():
            # If exactly one fill color is proposed for this white cell
            if len(colors_set) == 1:
                fill_c = list(colors_set)[0]
                # Check if the cell is still white (it should be based on the logic above)
                if output_grid[r, c] == 0:
                    output_grid[r, c] = fill_c
                    fill_color_grid[r, c] = fill_c # Update the fill color grid too
                    next_active_coords.add((r, c))
                    made_change_this_iteration = True # Mark that a change occurred

        # c. Prepare for next iteration or break
        if not made_change_this_iteration:
            break # No changes means expansion is complete

        active_coords = next_active_coords # Update active set for the next round

    # 4. Return the final grid
    return output_grid