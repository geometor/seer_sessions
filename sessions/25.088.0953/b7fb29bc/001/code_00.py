import numpy as np
from collections import deque

"""
Fill the area inside a green frame with alternating colors based on Manhattan distance to the nearest green pixel.
White pixels inside the frame are colored yellow (4) if their minimum Manhattan distance to any green pixel is odd,
and red (2) if the distance is even. Green pixels and pixels outside the frame remain unchanged.
"""

def _find_exterior_white(grid):
    """Finds all white pixels connected to the border using BFS."""
    rows, cols = grid.shape
    exterior_coords = set()
    q = deque()
    visited = np.zeros_like(grid, dtype=bool)

    # Add border white pixels to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
                exterior_coords.add((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
                exterior_coords.add((r, c))

    # BFS to find all connected white pixels
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))
                exterior_coords.add((nr, nc))

    return exterior_coords

def _calculate_distances_from_green(grid):
    """Calculates minimum Manhattan distance from each pixel to the nearest green pixel using BFS."""
    rows, cols = grid.shape
    distances = np.full_like(grid, -1, dtype=int) # Use -1 for unvisited/infinity
    q = deque()

    # Initialize queue with all green pixels
    green_pixels = np.argwhere(grid == 3)
    for r, c in green_pixels:
        distances[r, c] = 0
        q.append((r, c))

    # Perform BFS
    while q:
        r, c = q.popleft()
        current_dist = distances[r, c]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Manhattan distance neighbors
            nr, nc = r + dr, c + dc

            # Check bounds and if already visited with a shorter or equal path
            if 0 <= nr < rows and 0 <= nc < cols and distances[nr, nc] == -1:
                 distances[nr, nc] = current_dist + 1
                 q.append((nr, nc))
            # Optional: If allowing updates for potentially shorter paths (though not needed for standard BFS from all sources)
            # elif 0 <= nr < rows and 0 <= nc < cols and distances[nr, nc] > current_dist + 1:
            #     distances[nr, nc] = current_dist + 1
            #     q.append((nr, nc))


    return distances


def transform(input_grid):
    """
    Transforms the input grid based on the specified rules.

    Identifies white pixels inside the green frame, calculates their minimum
    Manhattan distance to the nearest green pixel, and colors them yellow (4)
    for odd distances and red (2) for even distances > 0.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    # Create a copy to modify
    output_grid = grid.copy()

    # 1. Identify all white pixels reachable from the border (exterior white)
    exterior_white_coords = _find_exterior_white(grid)

    # 2. Calculate minimum distances from all green pixels
    distances = _calculate_distances_from_green(grid)

    # 3. Iterate through the grid and color interior white pixels
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel was originally white
            if grid[r, c] == 0:
                # Check if it's an interior white pixel (not reachable from border)
                if (r, c) not in exterior_white_coords:
                    dist = distances[r, c]
                    # Check if it's reachable from a green pixel (dist != -1) and distance > 0
                    if dist > 0:
                        # Color based on odd/even distance
                        if dist % 2 == 1: # Odd distance
                            output_grid[r, c] = 4 # Yellow
                        else: # Even distance
                            output_grid[r, c] = 2 # Red

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()