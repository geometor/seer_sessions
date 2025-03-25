```python
"""
1.  **Identify Frame Components:** Frame components are objects that touch any edge (top, bottom, left, or right) of the input grid. There can be multiple frame components, and they can have different colors.
2.  **Identify Inside Objects:** Inside objects are any objects that are *not* frame components (i.e., they don't touch any edge of the grid).
3.  **Determine Frame and Inside Object Arrangement:**
    *   If the input grid height is greater than its width, the arrangement is considered "vertical".
    *   If the input grid height is less than or equal to its width, the arrangement is considered "horizontal".
4.  **Create Output Grid:**
    *   **Vertical Arrangement:** The output grid has the same height as the input grid. The output grid's width is the sum of the widths of a single column to represent the combined frame and a column for each of the inside objects.
    *   **Horizontal Arrangement:** The output grid has the same width as the input grid. The output grid's height is the sum of one row for the frame components, plus the heights of each of the inside objects.
5.  **Reconstruct Frame Components:**
    *   **Vertical Arrangement:** Reconstruct the frame components in the first *column* of the output grid. All frame components are "merged" into this single column, maintaining their vertical positions.
    *   **Horizontal Arrangement:** Reconstruct the frame components in the first *row* of the output grid. Maintain their horizontal positions,
6.  **Place Inside Objects:**
    *   **Vertical Arrangement:** Place each inside object in subsequent columns. Preserve the top-to-bottom and left-to-right order of the inside objects as they appear in the input. Each inside object occupies its own column, and is placed adjacent to the frame or the previous object.
    *   **Horizontal Arrangement:** Place each inside object in subsequent rows. Preserve the top-to-bottom and left-to-right order of the objects. Each object occupies its own row, and is placed adjacent to the frame or previous object.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (regions of the same color) in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(row + dr, col + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_frame_components(grid):
    """Identifies objects touching the border."""
    rows, cols = grid.shape
    all_objects = find_objects(grid)
    frame_components = []
    for obj in all_objects:
        for r, c in obj:
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                frame_components.append(obj)
                break  # Move to the next object once one part is found on the border
    return frame_components

def get_inside_objects(grid, frame_components):
    """Returns objects that are *not* frame components."""
    all_objects = find_objects(grid)
    inside_objects = [obj for obj in all_objects if obj not in frame_components]
    inside_objects.sort(key=lambda obj: (min(r for r, _ in obj), min(c for _, c in obj)))
    return inside_objects

def get_object_dimensions(object, grid):
    """Calculates the bounding box dimensions (width, height) of an object."""
    min_row = min(r for r, _ in object)
    max_row = max(r for r, _ in object)
    min_col = min(c for _, c in object)
    max_col = max(c for _, c in object)
    return max_col - min_col + 1, max_row - min_row + 1

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Frame Components
    frame_components = get_frame_components(input_grid)

    # 2. Identify Inside Objects
    inside_objects = get_inside_objects(input_grid, frame_components)

    # 3. Determine Arrangement
    vertical_arrangement = rows > cols

    # 4. Create Output Grid
    if vertical_arrangement:
        # Vertical Arrangement
        output_width = 1  # For the frame
        for obj in inside_objects:
            obj_width, _ = get_object_dimensions(obj, input_grid)
            output_width += obj_width
        output_grid = np.full((rows, output_width), -1, dtype=int) # Fill with -1 for now
    else:
        # Horizontal Arrangement
        output_height = 1 # For the frame
        for obj in inside_objects:
            _, obj_height = get_object_dimensions(obj, input_grid)
            output_height += obj_height
        output_grid = np.full((output_height, cols), -1, dtype=int) # Fill with -1

    # 5. Reconstruct Frame Components
    if vertical_arrangement:
        for r in range(rows):
          for c in range(cols):
            if (r,c) in set().union(*frame_components):
              output_grid[r,0] = input_grid[r,c]

    else: # horizontal
      for r in range(rows):
        for c in range(cols):
          if (r,c) in set().union(*frame_components):
            output_grid[0, c] = input_grid[r,c]

    # 6. Place Inside Objects
    if vertical_arrangement:
        col_offset = 1
        for obj in inside_objects:
            obj_width, obj_height = get_object_dimensions(obj, input_grid)
            min_row = min(r for r, _ in obj)
            min_col = min(c for _, c in obj)
            for r, c in obj:
                output_grid[r, col_offset + c - min_col] = input_grid[r, c]
            col_offset += obj_width

    else: # horizontal
        row_offset = 1
        for obj in inside_objects:
            obj_width, obj_height = get_object_dimensions(obj, input_grid)
            min_row = min(r for r, _ in obj)
            for r, c in obj:
                output_grid[row_offset + r - min_row, c] = input_grid[r, c]
            row_offset += obj_height
    output_grid = np.where(output_grid == -1, 0, output_grid) # fill empty with black

    return output_grid.tolist()
```