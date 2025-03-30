import numpy as np
from collections import deque

"""
The transformation identifies the connected component of non-Azure (8) pixels containing the single Red (2) start pixel. Then, it performs a flood fill starting from the Red pixel, changing only White (0) pixels within that specific component to Red (2). Azure pixels act as barriers defining the component boundaries. Pixels outside this component remain unchanged.

1.  Find the coordinates of the single Red (2) pixel. If none is found, return the input grid unchanged.
2.  Identify the connected component of pixels reachable from the Red start pixel by moving orthogonally through non-Azure (8) pixels. Store the coordinates of pixels in this component.
3.  Initialize the output grid as a copy of the input grid.
4.  Perform a Breadth-First Search (BFS) flood fill starting from the Red pixel:
    a. Initialize a queue with the start coordinate.
    b. Initialize a set `visited_fill` to track pixels visited during *this fill step*, adding the start coordinate.
    c. While the queue is not empty:
        i. Dequeue the current pixel coordinate `(r, c)`.
        ii. Examine its orthogonal neighbours `(nr, nc)`.
        iii. For a neighbour to be filled and added to the queue, it must satisfy all the following conditions:
            - Be within the grid boundaries.
            - Be part of the connected component identified in step 2.
            - Have not been visited yet in *this fill step* (not in `visited_fill`).
            - Be originally White (0) in the `input_grid`.
        iv. If all conditions are met for neighbour `(nr, nc)`:
            - Set `output_grid[nr, nc]` to Red (2).
            - Add `(nr, nc)` to `visited_fill`.
            - Enqueue `(nr, nc)`.
5.  Return the modified `output_grid`.
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
    Fills white areas connected to the red pixel within the non-azure component.
    """
    rows, cols = input_grid.shape
    start_color = 2      # Red
    background_color = 0 # White
    barrier_color = 8    # Azure
    fill_color = 2       # Red

    # 1. Find the starting Red (2) pixel
    start_coord = find_start_pixel(input_grid, start_color)
    if start_coord is None:
        return np.copy(input_grid) # No start pixel, return copy

    # 2. Identify the connected component of non-Azure pixels containing the start pixel
    component_coords = set()
    component_queue = deque([start_coord])
    visited_component = set([start_coord])
    component_coords.add(start_coord)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    while component_queue:
        r, c = component_queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor_coord = (nr, nc)

            # Check if neighbor is within bounds, not a barrier, and not visited for component finding
            if 0 <= nr < rows and 0 <= nc < cols and \
               input_grid[nr, nc] != barrier_color and \
               neighbor_coord not in visited_component:
                visited_component.add(neighbor_coord)
                component_coords.add(neighbor_coord)
                component_queue.append(neighbor_coord)

    # 3. Initialize the output grid
    output_grid = np.copy(input_grid)

    # 4. Perform flood fill within the identified component, changing only White pixels
    fill_queue = deque()
    visited_fill = set()

    # Only start the fill if the start coordinate itself is part of the component
    # (which it always should be by definition, but good check)
    if start_coord in component_coords:
        fill_queue.append(start_coord)
        visited_fill.add(start_coord)
        # Note: The starting pixel itself is already Red, so no color change needed for it.

    while fill_queue:
        r, c = fill_queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor_coord = (nr, nc)

            # Check conditions for filling the neighbor:
            # - In bounds
            # - Part of the identified component
            # - Not visited during *this fill*
            # - Originally White (0)
            if 0 <= nr < rows and 0 <= nc < cols and \
               neighbor_coord in component_coords and \
               neighbor_coord not in visited_fill and \
               input_grid[nr, nc] == background_color:

                # If all conditions met, fill the neighbor
                visited_fill.add(neighbor_coord)
                output_grid[nr, nc] = fill_color
                fill_queue.append(neighbor_coord)

    # 5. Return the final grid
    return output_grid