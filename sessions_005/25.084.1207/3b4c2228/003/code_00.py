import numpy as np
from collections import deque

def _find_objects(grid, color):
    """
    Finds and counts distinct contiguous objects of a specified color in the grid.
    Uses 4-connectivity (up, down, left, right).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        int: The number of distinct objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    object_count = 0

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                object_count += 1
                # Start a search (BFS) to find all connected pixels of this object
                queue = deque([(r, c)])
                visited[r, c] = True
                while queue:
                    row, col = queue.popleft()
                    # Check all 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
    return object_count

def transform(input_grid):
    """
    Transforms the input grid based on counting green and red objects and applying a specific rule set.

    1. Initialize a 3x3 output grid filled with white pixels (color 0).
    2. Identify all distinct contiguous objects composed of green pixels (color 3)
       in the input grid, considering pixels connected horizontally or vertically
       as part of the same object. Let the total count of these green objects be `num_green`.
    3. Identify all distinct contiguous objects composed of red pixels (color 2)
       in the input grid, using the same connectivity rule. Let the total count
       of these red objects be `num_red`.
    4. Determine a value `N` based on comparing `num_green` and `num_red`:
        *   If `num_green` is less than `num_red`, set `N` to 1.
        *   If `num_green` is equal to `num_red`:
            *   If `num_green` (or `num_red`) is 3 or greater, set `N` to 2.
            *   Otherwise (if `num_green` is less than 3), set `N` to 1.
        *   If `num_green` is greater than `num_red`:
            *   Calculate the difference: `diff = num_green - num_red`.
            *   If `diff` is exactly 1, set `N` to 2.
            *   If `diff` is 2 or more:
                *   If `num_red` is exactly 1, set `N` to 2.
                *   If `num_red` is 2 or more, set `N` to 3.
    5. Fill the main diagonal of the 3x3 output grid with blue pixels (color 1),
       starting from the top-left corner (0,0). Place exactly `N` blue pixels
       along this diagonal (i.e., at positions `(0,0)`, `(1,1)`, ..., `(N-1, N-1)`),
       ensuring not to exceed the grid boundaries.
    6. The resulting 3x3 grid is the final output.
    """
    # Initialize a 3x3 output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Count green (3) and red (2) objects using 4-connectivity
    num_green = _find_objects(input_grid, 3)
    num_red = _find_objects(input_grid, 2)

    # Determine the value N based on the comparison rules
    n_blue_pixels = 0 # Default value
    if num_green < num_red:
        n_blue_pixels = 1
    elif num_green == num_red:
        if num_green >= 3:
             n_blue_pixels = 2
        else: # num_green is 0, 1, or 2
             n_blue_pixels = 1
    else: # num_green > num_red
        diff = num_green - num_red
        if diff == 1:
            n_blue_pixels = 2
        elif diff >= 2:
            if num_red == 1:
                n_blue_pixels = 2
            elif num_red >= 2:
                n_blue_pixels = 3
            # Note: If num_red is 0 and diff >= 2, n_blue_pixels remains 0 based on this logic.
            # However, the examples don't cover this specific edge case.
            # Example 2 (5g, 1r, diff=4) -> N=2, covered by num_red == 1.
            # Example 4 (4g, 2r, diff=2) -> N=3, covered by num_red >= 2.
            # Let's assume the derived logic is complete for the given examples.

    # Place N blue (1) pixels on the main diagonal
    for i in range(n_blue_pixels):
        if i < 3: # Ensure we don't go out of bounds for the 3x3 grid
            output_grid[i, i] = 1

    return output_grid