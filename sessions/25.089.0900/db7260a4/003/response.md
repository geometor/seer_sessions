```python
import numpy as np
from collections import deque

"""
Conditionally fills regions or the bottom row based on a trigger pixel's location relative to a boundary structure.

1.  Create a copy of the input grid to serve as the output grid.
2.  Locate the single blue (1) pixel (the trigger) in the input grid. Note its coordinates (row, column).
3.  Change the trigger pixel's location in the output grid to white (0).
4.  Locate all red (2) pixels (the boundary structure) in the input grid.
5.  If no red pixels exist, change all pixels in the bottom row of the output grid to blue (1) and return.
6.  Determine the minimum and maximum column indices occupied by the red pixels (the horizontal span).
7.  Check if the trigger pixel's column index falls within the horizontal span (inclusive).
8.  Find all connected components of white (0) pixels in the current state of the output grid (using 4-directional adjacency).
9.  Identify which of these white components, if any, do *not* contain any pixels located on the grid boundary (row 0, last row, column 0, last column). These are the "non-boundary" components.
10. Apply the fill rule:
    *   If the trigger pixel's column was *within* the horizontal span *and* there is at least one non-boundary white component:
        *   Select the largest non-boundary component (the one with the most pixels).
        *   Change the color of all pixels within this selected component to blue (1) in the output grid.
    *   Else (either the trigger pixel's column was *outside* the span, or it was *inside* but there were *no* non-boundary white components):
        *   Change the color of all pixels in the bottom row (last row) of the output grid to blue (1).
11. Output the final modified grid.
"""


def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    coords = np.argwhere(grid == color)
    # Convert to list of tuples for easier handling, especially with sets
    return [tuple(coord) for coord in coords]

def find_connected_components(grid, color, connectivity=4):
    """
    Finds all connected components of a given color in the grid.
    Uses Breadth-First Search (BFS).
    """
    rows, cols = grid.shape
    visited = set()
    components = []
    
    # Define neighbor directions based on connectivity
    if connectivity == 4:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(rows):
        for c in range(cols):
            coord = (r, c)
            if grid[r, c] == color and coord not in visited:
                # Start BFS for a new component
                component = set()
                q = deque([coord])
                visited.add(coord)
                component.add(coord)

                while q:
                    curr_r, curr_c = q.popleft()
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        neighbor_coord = (nr, nc)
                        # Check bounds and color and if not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           neighbor_coord not in visited:
                            visited.add(neighbor_coord)
                            component.add(neighbor_coord)
                            q.append(neighbor_coord)
                
                if component:
                    components.append(component)
    return components

def check_boundary_touch(component, grid_shape):
    """
    Checks if any pixel in the component touches the grid boundary.
    """
    rows, cols = grid_shape
    max_row = rows - 1
    max_col = cols - 1
    for r, c in component:
        if r == 0 or r == max_row or c == 0 or c == max_col:
            return True
    return False


def transform(input_grid_list):
    """
    Transforms the input grid based on the described logic.
    """
    # 1. Initialize output grid
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 2. Locate trigger pixel
    trigger_coords = find_pixels(output_grid, 1) # Blue = 1
    if not trigger_coords:
        # No trigger found, return original grid (or handle as needed)
        return input_grid_list 
    trigger_coord = trigger_coords[0] # Assume exactly one trigger

    # 3. Change trigger pixel to white in output
    output_grid[trigger_coord] = 0 # White = 0

    # 4. Locate red boundary pixels
    red_coords = find_pixels(output_grid, 2) # Red = 2

    fill_bottom_row = False # Flag to determine final action

    # 5. Handle case of no red pixels
    if not red_coords:
        fill_bottom_row = True
    else:
        # 6. Determine horizontal span of red boundary
        red_cols = [c for r, c in red_coords]
        min_red_col = min(red_cols)
        max_red_col = max(red_cols)

        # 7. Check trigger position relative to span
        trigger_col = trigger_coord[1]
        is_trigger_inside_span = min_red_col <= trigger_col <= max_red_col

        # 8. Find all connected components of white pixels in the modified grid
        white_components = find_connected_components(output_grid, 0, connectivity=4)

        # 9. Identify non-boundary components
        non_boundary_components = []
        for component in white_components:
            if not check_boundary_touch(component, output_grid.shape):
                non_boundary_components.append(component)

        # 10. Apply fill rule
        if is_trigger_inside_span and non_boundary_components:
            # Find the largest non-boundary component
            largest_component = max(non_boundary_components, key=len)
            # Fill the largest component with blue
            for r, c in largest_component:
                output_grid[r, c] = 1 # Blue = 1
        else:
            # Trigger outside span OR (inside span but no non-boundary components)
            fill_bottom_row = True

    # Apply bottom row fill if flagged
    if fill_bottom_row:
        if rows > 0: # Ensure grid is not empty
             output_grid[rows - 1, :] = 1 # Fill last row with blue

    # 11. Return final grid
    return output_grid.tolist()
```