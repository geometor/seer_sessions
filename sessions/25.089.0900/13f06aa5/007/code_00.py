import numpy as np
from collections import Counter

"""
Identify unique non-background pixels (triggers) in the input grid. A trigger pixel 
is one whose color is not the background color and appears exactly once in the grid. 
For each trigger:
1. Replace the trigger pixel with the background color in the output grid.
2. Perform an action based on the trigger's color (C1) and position (r, c):
    - Blue(1) or Green(3): Place C1 at (0, c) (Top edge, same column). Mark Top edge affected.
    - Red(2): Place C1 at (r, 0) (Left edge, same row). Mark Left edge affected.
    - Azure(8): Place C1 at (r, width-1) (Right edge, same row). Mark Right edge affected.
    - Magenta(6): Fill the entire bottom row (height-1) with Magenta(6). Also, place 
      Magenta(6) pixels in column 'c' at rows r+2, r+4, ... stopping before the last row. 
      Magenta does not mark edges as affected for corner checks.
3. After processing all triggers, handle corner intersections:
    - If Top and Left edges were affected, set pixel (0, 0) to White(0).
    - If Top and Right edges were affected, set pixel (0, width-1) to White(0).
Pixels not otherwise modified remain unchanged from the input.
"""

def find_background_color(grid_np):
    """Finds the most frequent color in the grid."""
    if grid_np.size == 0:
        return 0 # Default for empty grid
    counts = Counter(grid_np.flatten())
    # If multiple colors have the same max frequency, Counter returns one arbitrarily.
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_triggers(grid_np, background_color):
    """Finds unique non-background pixels."""
    height, width = grid_np.shape
    color_counts = Counter(grid_np.flatten())
    triggers = []
    for r in range(height):
        for c in range(width):
            color_C1 = grid_np[r, c]
            # Check if the color is not background and its count is exactly 1
            if color_C1 != background_color and color_counts[color_C1] == 1:
                triggers.append({'C1': color_C1, 'r': r, 'c': c})
    return triggers

def transform(input_grid):
    """
    Applies the transformation rule based on unique trigger pixels and edge/column modifications.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    if height == 0 or width == 0:
        return [] # Handle empty grid case

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Determine the background color
    background_color = find_background_color(input_grid_np)

    # Find all trigger pixels
    triggers = find_triggers(input_grid_np, background_color)

    # Keep track of which edges have been affected by non-Magenta triggers
    top_edge_affected = False
    left_edge_affected = False
    right_edge_affected = False

    # Process each trigger pixel
    for trigger in triggers:
        C1, r, c = trigger['C1'], trigger['r'], trigger['c']

        # Step 1: Replace the trigger pixel with the background color
        # Ensure coordinates are valid before writing
        if 0 <= r < height and 0 <= c < width:
             output_grid[r, c] = background_color

        # Step 2: Apply action based on C1
        if C1 == 1 or C1 == 3: # Blue (1) or Green (3) -> Top edge
            if height > 0 and 0 <= c < width: # Check target bounds
                output_grid[0, c] = C1
                top_edge_affected = True
        elif C1 == 2: # Red (2) -> Left edge
            if width > 0 and 0 <= r < height: # Check target bounds
                output_grid[r, 0] = C1
                left_edge_affected = True
        elif C1 == 8: # Azure (8) -> Right edge
            if width > 0 and 0 <= r < height: # Check target bounds
                output_grid[r, width - 1] = C1
                right_edge_affected = True
        elif C1 == 6: # Magenta (6) -> Special rules
            # Fill bottom edge
            if height > 0: # Ensure there is a bottom row
                output_grid[height - 1, :] = 6

            # Special column fill below the trigger
            # Start at r+2, step by 2, stop *before* the last row (height-1)
            for row_idx in range(r + 2, height - 1, 2):
                 # Check bounds before writing
                 if 0 <= row_idx < height and 0 <= c < width:
                    output_grid[row_idx, c] = 6
            # Note: Magenta actions do not set the edge_affected flags

    # Step 3: Handle corner intersections after processing all triggers
    # Check Top-Left corner (White = 0)
    if top_edge_affected and left_edge_affected:
        if height > 0 and width > 0: # Ensure corner exists
             output_grid[0, 0] = 0

    # Check Top-Right corner (White = 0)
    if top_edge_affected and right_edge_affected:
        if height > 0 and width > 0: # Ensure corner exists
            output_grid[0, width - 1] = 0

    # Return the modified grid as a list of lists
    return output_grid.tolist()