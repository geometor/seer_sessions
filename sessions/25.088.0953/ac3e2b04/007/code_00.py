import numpy as np
from collections import deque

"""
Transforms the input grid based on the following rules:

1.  **Identify Enclosed White Pixels:** Find all white (0) pixels that cannot reach the grid border by moving only through other 4-directionally adjacent white pixels. These are considered "enclosed".
2.  **Identify Adjacent Red Pixels:** Find all red (2) pixels in the original input grid that are 4-directionally adjacent (up, down, left, right) to at least one of the "enclosed white pixels" identified in step 1.
3.  **Apply Changes:** Create an output grid by copying the input. Then, change all "enclosed white pixels" to blue (1) in the output grid. Also, change all identified "adjacent red pixels" to blue (1) in the output grid. All other pixels retain their original color.
"""

def find_enclosed_white_pixels(grid):
    """
    Identifies white pixels enclosed by non-white pixels using BFS.

    Args:
        grid (np.array): The input grid.

    Returns:
        set: A set of tuples, where each tuple is the (row, col) coordinate
             of an enclosed white pixel.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    queue = deque()

    # Initialize queue with all border white pixels
    for r in range(height):
        for c in range(width):
            is_border = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            if is_border and grid[r, c] == 0:
                if not visited[r, c]: # Check if already added (e.g., corners)
                    visited[r, c] = True
                    queue.append((r, c))

    # Perform BFS starting from border white pixels (4-directional)
    while queue:
        r, c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, color (must be white), and visited status
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                queue.append((nr, nc))

    # Identify enclosed white pixels (white pixels not visited by the BFS)
    enclosed_coords = set()
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited[r, c]:
                enclosed_coords.add((r, c))

    return enclosed_coords

def find_adjacent_red_pixels(grid, enclosed_white_coords):
    """
    Identifies red pixels adjacent (4-directionally) to enclosed white pixels.

    Args:
        grid (np.array): The input grid.
        enclosed_white_coords (set): Set of coordinates of enclosed white pixels.

    Returns:
        set: A set of tuples, where each tuple is the (row, col) coordinate
             of a red pixel adjacent to an enclosed white pixel.
    """
    height, width = grid.shape
    red_to_change_coords = set()
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)] # 4-directional neighbors

    for r in range(height):
        for c in range(width):
            # Check if the pixel is red in the original grid
            if grid[r, c] == 2:
                # Check its 4 neighbors
                for dr, dc in deltas:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if the neighbor is an enclosed white pixel
                    if 0 <= nr < height and 0 <= nc < width and \
                       (nr, nc) in enclosed_white_coords:
                        red_to_change_coords.add((r, c))
                        break # Found one adjacent enclosed white, no need to check others

    return red_to_change_coords

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 2. Identify enclosed white pixels
    enclosed_white_coords = find_enclosed_white_pixels(input_grid)

    # 3. Identify red pixels adjacent to the enclosed white pixels
    red_coords_to_change = find_adjacent_red_pixels(input_grid, enclosed_white_coords)

    # 4. Change enclosed white pixels to blue in the output grid
    for r, c in enclosed_white_coords:
        output_grid[r, c] = 1 # Change to blue

    # 5. Change identified adjacent red pixels to blue in the output grid
    for r, c in red_coords_to_change:
        output_grid[r, c] = 1 # Change to blue

    # 6. Return the final transformed grid
    return output_grid