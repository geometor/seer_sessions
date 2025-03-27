import numpy as np

"""
Identify all distinct groups of connected azure (8) pixels in the input grid, considering 8-way connectivity (horizontal, vertical, and diagonal). Count the number of these distinct objects, let the count be N. Create a new N x N grid initialized with white (0). Set the pixels along the main diagonal (from top-left to bottom-right) of this new grid to azure (8). Return the resulting N x N grid.
"""

def _find_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in a grid using BFS.
    Considers 8-way connectivity (including diagonals).

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        int: The number of distinct objects found.
    """
    rows, cols = grid.shape
    visited = set()
    object_count = 0

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is the target color and not yet visited
            if grid[r, c] == target_color and (r, c) not in visited:
                # Found the start of a new object
                object_count += 1
                queue = [(r, c)]
                visited.add((r, c))

                # Perform BFS to find all connected pixels of this object
                while queue:
                    curr_r, curr_c = queue.pop(0)

                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip the pixel itself

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if the neighbor is within bounds
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if the neighbor has the target color and hasn't been visited
                                if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    queue.append((nr, nc))
    return object_count


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the count of azure objects.

    1. Counts the number (N) of distinct azure (8) objects (connected horizontally, vertically, or diagonally).
    2. Creates an N x N grid filled with white (0).
    3. Draws an azure (8) diagonal line from the top-left to the bottom-right corner.

    Args:
        input_grid (np.ndarray): The input grid containing azure objects.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Define the target color
    azure_color = 8
    background_color = 0

    # 1. Count the number of distinct azure objects
    num_objects = _find_objects(input_grid, azure_color)

    # Handle the case where N might be 0, although examples suggest N > 0
    if num_objects == 0:
        return np.array([[]], dtype=int) # Or handle as per potential edge case rules

    # 2. Create a new N x N grid initialized with the background color
    output_grid_size = num_objects
    output_grid = np.full((output_grid_size, output_grid_size), background_color, dtype=int)

    # 3. Draw the azure diagonal
    for i in range(output_grid_size):
        output_grid[i, i] = azure_color

    return output_grid
