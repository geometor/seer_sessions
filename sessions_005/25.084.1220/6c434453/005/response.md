```python
"""
Identifies blue shapes (color 1) that enclose exactly one single white pixel (color 0).
For each such identified blue shape and its single white hole:
1. The original white hole pixel is changed to red (color 2).
2. The four orthogonal neighbors of the white hole pixel (which must be part of the blue shape) are also changed to red (color 2). These five red pixels form a '+' shape centered on the original hole.
3. All other pixels belonging to the original blue shape (those not part of the red '+') are changed to white (color 0).
4. All other pixels in the grid retain their original colors.
"""

import numpy as np
from collections import deque

# --- Helper Functions ---

def find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in the grid.
    Uses 4-connectivity (up, down, left, right).

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the components to find.

    Returns:
        list: A list of components. Each component is a set of (row, col) tuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            # If the pixel has the target color and hasn't been visited yet
            if grid[r, c] == target_color and not visited[r, c]:
                # Start a BFS to find the connected component
                component = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                component.add((nr, nc))
                                q.append((nr, nc))
                # Add the found component to the list
                components.append(component)
    return components

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    height, width = input_grid.shape
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Find all blue components (color 1)
    blue_components = find_connected_components(input_grid, 1)

    # 2. Find all white components (color 0)
    white_components = find_connected_components(input_grid, 0)

    # 3. Create a mapping from pixel coordinate to the index of the blue component it belongs to
    pixel_to_blue_component_idx = {}
    for idx, component in enumerate(blue_components):
        for r, c in component:
            pixel_to_blue_component_idx[(r, c)] = idx

    # 4. Identify target transformations: (blue_component_coords, hole_coord)
    targets = []
    for white_component in white_components:
        # Check if the white component is a single pixel
        if len(white_component) == 1:
            hole_coord = list(white_component)[0]
            r, c = hole_coord

            # Check if the hole touches the boundary
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                continue # Holes touching boundary are ignored

            # Check the 4 orthogonal neighbors
            neighbors = []
            valid_neighbors = True
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Neighbor must be within bounds
                if 0 <= nr < height and 0 <= nc < width:
                    neighbors.append((nr, nc))
                else:
                    # Should not happen if hole isn't on boundary, but check for safety
                    valid_neighbors = False
                    break

            if not valid_neighbors or len(neighbors) != 4: # Ensure exactly 4 neighbors exist
                continue

            # Check if all neighbors are blue and belong to the *same* blue component
            enclosing_blue_idx = None
            is_valid_hole = True
            for nr, nc in neighbors:
                if input_grid[nr, nc] != 1: # Neighbor is not blue
                    is_valid_hole = False
                    break
                # Neighbor is blue, check which component it belongs to
                if (nr, nc) not in pixel_to_blue_component_idx:
                     # This blue pixel isn't part of any found component? Should not happen.
                     is_valid_hole = False
                     break

                current_blue_idx = pixel_to_blue_component_idx[(nr, nc)]
                if enclosing_blue_idx is None:
                    enclosing_blue_idx = current_blue_idx # First blue neighbor found
                elif enclosing_blue_idx != current_blue_idx:
                    # Neighbor belongs to a different blue component
                    is_valid_hole = False
                    break

            # If all checks passed, store the target
            if is_valid_hole and enclosing_blue_idx is not None:
                targets.append((blue_components[enclosing_blue_idx], hole_coord))

    # 5. Apply transformations based on identified targets
    for blue_shape_coords, hole_coord in targets:
        r, c = hole_coord

        # Define the coordinates for the red '+' shape
        plus_coords = set()
        plus_coords.add(hole_coord) # Center
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Add neighbor if within bounds (should always be true for valid targets)
            if 0 <= nr < height and 0 <= nc < width:
                plus_coords.add((nr, nc))

        # Iterate through the original blue shape pixels
        for br, bc in blue_shape_coords:
            # Check if this blue pixel is part of the '+' shape
            if (br, bc) in plus_coords:
                # Change to red (color 2)
                if 0 <= br < height and 0 <= bc < width: # Bounds check for safety
                    output_grid[br, bc] = 2
            else:
                # Change to white (color 0)
                 if 0 <= br < height and 0 <= bc < width: # Bounds check for safety
                    output_grid[br, bc] = 0

        # Ensure the center (original hole) is red
        if 0 <= r < height and 0 <= c < width: # Bounds check for safety
             output_grid[r, c] = 2

    # Return the modified grid
    return output_grid
```