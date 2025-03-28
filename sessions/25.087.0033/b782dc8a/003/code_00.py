"""
Transforms the input grid by identifying a specific region of white pixels connected to initial 'seed' colors and filling that region with a checkerboard pattern using those seed colors. Azure (8) pixels act as static barriers, confining the fill.

1.  **Identify Colors:** Find the two 'fill colors' (distinct from white 0 and azure 8). Sort them into `color_low` and `color_high`.
2.  **Locate Seeds:** Find all pixels initially containing `color_low` or `color_high`.
3.  **Determine Fillable Region:** Perform a Breadth-First Search (BFS) starting from the seed pixels. The search expands only into orthogonally adjacent white (0) pixels and is blocked by azure (8) pixels. Collect all reachable white pixel coordinates.
4.  **Apply Checkerboard:** Create a copy of the input grid. For each white pixel coordinate found in the fillable region, replace its color: use `color_low` if (row + col) is even, and `color_high` if (row + col) is odd.
5.  **Output:** Return the modified grid. Original azure, seed, and unconnected white pixels remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a bounded checkerboard fill pattern to white pixels connected to seed colors.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- 1. Identify Colors ---
    unique_colors = np.unique(grid)
    fill_colors = sorted([color for color in unique_colors if color not in [0, 8]])

    # Ensure exactly two fill colors were found
    if len(fill_colors) != 2:
        # Handle error case or assumption violation - return input unchanged
        # print(f"Warning: Expected 2 fill colors, found {len(fill_colors)}. Returning input.")
        return input_grid # Or raise an error

    color_low = fill_colors[0]
    color_high = fill_colors[1]

    # --- 2. Locate Seeds ---
    seed_pixels = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] in fill_colors:
                seed_pixels.append((r, c))

    # If no seeds are found, no region can be filled, return input
    if not seed_pixels:
        return input_grid

    # --- 3. Determine Fillable Region (BFS) ---
    fillable_region = set() # Stores coordinates of white pixels to be filled
    visited = set()        # Stores coordinates visited during BFS
    queue = deque()        # Queue for BFS

    # Initialize queue and visited set with seed locations
    for seed in seed_pixels:
        if seed not in visited:
            visited.add(seed)
            queue.append(seed)
            # Note: Seed pixels themselves are *not* added to fillable_region,
            # as their original color should be preserved.

    # Perform BFS
    while queue:
        r, c = queue.popleft()

        # Explore orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_coord = (nr, nc)
                # Check if already visited
                if neighbor_coord not in visited:
                    neighbor_color = grid[nr, nc]

                    # Check if it's a barrier
                    if neighbor_color != 8:
                        # Mark as visited regardless of color (unless barrier)
                        visited.add(neighbor_coord)
                        # If it's a white pixel, add to fillable region and queue
                        if neighbor_color == 0:
                            fillable_region.add(neighbor_coord)
                            queue.append(neighbor_coord)
                        # If it's another seed pixel, add to queue to continue search
                        # but do not add to fillable_region
                        elif neighbor_color in fill_colors:
                             queue.append(neighbor_coord)


    # --- 4. Apply Checkerboard ---
    # Create a copy of the input grid to modify
    output_grid = grid.copy()

    # Iterate through the identified fillable white pixels
    for r, c in fillable_region:
        # Calculate the parity based on row and column indices
        parity = (r + c) % 2

        # Assign the appropriate fill color based on parity
        if parity == 0:
            output_grid[r, c] = color_low
        else:
            output_grid[r, c] = color_high

    # --- 5. Output ---
    # Convert the result back to a list of lists before returning
    return output_grid.tolist()