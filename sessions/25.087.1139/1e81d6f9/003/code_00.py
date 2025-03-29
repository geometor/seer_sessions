import numpy as np
from collections import deque

"""
Identifies all distinct contiguous objects composed solely of yellow (4) pixels in the input grid, considering 8-way adjacency. 
Counts how many of these objects consist of exactly one pixel (single yellow objects).
If the count of single yellow objects is exactly 6:
  Identifies the single yellow object with the minimum row index (and minimum column index as a tie-breaker).
  Changes the color of all *other* single yellow objects to white (0).
  Keeps the identified top-leftmost single yellow object yellow.
If the count of single yellow objects is not 6, the grid remains unchanged.
"""

def find_connected_object(grid, start_row, start_col, target_color, visited):
    """
    Finds all connected pixels of a target_color starting from (start_row, start_col)
    using Breadth-First Search (BFS) considering 8-way adjacency.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        target_color (int): The color of the object to find.
        visited (np.array): A boolean grid of the same shape as grid,
                             marking visited pixels.

    Returns:
        list: A list of (row, col) tuples representing the pixels in the object.
              Returns an empty list if the starting pixel is not the target color
              or has already been visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] != target_color:
        return []

    object_pixels = []
    queue = deque([(start_row, start_col)])
    visited[start_row, start_col] = True

    while queue:
        r, c = queue.popleft()
        object_pixels.append((r, c))

        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip self

                nr, nc = r + dr, c + dc

                # Check bounds, color, and visited status
                if 0 <= nr < rows and 0 <= nc < cols and \
                   not visited[nr, nc] and \
                   grid[nr, nc] == target_color:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    return object_pixels


def transform(input_grid):
    """
    Applies the transformation rule based on the count of single yellow pixels.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # Keep track of visited pixels to avoid processing the same object multiple times
    visited = np.zeros_like(input_grid_np, dtype=bool)

    target_color = 4  # Yellow
    replacement_color = 0 # White

    # 1. Identify all single yellow objects
    single_yellow_pixels = []
    for r in range(rows):
        for c in range(cols):
            # If the pixel is the target color and hasn't been visited yet
            if input_grid_np[r, c] == target_color and not visited[r, c]:
                # Find the complete connected object starting from this pixel
                object_pixels = find_connected_object(input_grid_np, r, c, target_color, visited)

                # Check if the object size is exactly 1
                if len(object_pixels) == 1:
                    # The object contains only the starting pixel (r, c)
                    single_yellow_pixels.append(object_pixels[0]) # Add (r, c) tuple

    # 2. Count the single yellow objects
    num_single_yellow = len(single_yellow_pixels)

    # 3. Check the condition (N == 6)
    if num_single_yellow == 6:
        # Condition met: Perform transformation
        # Create the output grid as a copy
        output_grid_np = np.copy(input_grid_np)

        # a. Find the top-leftmost single yellow pixel to preserve
        # Sort by row, then by column
        single_yellow_pixels.sort(key=lambda x: (x[0], x[1]))
        pixel_to_preserve = single_yellow_pixels[0]

        # b. Change all *other* single yellow pixels to white
        for r, c in single_yellow_pixels:
            if (r, c) != pixel_to_preserve:
                output_grid_np[r, c] = replacement_color

        # Convert the result back to a list of lists
        return output_grid_np.tolist()

    else:
        # Condition not met: Return the input grid unchanged
        return input_grid # Return original list of lists
