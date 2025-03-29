import numpy as np
from collections import deque

"""
Identifies the two distinct non-white colors present in the input grid.
Finds all contiguous objects (shapes) formed by each of these two colors.
Creates an output grid where each object retains its original shape and position,
but its color is swapped with the other non-white color.
Background (white) pixels remain unchanged.
"""

def _find_object_pixels(grid: np.ndarray, start_r: int, start_c: int, visited: np.ndarray) -> list:
    """
    Finds all connected pixels of the same color starting from (start_r, start_c)
    using Breadth-First Search (BFS). Uses 4-connectivity.

    Args:
        grid: The input numpy array grid.
        start_r: The starting row coordinate.
        start_c: The starting column coordinate.
        visited: A boolean numpy array of the same shape as grid, marking visited pixels.

    Returns:
        A list of tuples, where each tuple is the (row, col) coordinate of a pixel
        belonging to the connected object. Returns an empty list if the starting
        pixel is background or already visited.
    """
    rows, cols = grid.shape
    start_color = grid[start_r, start_c]

    # Ignore background color or already visited pixels
    if start_color == 0 or visited[start_r, start_c]:
        return []

    object_pixels = []
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, if neighbor has the same color, and if not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and \
               grid[nr, nc] == start_color:
                visited[nr, nc] = True
                q.append((nr, nc))

    return object_pixels


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Swaps the colors of distinct objects in the grid.

    Identifies the two non-white colors (color1, color2). Finds all objects
    made of color1 and redraws them with color2 in the output. Finds all
    objects made of color2 and redraws them with color1 in the output.
    Background pixels remain white.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid with object colors swapped.
    """
    # --- Initialization ---
    rows, cols = input_grid.shape
    # Initialize output grid with background color (white = 0)
    output_grid = np.zeros_like(input_grid)
    # Keep track of visited pixels to avoid processing objects multiple times
    visited = np.zeros_like(input_grid, dtype=bool)

    # --- Color Identification ---
    # Find the unique non-zero color values
    unique_colors = np.unique(input_grid)
    non_white_colors = unique_colors[unique_colors != 0]

    # Ensure there are exactly two non-white colors
    if len(non_white_colors) != 2:
        # This case shouldn't happen based on the examples.
        # Return a copy of the input or an empty grid based on ARC rules interpretation.
        # Returning input copy seems safer.
        # print(f"Warning: Expected 2 non-white colors, found {len(non_white_colors)}. Returning original grid.")
        return input_grid.copy()

    color1 = non_white_colors[0]
    color2 = non_white_colors[1]

    # --- Object Processing and Color Swapping ---
    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            current_pixel_color = input_grid[r, c]

            # Check if the pixel is non-white and hasn't been visited yet
            if current_pixel_color != 0 and not visited[r, c]:
                # Determine the target color for the swap
                target_color = color2 if current_pixel_color == color1 else color1

                # Find all pixels belonging to this object
                object_coords = _find_object_pixels(input_grid, r, c, visited)

                # Draw the object onto the output grid with the swapped color
                for obj_r, obj_c in object_coords:
                    output_grid[obj_r, obj_c] = target_color

    return output_grid