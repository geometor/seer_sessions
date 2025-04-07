import numpy as np

"""
Transforms the input grid by projecting specific colors diagonally.

1. Initialize the output grid as a copy of the input grid.
2. Define background colors (0: white, 1: blue) and the static obstacle color (3: green).
3. Define projecting colors and their directions:
    - Red (2): Up-left (dr=-1, dc=-1)
    - Yellow (4) and Azure (8): Down-left (dr=+1, dc=-1)
4. Identify all non-background pixels in the input grid as potential sources.
5. Iterate through each source pixel:
    a. Skip green pixels (they are static obstacles only).
    b. Determine the projection direction (dr, dc) for red, yellow, or azure.
    c. Trace a path starting from the source pixel's location.
    d. In each step along the path:
        i. Calculate the next position (next_r, next_c).
        ii. Check for stop conditions:
            - If (next_r, next_c) is out of grid bounds, stop projecting for this source.
            - If the input grid color at (next_r, next_c) is green (3), stop projecting.
        iii. Check for coloring condition:
            - If the input grid color at (next_r, next_c) is a background color (0 or 1), set the output grid color at (next_r, next_c) to the source pixel's color.
        iv. Update the current position to (next_r, next_c) and continue tracing.
6. Return the final modified output grid.
"""

def transform(input_grid):
    """
    Applies the diagonal color projection transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define color sets and properties
    background_colors = {0, 1} # white, blue
    static_obstacle_color = 3 # green
    projecting_colors = {
        2: (-1, -1), # red: up-left
        4: (1, -1),  # yellow: down-left
        8: (1, -1)   # azure: down-left
    }

    # Find all non-background pixels (potential sources) in the input grid
    source_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color not in background_colors:
                source_pixels.append({'r': r, 'c': c, 'color': color})

    # Process each source pixel for projection
    for source in source_pixels:
        r_start, c_start, color = source['r'], source['c'], source['color']

        # Skip static green pixels (they don't project)
        if color == static_obstacle_color:
            continue

        # Get projection direction if the color is a projecting color
        if color in projecting_colors:
            dr, dc = projecting_colors[color]
        else:
            # Should not happen based on examples, but good to handle
            continue 

        # Initialize current position for projection ray tracing
        curr_r, curr_c = r_start, c_start

        # Start projection loop
        while True:
            # Calculate the next position in the projection path
            next_r, next_c = curr_r + dr, curr_c + dc

            # --- Check Stop Conditions ---
            # 1. Check boundaries
            if not (0 <= next_r < height and 0 <= next_c < width):
                break # Stop if outside grid

            # 2. Check for static obstacle (green) in the *input* grid
            obstacle_check_color = input_np[next_r, next_c]
            if obstacle_check_color == static_obstacle_color:
                break # Stop if the next cell is a green obstacle

            # --- Check Coloring Condition ---
            # Only color if the target cell in the *input* grid was a background color
            if obstacle_check_color in background_colors:
                output_np[next_r, next_c] = color

            # Move to the next position for the next iteration of tracing
            curr_r, curr_c = next_r, next_c

    # Convert back to list of lists before returning
    return output_np.tolist()