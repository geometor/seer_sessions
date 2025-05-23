import numpy as np
from collections import deque

"""
Transforms the input grid based on two main rules:
1. Fills enclosed white regions: White pixels (0) that are not connected to the grid border via a path of only white pixels (using 4-directional adjacency) are changed to blue (1).
2. Changes specific adjacent red pixels: Red pixels (2) that are part of a horizontal line segment of length 2 or more AND are adjacent (using 8-directional adjacency, including diagonals) to any of the enclosed white pixels (identified in rule 1) are also changed to blue (1).
All other pixels retain their original color.
"""

def find_reachable_white_pixels(grid):
    """
    Performs a Breadth-First Search (BFS) starting from all border white pixels
    to find all white pixels connected to the boundary using 4-directional movement.

    Args:
        grid (np.array): The input grid.

    Returns:
        np.array: A boolean grid of the same shape as input, where True indicates
                  a white pixel is reachable from the border.
    """
    height, width = grid.shape
    is_reachable = np.zeros((height, width), dtype=bool)
    queue = deque()

    # Add all white border pixels to the queue and mark as reachable
    for r in range(height):
        for c in [0, width - 1]:
            if grid[r, c] == 0 and not is_reachable[r, c]:
                is_reachable[r, c] = True
                queue.append((r, c))
    # Avoid adding corners twice
    for c in range(1, width - 1):
        for r in [0, height - 1]:
             if grid[r, c] == 0 and not is_reachable[r, c]:
                is_reachable[r, c] = True
                queue.append((r, c))

    # Perform BFS (4-directional neighbors: up, down, left, right)
    while queue:
        r, c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, color (must be white), and visited status
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and not is_reachable[nr, nc]:
                is_reachable[nr, nc] = True
                queue.append((nr, nc))

    return is_reachable

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    height, width = input_grid.shape
    # 1. Initialize Output Grid
    output_grid = np.copy(input_grid)

    # 2. Find Reachable White Pixels
    is_reachable = find_reachable_white_pixels(input_grid)

    # 3. Identify Enclosed White Pixel Coordinates
    enclosed_white_coords = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 0 and not is_reachable[r, c]:
                enclosed_white_coords.add((r, c))

    # 4. Fill Enclosed White Regions
    for r, c in enclosed_white_coords:
        output_grid[r, c] = 1 # Change to blue

    # 5. Identify Red Pixels to Change
    red_pixels_to_change_coords = set()
    # Define 8 neighbors (including diagonals)
    neighbors_8 = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

    for r in range(height):
        for c in range(width):
            # Check if pixel is red (2)
            if input_grid[r, c] == 2:
                # Check if part of horizontal red segment >= length 2
                is_horizontal = False
                # Check left neighbor
                if c > 0 and input_grid[r, c - 1] == 2:
                    is_horizontal = True
                # Check right neighbor
                if not is_horizontal and c < width - 1 and input_grid[r, c + 1] == 2:
                    is_horizontal = True

                if is_horizontal:
                    # Check 8 neighbors for adjacency to enclosed white pixels
                    is_adjacent_to_enclosed = False
                    for dr, dc in neighbors_8:
                        nr, nc = r + dr, c + dc
                        # Check bounds and if neighbor is in the enclosed set
                        if 0 <= nr < height and 0 <= nc < width and (nr, nc) in enclosed_white_coords:
                            is_adjacent_to_enclosed = True
                            break # Found an adjacent enclosed white pixel

                    # If criteria met, mark this red pixel for change
                    if is_adjacent_to_enclosed:
                        red_pixels_to_change_coords.add((r, c))

    # 6. Change Designated Red Pixels
    for r, c in red_pixels_to_change_coords:
        output_grid[r, c] = 1 # Change to blue

    # 7. Return Final Grid
    return output_grid