"""
1.  **Identify Red Objects:** Find all distinct, contiguous regions of red (color 2) pixels. Each region is a separate object.
2.  **Identify Gray Pixels:** Find all individual gray (color 5) pixels.
3.  **Process Each Red Object:** For *each* red object:
    *   **Calculate Outline:** Determine the outline of the red object. The outline consists of all empty (color 0) pixels directly adjacent (up, down, left, or right) to the red object's pixels.
    * **Prioritized Outline Filling**: Find the Manhattan distance for each gray pixel and outline position, and, for each red object, sort by the minimal distances.
    *   **Place Gray Pixels:** For each gray pixel, try to find the closest point from the sorted outlines, attempt to place each grey pixel on the outline of a red object. If an outline position is occupied by a gray pixel, the next closest free outline position should be selected.
4. **Output Grid:** Create a new grid with the original red objects and the gray pixels moved to their new positions on the outlines.
"""

import numpy as np
from collections import defaultdict

def find_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_outline(grid, red_object):
    """Calculates the outline positions around a single red object."""
    outline = set()
    for r_red, c_red in red_object:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r_outline, c_outline = r_red + dr, c_red + dc
            if 0 <= r_outline < grid.shape[0] and 0 <= c_outline < grid.shape[1] and grid[r_outline, c_outline] == 0:
                outline.add((r_outline, c_outline))
    return list(outline)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find red objects and gray pixels
    red_objects = find_objects(input_grid, 2)
    gray_pixels = find_objects(input_grid, 5)
    gray_pixels_flat = [pixel for sublist in gray_pixels for pixel in sublist]

    # Clear original gray pixel positions
    for r, c in gray_pixels_flat:
        output_grid[r, c] = 0

    # Create a dictionary to store distances between gray pixels and outline positions for each red object
    distances = defaultdict(list)

    # Process each red object separately
    for red_object in red_objects:
        outline = get_outline(input_grid, red_object)

        # Calculate distances and populate the distances dictionary
        for r_gray, c_gray in gray_pixels_flat:
            for r_out, c_out in outline:
                dist = abs(r_out - r_gray) + abs(c_out - c_gray)
                distances[(r_gray, c_gray)].append(((r_out, c_out), dist))

    # Sort distances for each gray pixel
    for gray_pixel in distances:
        distances[gray_pixel].sort(key=lambda x: x[1])

    # Keep track of occupied outline positions
    occupied = set()

   # Place Gray Pixels based on sorted distances
    for (r_gray, c_gray), dist_list in distances.items():  # Iterate over all gray pixels
        for (r_out, c_out), dist in dist_list:           # Iterate over sorted distances
            if (r_out, c_out) not in occupied:        # Check if position not taken
                output_grid[r_out, c_out] = 5            # put grey pixel
                occupied.add((r_out, c_out))             # Mark as occupied
                break                                    # Move to the next gray pixel
            
    return output_grid