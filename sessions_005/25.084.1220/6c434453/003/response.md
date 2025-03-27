```python
import numpy as np
from collections import deque

"""
Identifies blue shapes (color 1) in the input grid that fully enclose exactly 
one contiguous area of white pixels (color 0, a 'hole'). For each such identified 
blue shape, its pixels are changed to white (color 0), and the pixels of the 
single hole it encloses are changed to red (color 2) in the output grid. 
All other pixels retain their original colors.
"""

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

def touches_boundary(component, grid_shape):
    """
    Checks if any pixel in the component is on the grid boundary.

    Args:
        component (set): A set of (row, col) tuples representing the component.
        grid_shape (tuple): The (height, width) of the grid.

    Returns:
        bool: True if the component touches the boundary, False otherwise.
    """
    height, width = grid_shape
    for r, c in component:
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            return True
    return False

def get_neighbors(component, grid_shape):
    """
    Gets all unique neighboring coordinates of a component.
    Neighbors are defined using 4-connectivity.

    Args:
        component (set): A set of (row, col) tuples.
        grid_shape (tuple): The (height, width) of the grid.

    Returns:
        set: A set of (row, col) tuples representing neighboring coordinates
             that are within the grid bounds but not part of the component itself.
    """
    height, width = grid_shape
    neighbors = set()
    for r, c in component:
        # Check 4 neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds and not part of the component itself
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in component:
                neighbors.add((nr, nc))
    return neighbors

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    height, width = input_grid.shape
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Find all blue components (shapes)
    blue_components = find_connected_components(input_grid, 1)

    # 2. Find all white components
    white_components = find_connected_components(input_grid, 0)

    # 3. Create a mapping from pixel coordinate to the index of the blue component it belongs to
    # This allows quick checking of which blue component a neighbor belongs to.
    pixel_to_blue_component_idx = {}
    for idx, component in enumerate(blue_components):
        for r, c in component:
            pixel_to_blue_component_idx[(r, c)] = idx

    # 4. Identify which blue component encloses which white components (potential holes)
    # A dictionary to store the list of hole-components associated with each blue component index
    blue_component_holes = {idx: [] for idx in range(len(blue_components))}

    # Iterate through each white component to see if it's a hole
    for white_component in white_components:
        # A hole cannot touch the grid boundary
        if not touches_boundary(white_component, (height, width)):
            # Get all neighbors of the white component
            neighbors = get_neighbors(white_component, (height, width))

            # Check if this white component is a valid hole enclosed by a SINGLE blue component
            enclosing_blue_idx = -1 # Track the index of the potential enclosing blue component
            is_valid_hole = True
            if not neighbors: # A non-boundary component must have neighbors
                 is_valid_hole = False

            for nr, nc in neighbors:
                pixel_color = input_grid[nr, nc]
                # All neighbors MUST be blue (color 1)
                if pixel_color == 1:
                    # Check which blue component this neighbor belongs to
                    if (nr, nc) in pixel_to_blue_component_idx:
                        current_blue_idx = pixel_to_blue_component_idx[(nr, nc)]
                        # If this is the first blue neighbor found, record its component index
                        if enclosing_blue_idx == -1:
                            enclosing_blue_idx = current_blue_idx
                        # If a neighbor belongs to a DIFFERENT blue component, it's not a valid hole
                        elif enclosing_blue_idx != current_blue_idx:
                            is_valid_hole = False
                            break
                    else:
                        # This neighbor is blue but not part of any pre-identified component?
                        # This shouldn't happen if find_connected_components is correct.
                        # Treat as invalid for safety.
                        is_valid_hole = False
                        break
                else:
                    # If any neighbor is not blue, it's not a valid hole (must be fully surrounded by blue)
                    is_valid_hole = False
                    break

            # If the loop completed, all neighbors were blue, and they all belonged to the same blue component
            if is_valid_hole and enclosing_blue_idx != -1:
                # Add this white component (hole) to the list for the identified blue component
                blue_component_holes[enclosing_blue_idx].append(white_component)

    # 5. Modify the output grid based on blue components with exactly one hole
    for blue_idx, holes in blue_component_holes.items():
        # Check if this blue component has exactly one associated hole
        if len(holes) == 1:
            # Get the coordinates of the single hole
            single_hole_coords = holes[0]
            # Get the coordinates of the enclosing blue shape
            enclosing_blue_coords = blue_components[blue_idx]

            # Change the color of the enclosing blue pixels to white (0)
            for r, c in enclosing_blue_coords:
                # Check bounds just in case, although component coords should be valid
                if 0 <= r < height and 0 <= c < width:
                     output_grid[r, c] = 0

            # Change the color of the hole pixels to red (2)
            for r, c in single_hole_coords:
                # Check bounds just in case
                if 0 <= r < height and 0 <= c < width:
                     output_grid[r, c] = 2

    # Return the modified grid
    return output_grid
```