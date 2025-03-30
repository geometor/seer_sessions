```python
import numpy as np
from collections import deque

"""
Perform a flood fill transformation starting from the single red pixel (2) in the input grid.

1.  Identify the single red pixel (color 2) in the input grid; this is the starting point for the transformation.
2.  Perform a flood fill operation (using Breadth-First Search) starting from this red pixel.
3.  The flood fill spreads only to orthogonally adjacent white pixels (color 0).
4.  The flood fill is blocked by azure pixels (color 8), other non-white pixels, and the boundaries of the grid. These blocking pixels remain unchanged.
5.  All white pixels reachable by the flood fill from the starting red pixel, by moving only through white pixels, change their color to red (2).
6.  The original starting red pixel remains red.
7.  White pixels that are not reachable by the flood fill remain white.
8.  The final output grid contains the original non-white pixels (like azure), the original red pixel, the newly filled red pixels, and the remaining unreachable white pixels.
"""


# Helper function to find the starting pixel
def find_start_pixel(grid: np.ndarray, color: int) -> tuple[int, int] | None:
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None # Return None if the color is not found


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a flood fill transformation starting from the red pixel (2),
    filling adjacent white pixels (0) until blocked by azure pixels (8),
    other non-white pixels, or grid boundaries.
    """
    # Initialize output_grid as a copy of the input grid
    # The transformation will be applied to this copy.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define the colors involved in the transformation
    fill_color = 2       # Red: The color to fill with and the start pixel color
    background_color = 0 # White: The color of pixels eligible to be filled
    # Barrier colors (like azure=8) are handled implicitly by not being background_color

    # 1. Find the starting red pixel coordinates
    start_coord = find_start_pixel(input_grid, fill_color)

    # If no starting pixel (red=2) is found, return the original grid.
    # This handles potential edge cases, although the task implies a start pixel exists.
    if start_coord is None:
        # print("Warning: No start pixel (red=2) found.") # Keep commented for ARC task
        return output_grid

    # 2. Initialize data structures for Breadth-First Search (BFS) flood fill
    # The queue stores coordinates (row, col) of pixels to be processed.
    # Initialize queue with the starting pixel.
    queue = deque([start_coord])
    # The visited set stores coordinates of pixels that have been processed or added to the queue.
    # We specifically track pixels that we intend to fill (originally background color)
    # and the starting pixel itself to prevent cycles and redundant checks.
    visited = set([start_coord]) # Mark the starting pixel as visited

    # Define the four orthogonal directions (change in row, change in col)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # 3. Start the flood fill process (BFS)
    while queue:
        # Get the current coordinate from the front of the queue
        r, c = queue.popleft()
        # The pixel at (r, c) is guaranteed to be the fill_color (red)
        # either the start pixel or one filled in a previous step.

        # Explore the orthogonal neighbors of the current pixel
        for dr, dc in directions:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)

                # Check two conditions for filling the neighbor:
                # a) The neighbor pixel in the *original* input grid must be the background color (white).
                # b) The neighbor pixel must not have been visited yet (i.e., not already processed or added to the queue).
                if input_grid[nr, nc] == background_color and neighbor_coord not in visited:
                    # If both conditions are met:
                    # Mark this neighbor as visited to avoid re-processing
                    visited.add(neighbor_coord)
                    # Change the color of this neighbor to the fill color (red) in the output grid
                    output_grid[nr, nc] = fill_color
                    # Add this newly filled neighbor to the queue, so its own neighbors can be explored
                    queue.append(neighbor_coord)

                # Implicitly handles barriers:
                # - If neighbor is out of bounds, loop condition `0 <= nr < rows...` fails.
                # - If neighbor is already visited, `neighbor_coord not in visited` fails.
                # - If neighbor is azure (8) or any color other than white (0),
                #   `input_grid[nr, nc] == background_color` fails.
                # In all these cases, the fill does not proceed into or through that neighbor
                # from the current pixel (r, c).

    # 4. Return the modified grid after the flood fill is complete
    return output_grid
```