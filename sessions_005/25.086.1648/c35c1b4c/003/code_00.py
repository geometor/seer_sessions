"""
Identify the most frequent color (dominant color) in the input grid.
Perform a reachability analysis (BFS) starting from all boundary pixels that are *not* the dominant color.
This search can traverse through any adjacent (8 directions: orthogonal and diagonal) pixel that is also *not* the dominant color.
Mark all pixels reachable from the boundary through non-dominant paths.
Create an output grid by copying the input grid.
Iterate through the grid; any pixel that is *not* the dominant color and was *not* marked as reachable is considered enclosed.
Change the color of these enclosed pixels in the output grid to the dominant color.
Return the modified output grid.
"""

import numpy as np
from collections import deque, Counter

def find_dominant_color(grid):
    """
    Finds the color with the highest frequency in the grid.
    Handles ties by returning the smallest color value among the most frequent ones.
    """
    # Ensure grid is a numpy array for efficient counting
    grid_np = np.array(grid)
    # Flatten the grid to count occurrences
    colors, counts = np.unique(grid_np, return_counts=True)
    
    # Find the maximum count
    max_count = np.max(counts)
    
    # Find all colors that have the maximum count
    most_frequent_colors = colors[counts == max_count]
    
    # If there's a tie, return the smallest color value (consistent tie-breaking)
    dominant_color = np.min(most_frequent_colors)
    
    return dominant_color

def transform(input_grid):
    """
    Fills enclosed regions (pixels not of the dominant color that cannot reach
    the grid boundary without crossing the dominant color) with the dominant color.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid)
    height, width = grid.shape

    # 1. Find the dominant color
    dominant_color = find_dominant_color(grid)

    # 2. Initialize output grid as a copy of the input
    output_grid = grid.copy()

    # 3. Initialize reachability tracking and BFS queue
    is_reachable = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # 4. Seed the BFS queue with non-dominant boundary pixels
    for r in range(height):
        for c in range(width):
            # Check if pixel is on the boundary
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                # Check if the boundary pixel is not the dominant color
                if grid[r, c] != dominant_color:
                    # If not already marked, mark as reachable and add to queue
                    if not is_reachable[r, c]:
                        is_reachable[r, c] = True
                        queue.append((r, c))

    # 5. Perform BFS to find all reachable non-dominant pixels
    # Define 8 directions (orthogonal and diagonal)
    dr = [-1, -1, -1, 0, 0, 1, 1, 1]
    dc = [-1, 0, 1, -1, 1, -1, 0, 1]

    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for i in range(8):
            nr, nc = r + dr[i], c + dc[i]

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is not the dominant color AND not yet visited/reachable
                if grid[nr, nc] != dominant_color and not is_reachable[nr, nc]:
                    is_reachable[nr, nc] = True
                    queue.append((nr, nc))

    # 6. Fill enclosed non-dominant pixels in the output grid
    for r in range(height):
        for c in range(width):
            # If pixel is not dominant AND was not reached from the boundary
            if grid[r, c] != dominant_color and not is_reachable[r, c]:
                output_grid[r, c] = dominant_color

    # Convert back to list of lists for the expected ARC format
    return output_grid.tolist()