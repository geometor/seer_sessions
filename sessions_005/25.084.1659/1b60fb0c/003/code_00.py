import numpy as np
from collections import deque

"""
Identifies specific regions of white pixels (0) based on their relationship to blue pixels (1) and grid boundaries, then changes their color to red (2).

A contiguous region of white pixels is targeted for transformation if it meets either of the following conditions:
a) The white region is entirely surrounded by blue (1) pixels. All adjacent pixels outside the region are blue. Touching the grid boundary means it's not entirely surrounded by blue.
b) The white region is connected to the leftmost column (column 0) AND is NOT connected to the rightmost column (column width-1). Connectivity is defined by adjacency (up, down, left, right) through white pixels only.

All white pixels belonging to a targeted region are changed to red (2).
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()  # Initialize output_grid as a copy
    height, width = grid.shape

    # Constants for colors
    background_color = 0  # white
    boundary_color = 1  # blue
    fill_color = 2  # red

    # Keep track of visited white pixels to avoid processing regions multiple times
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each cell to find starting points of white regions
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited yet, start exploring its region
            if grid[r, c] == background_color and not visited[r, c]:
                
                # --- Start BFS to find the connected white region ---
                current_region_pixels = []
                queue = deque([(r, c)])
                visited[r, c] = True
                
                touches_left = False
                touches_right = False
                
                while queue:
                    row, col = queue.popleft()
                    current_region_pixels.append((row, col))

                    # Check boundary conditions for Condition B
                    if col == 0:
                        touches_left = True
                    if col == width - 1:
                        touches_right = True

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # If neighbor is white and not visited, add to queue and mark visited
                            if grid[nr, nc] == background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                # --- End BFS ---

                # --- Check Condition A: Completely Enclosed by Blue ---
                is_enclosed = True
                region_set = set(current_region_pixels) # For faster neighbor check
                for pr, pc in current_region_pixels:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = pr + dr, pc + dc
                        
                        # Check if neighbor is out of bounds
                        if not (0 <= nr < height and 0 <= nc < width):
                            is_enclosed = False
                            break # Touches boundary, cannot be enclosed

                        # Check if neighbor is outside the current region
                        if (nr, nc) not in region_set:
                            # If the neighbor outside the region is not blue, it's not enclosed
                            if grid[nr, nc] != boundary_color:
                                is_enclosed = False
                                break
                    if not is_enclosed:
                        break
                
                # --- Check Condition B: Touches Left but not Right ---
                is_left_bounded_only = touches_left and not touches_right

                # --- Apply Fill if either condition is met ---
                if is_enclosed or is_left_bounded_only:
                    for pr, pc in current_region_pixels:
                        output_grid[pr, pc] = fill_color

    # Convert back to list of lists before returning
    return output_grid.tolist()