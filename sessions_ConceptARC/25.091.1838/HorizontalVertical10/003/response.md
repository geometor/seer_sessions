```python
"""
Transforms the input grid by adding a single line of azure (8) color along one edge.
The specific edge and orientation of the line depend on the orientation of the shapes present in the input grid.
Shapes are defined as contiguous blocks of the same non-background color.
If the grid contains only shapes that are strictly wider than tall (horizontal), a vertical azure line is added to the rightmost column.
Otherwise (if any shape is taller than wide (vertical), square, or if both horizontal and vertical shapes exist, or if no shapes exist), a horizontal azure line is added to the topmost row.
"""

import numpy as np
from typing import List, Tuple, Set

# ==================================
# Helper Functions
# ==================================

def find_objects_same_color(grid: np.ndarray, background_color: int = 0) -> List[Set[Tuple[int, int]]]:
    """
    Finds connected components (objects) of pixels with the same non-background color in the grid.
    Uses 4-way adjacency (up, down, left, right).

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background color (default 0).

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a connected object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            pixel_color = grid[r, c]
            # Check if the pixel is not background and not visited yet
            if pixel_color != background_color and (r, c) not in visited:
                obj_coords = set()
                q = [(r, c)]  # Queue for BFS
                visited.add((r, c))

                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.pop(0)
                    obj_coords.add((curr_r, curr_c))

                    # Check 4 adjacent neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, if neighbor has the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == pixel_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Calculates the height and width of the bounding box for a set of coordinates.

    Args:
        coords: A set of (row, col) tuples representing an object.

    Returns:
        A tuple containing the (height, width) of the bounding box.
        Returns (0, 0) if coords is empty.
    """
    if not coords:
        return 0, 0
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

# ==================================
# Transformation Function
# ==================================

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A List of Lists representing the input grid.

    Returns:
        A List of Lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape
    azure_color = 8

    # Handle empty grid case
    if rows == 0 or cols == 0:
        return output_grid.tolist()

    # Find all distinct objects (contiguous same-colored non-background pixels)
    objects = find_objects_same_color(input_np)

    # Determine object orientations
    has_horizontal = False
    has_vertical = False

    if not objects:
        # If no objects, default to adding a horizontal line at the top
        output_grid[0, :] = azure_color
        return output_grid.tolist()

    # Analyze dimensions of each object
    for obj_coords in objects:
        h, w = get_bounding_box(obj_coords)
        if w > h:
            has_horizontal = True
        if h > w:
            has_vertical = True
        # Optional: Check if both types are found early to potentially break loop
        # if has_horizontal and has_vertical:
        #     break # Both found, outcome is determined ('else' case)

    # Apply transformation based on the presence of object orientations
    if has_horizontal and not has_vertical:
        # Only horizontal objects found: add vertical line to the rightmost column
        output_grid[:, -1] = azure_color
    else:
        # Vertical objects found, or both found, or only square objects found:
        # Add horizontal line to the topmost row
        output_grid[0, :] = azure_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```