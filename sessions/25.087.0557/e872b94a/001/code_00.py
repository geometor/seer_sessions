"""
This program identifies distinct groups of connected gray (5) pixels in an input grid, where connectivity is defined by cardinal adjacency (up, down, left, right). The height of the output grid, which is a single column filled with white (0) pixels, is equal to the total count of these distinct gray objects found in the input grid.
"""

import numpy as np

def _find_objects(grid):
    """
    Finds and counts distinct connected objects of gray pixels (5) in the grid.
    Connectivity is cardinal (up, down, left, right).

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The number of distinct gray objects.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    object_count = 0

    for r in range(rows):
        for c in range(cols):
            # If we find a gray pixel that hasn't been visited yet, start a search
            if grid[r, c] == 5 and not visited[r, c]:
                object_count += 1
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0) # Use BFS

                    # Check cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == 5 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
    return object_count


def transform(input_grid):
    """
    Transforms the input grid by counting distinct gray (5) objects (connected cardinally)
    and creating a white (0) output column with height equal to that count.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array (N x 1) filled with 0s, where N is the
                  number of gray objects in the input_grid.
    """
    # Convert input list of lists to numpy array if necessary
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # 1. Find and count the distinct gray objects in the input grid
    num_objects = _find_objects(input_grid)

    # 2. Create the output grid: a column vector of height num_objects, filled with 0s
    # Ensure the output is a 2D array (N x 1) even if N=0 or N=1
    output_height = num_objects
    output_width = 1
    # Use np.zeros to create a grid filled with 0 (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    return output_grid