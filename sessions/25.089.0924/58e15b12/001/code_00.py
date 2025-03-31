import numpy as np

"""
Transforms the input grid based on diagonal path tracing with wrap-around for azure (8) and green (3) pixels.

1. Identify all initial positions of azure (8) and green (3) pixels in the input grid.
2. For each initial azure pixel, trace a diagonal path (down-right) across the grid, wrapping around edges. Store all visited coordinates.
3. For each initial green pixel, trace a similar diagonal path, wrapping around edges. Store all visited coordinates separately.
4. Create an output grid initialized with white (0) pixels, matching the input grid dimensions.
5. Populate the output grid:
    - Mark all coordinates visited by azure paths with azure (8).
    - Mark all coordinates visited by green paths with green (3).
6. Identify coordinates visited by *both* azure and green paths (collisions).
7. Change the color of collision coordinates in the output grid to magenta (6).
8. Return the final output grid.
"""

def trace_diagonal_path(start_r, start_c, height, width):
    """
    Traces a diagonal path (down-right) with wrap-around.

    Args:
        start_r: Starting row index.
        start_c: Starting column index.
        height: Grid height.
        width: Grid width.

    Returns:
        A set of (row, col) tuples representing the path coordinates.
    """
    path_coords = set()
    curr_r, curr_c = start_r, start_c
    # Iterate enough times to cover all possible unique positions in the wrap-around path
    # The maximum length of such a cycle is related to lcm(height, width), 
    # but height * width is a safe upper bound to ensure all reachable cells are visited.
    for _ in range(height * width): 
        path_coords.add((curr_r, curr_c))
        # Move diagonally down-right
        next_r = curr_r + 1
        next_c = curr_c + 1
        # Apply wrap-around logic for row and column independently
        curr_r = next_r % height
        curr_c = next_c % width
        # Optimization: stop if we return to the start after the first step
        if (curr_r, curr_c) == (start_r, start_c) and len(path_coords) > 1:
             break # Cycle detected
            
    return path_coords

def transform(input_grid):
    """
    Applies the diagonal path tracing and collision transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize the output grid with background color (0)
    output_grid = np.zeros_like(input_np)
    
    # Sets to store coordinates visited by each color's path
    azure_path_coords = set()
    green_path_coords = set()

    # Find initial positions and trace paths
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            if pixel_color == 8:  # Azure
                path = trace_diagonal_path(r, c, height, width)
                azure_path_coords.update(path)
            elif pixel_color == 3:  # Green
                path = trace_diagonal_path(r, c, height, width)
                green_path_coords.update(path)

    # Populate the output grid with azure paths
    for r, c in azure_path_coords:
        output_grid[r, c] = 8

    # Populate the output grid with green paths (overwrites azure if only green)
    for r, c in green_path_coords:
        output_grid[r, c] = 3

    # Find and mark collisions with magenta
    collision_coords = azure_path_coords.intersection(green_path_coords)
    for r, c in collision_coords:
        output_grid[r, c] = 6
        
    # return output_grid # Return numpy array - standard practice in ARC
    # Or convert back to list of lists if required by a specific framework
    return output_grid.tolist() 
