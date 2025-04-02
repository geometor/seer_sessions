import numpy as np
from collections import deque, Counter

"""
Identify the background color (assumed to be 0), the container color (the most frequent non-background color forming enclosing structures), and the target color (the other non-background color). 
Perform a flood fill (or Breadth-First Search - BFS) starting from the grid boundaries, avoiding cells with the container color. 
Mark all reachable cells ('outside' region). 
Create an output grid initialized with the background color. 
Copy the target color to the output grid only for cells that originally contained the target color and were marked as reachable ('outside') during the flood fill.
"""

def _identify_colors(grid):
    """Identifies background, container, and target colors."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Assume background is 0
    background_color = 0
    if background_color in color_counts:
        del color_counts[background_color]

    if not color_counts: # Only background color present
        return background_color, None, None

    # Find the most frequent non-background color as the potential container
    # Sort by count descending, then by color value ascending as tie-breaker
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
    
    container_color = sorted_colors[0][0]
    target_color = None
    
    if len(sorted_colors) > 1:
        # Find the first color that isn't the container
        for color, _ in sorted_colors[1:]:
            target_color = color
            break
    elif len(sorted_colors) == 1:
         # If only one non-background color, it acts as the target, no container blocking
         target_color = container_color
         container_color = -1 # Indicate no container effectively blocks flood fill


    # A better heuristic might be needed if frequency isn't always the best indicator
    # of the container, but it works for the provided examples.

    return background_color, container_color, target_color

def transform(input_grid):
    """
    Filters the input grid to keep only target color pixels located outside
    of regions enclosed by the container color.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Identify the key colors
    background_color, container_color, target_color = _identify_colors(input_np)

    # Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # If there's no target color, return the background grid
    if target_color is None:
        return output_grid.tolist()
        
    # If there's effectively no container (either only background and target,
    # or identified container color is -1), all target pixels are kept.
    if container_color is None or container_color == -1:
         for r in range(rows):
            for c in range(cols):
                 if input_np[r, c] == target_color:
                     output_grid[r, c] = target_color
         return output_grid.tolist()


    # Perform flood fill (BFS) from boundaries to find 'outside' cells
    q = deque()
    visited = np.zeros_like(input_np, dtype=bool)

    # Add boundary cells to queue if they are not the container color
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_np[r, c] != container_color and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
    for c in range(cols): # Use range(cols) instead of range(1, cols - 1) to include corners twice, which is fine
        for r in [0, rows - 1]:
             if input_np[r, c] != container_color and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
                
    # Define 8 directions for neighbors (including diagonals)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Start BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited and not the container color
                if not visited[nr, nc] and input_np[nr, nc] != container_color:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Populate the output grid
    for r in range(rows):
        for c in range(cols):
            # If the cell in the input grid has the target color AND was visited (is outside)
            if input_np[r, c] == target_color and visited[r, c]:
                # Set the corresponding cell in the output grid to the target color
                output_grid[r, c] = target_color

    return output_grid.tolist()