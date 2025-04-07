import copy
from collections import deque

"""
Transforms an input grid by identifying connected components of a target value (6), 
calculating properties of each component (size and shape for size 3 components), 
determining a replacement value based on these properties, and updating the grid. 
The background value (7) remains unchanged.

Transformation Rules:
- Identify connected components of '6's using 4-way adjacency.
- Calculate component size.
- For size 3 components, calculate bounding box area (height * width).
- Replace component cells based on the following map:
    - Size 2 -> 9
    - Size 3, BBox Area 3 (Line) -> 2
    - Size 3, BBox Area 4 (L-shape) -> 4
    - Size 4 -> 8
    - Size 5 -> 3
    - Size 6 -> 5
- Keep '7's unchanged.
"""

def _calculate_bounding_box_area(component_coords):
    """Calculates the area of the minimum bounding box for a component."""
    if not component_coords:
        return 0
    min_r = min(r for r, c in component_coords)
    max_r = max(r for r, c in component_coords)
    min_c = min(c for r, c in component_coords)
    max_c = max(c for r, c in component_coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

def _get_replacement_value(size, bbox_area=None):
    """Determines the replacement value based on component size and bounding box area."""
    if size == 2:
        return 9
    elif size == 3:
        if bbox_area == 3:  # Line shape
            return 2
        elif bbox_area == 4:  # L-shape
            return 4
        else:
            # Default or error case for size 3 if bbox area is unexpected
            # Based on examples, only 3 and 4 are expected.
             return 7 # Or raise an error
    elif size == 4:
        return 8
    elif size == 5:
        return 3
    elif size == 6:
        return 5
    else:
        # Default or error case for unexpected sizes
        return 7 # Or raise an error

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Constants
    target_value = 6
    background_value = 7 # Although not explicitly used in replacement logic here, it's the default.

    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])
    visited = set() # Keep track of visited cells to avoid re-processing

    # Iterate through each cell to find components
    for r in range(rows):
        for c in range(cols):
            # Check if the cell contains the target value and hasn't been visited yet
            if input_grid[r][c] == target_value and (r, c) not in visited:
                # Found the start of a new component, perform BFS to find all its cells
                component_coords = []
                q = deque([(r, c)])
                visited.add((r, c))
                component_coords.append((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    # Explore 4-way neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if the neighbor is part of the component
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           input_grid[nr][nc] == target_value and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            component_coords.append((nr, nc))

                # Component found, calculate its properties and determine replacement value
                component_size = len(component_coords)
                bbox_area = None
                if component_size == 3:
                    bbox_area = _calculate_bounding_box_area(component_coords)

                replacement_value = _get_replacement_value(component_size, bbox_area)

                # Update the output grid for all cells in this component
                for comp_r, comp_c in component_coords:
                    output_grid[comp_r][comp_c] = replacement_value

    return output_grid