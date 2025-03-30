```python
import numpy as np
from collections import deque

"""
Transforms the input grid by extending green shapes towards associated magenta markers.

1. Identify all distinct contiguous green (3) shapes and their initial bounding boxes.
2. Identify all magenta (6) marker pixels.
3. For each green shape, calculate its final extended bounding box:
    - Start with the initial bounding box.
    - Check each magenta marker for horizontal or vertical alignment with the *initial* bounding box.
    - If a marker is aligned and outside the initial box, expand the corresponding edge of the bounding box towards the marker, stopping one pixel short. Use min/max to handle multiple markers extending the same edge.
4. Create the output grid by filling the area within each calculated final extended bounding box with green (3), *unless* the pixel corresponds to a magenta (6) marker in the input grid. Magenta markers are preserved.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              - 'pixels': A set of (row, col) tuples for the object's pixels.
              - 'bbox': The bounding box (min_row, max_row, min_col, max_col).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c
                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                if obj_pixels:
                    objects.append({'pixels': obj_pixels, 'bbox': (min_r, max_r, min_c, max_c)})
    return objects

def find_pixels(grid, color):
    """
    Finds the coordinates of all pixels of a specific color.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find.

    Returns:
        list: A list of (row, col) tuples for pixels of the specified color.
    """
    return list(zip(*np.where(grid == color)))


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # 1. Identify Objects
    green_shapes = find_objects(input_grid, 3)
    magenta_markers = find_pixels(input_grid, 6)

    # Store the final extended bounding boxes for each shape
    extended_bboxes = []

    # 2. Calculate Extensions for each green shape
    for shape in green_shapes:
        # Get the initial bounding box
        min_r, max_r, min_c, max_c = shape['bbox']
        # Initialize the extended bounding box with the initial values
        ext_min_r, ext_max_r = min_r, max_r
        ext_min_c, ext_max_c = min_c, max_c

        # Check each marker for association and update extended bounds
        for m_r, m_c in magenta_markers:
            # Check horizontal alignment (marker row within shape's initial row span)
            if min_r <= m_r <= max_r:
                # Marker is to the right of the initial bbox
                if m_c > max_c:
                    ext_max_c = max(ext_max_c, m_c - 1)
                # Marker is to the left of the initial bbox
                elif m_c < min_c:
                    ext_min_c = min(ext_min_c, m_c + 1)

            # Check vertical alignment (marker col within shape's initial col span)
            elif min_c <= m_c <= max_c:
                 # Marker is below the initial bbox
                if m_r > max_r:
                    ext_max_r = max(ext_max_r, m_r - 1)
                # Marker is above the initial bbox
                elif m_r < min_r:
                    ext_min_r = min(ext_min_r, m_r + 1)
        
        # Store the calculated final extended bounding box for this shape
        extended_bboxes.append((ext_min_r, ext_max_r, ext_min_c, ext_max_c))

    # 4. Fill Extended Areas in the output grid
    # Note: We fill based on *all* extended boxes combined conceptually.
    # If a pixel falls within *any* extended box, it becomes green (unless it's a marker).
    for ext_min_r, ext_max_r, ext_min_c, ext_max_c in extended_bboxes:
        # Iterate through every pixel within this extended bounding box
        for r in range(ext_min_r, ext_max_r + 1):
            for c in range(ext_min_c, ext_max_c + 1):
                # Ensure coordinates are within the grid bounds (safety check)
                if 0 <= r < rows and 0 <= c < cols:
                    # Check the *original* input grid for a magenta marker
                    if input_grid[r, c] != 6:
                        # If not a marker, fill with green in the output grid
                        output_grid[r, c] = 3

    # 5. Final Result: The output grid now contains the filled areas
    return output_grid
```