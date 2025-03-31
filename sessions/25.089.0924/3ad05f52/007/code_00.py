import numpy as np
from collections import deque

"""
Perform a constrained flood fill operation on the input grid.
1. Identify the unique 'fill color' which is not white (0) or azure (8).
2. Identify all pixels with this 'fill color' in the input grid; these are the 'seed points'.
3. Identify all white (0) pixels connected to the grid border without crossing any non-white pixels (including azure 8). Mark these as 'exterior white'.
4. Starting from the seed points, perform a 4-way flood fill on the grid.
5. The fill operation changes white (0) pixels to the 'fill color' *only if* the white pixel is *not* marked as 'exterior white'.
6. The fill stops at the grid boundaries, at pixels with the azure (8) color (or any other non-white pixel), and at 'exterior white' pixels.
7. The output grid is the input grid after the constrained flood fill operation.
"""

def transform(input_grid):
    """
    Applies a constrained flood fill transformation based on a unique seed color
    bounded by azure (8), ensuring the fill does not leak into exterior white areas.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # --- Find the unique fill color and seed points ---
    fill_color = -1
    unique_colors = np.unique(input_grid)

    # Iterate through unique colors to find the one that's not background (0) or boundary (8)
    for color in unique_colors:
        if color != 0 and color != 8:
            fill_color = color
            break # Assume only one such color based on problem description

    # If no specific fill color found (grid might be only 0s and 8s, or just 0s), return original
    if fill_color == -1:
        return output_grid

    # Find all initial locations of the fill color in the input grid
    seed_points_coords = np.where(input_grid == fill_color)
    seed_points = list(zip(seed_points_coords[0], seed_points_coords[1]))

    # If no seed points found for the determined fill_color, return original
    if not seed_points:
         return output_grid

    # --- Identify Exterior White Pixels ---
    is_exterior = np.zeros((height, width), dtype=bool)
    exterior_queue = deque()

    # Check border cells and add starting points for the exterior BFS
    for r in range(height):
        for c in [0, width - 1]:
            # If a border cell is white (0) and not already marked
            if input_grid[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                exterior_queue.append((r, c))
    for c in range(1, width - 1): # Avoid double-checking corners
        for r in [0, height - 1]:
            if input_grid[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                exterior_queue.append((r, c))

    # BFS to find all white pixels connected to the border
    while exterior_queue:
        r, c = exterior_queue.popleft()
        # Explore 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If neighbor is white in the *original input* and not yet marked as exterior
                if input_grid[nr, nc] == 0 and not is_exterior[nr, nc]:
                    is_exterior[nr, nc] = True
                    exterior_queue.append((nr, nc))

    # --- Perform Constrained Flood Fill (using BFS) ---
    fill_queue = deque(seed_points)
    # Initialize visited set. Crucially, include all seed points AND all exterior white points.
    # This prevents the fill from starting in or spreading into the exterior region.
    visited = set(seed_points)
    exterior_coords = np.where(is_exterior)
    visited.update(zip(exterior_coords[0], exterior_coords[1]))


    while fill_queue:
        r, c = fill_queue.popleft()

        # Explore 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor hasn't been visited yet (this implicitly handles boundaries like 8 and exterior white cells)
                if (nr, nc) not in visited:
                    # Check if the neighbor is a fillable area (white color 0 in the *output grid*)
                    # We only need to check if it's 0, because the 'visited' check already
                    # filters out boundaries(8), exterior white, and already filled cells.
                    if output_grid[nr, nc] == 0:
                         # Fill the pixel
                        output_grid[nr, nc] = fill_color
                        # Mark as visited
                        visited.add((nr, nc))
                        # Add to queue for further exploration
                        fill_queue.append((nr, nc))
                    else:
                        # If it's not white (0), it must be a boundary (8) or some other non-fillable color.
                        # Mark it as visited anyway to avoid checking it again from another path.
                         visited.add((nr, nc))


    # Return the modified grid
    return output_grid