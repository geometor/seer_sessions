```python
"""
1.  **Identify the Frame:** Determine the outermost rows and columns (the "frame") of the input grid. Note the colors present in the frame.
2.  **Identify Inside Objects:** Identify all contiguous objects (clusters of the same color) that are *not* part of the frame. Preserve their color and order from top-to-bottom, and left-to-right.
3. **Create Output:**
   * Example 1 - The frame of the input is represented as the first column of the output. The objects inside the frame from the input grid are stacked next to the frame, preserving order.
   * Example 2 - The frame of the input is presented as the first *row* of the output. The objects inside the input frame are stacked *above* the frame, preserving order.
4. **Resize and Populate:**
    *  Example 1: The output grid has the same number of rows (height) as the input. The output width is equal to the number of inside objects + 1 (for the frame).
   * Example 2: The output grid has the same number of columns (width) as the input grid. The output height is determined by the number of inside objects, plus one (for the frame).
5. **Object Placement:** Inside objects are placed next to the frame, preserving their colors and original order.
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

def get_frame_coords(grid):
    """Returns a set of (row, col) tuples representing the frame."""
    rows, cols = grid.shape
    frame = set()
    for r in range(rows):
        frame.add((r, 0))
        frame.add((r, cols - 1))
    for c in range(1, cols - 1):
        frame.add((0, c))
        frame.add((rows - 1, c))
    return frame


def get_inside_objects(grid, frame_coords):
    """
    Returns a list of objects inside the frame, preserving their original order.
    """
    all_objects = find_objects(grid)
    inside_objects = []
    for obj in all_objects:
        if not any((r, c) in frame_coords for r, c in obj):
            inside_objects.append(obj)
    return inside_objects

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the Frame
    frame_coords = get_frame_coords(input_grid)
    frame_objects = []
    for obj in find_objects(input_grid):
      if any((r,c) in frame_coords for r, c in obj):
        frame_objects.append(obj)

    # 2. Identify Inside Objects
    inside_objects = get_inside_objects(input_grid, frame_coords)

    # 3. & 4. Create and Resize Output Grid
    if rows > cols:  # Example 1 type
        output_grid = np.full((rows, len(inside_objects) + 1), -1)

        # Place frame objects in the first column
        frame_row_index = 0
        for obj in frame_objects:
            for r, c in obj:
              if frame_row_index < output_grid.shape[0]:
                output_grid[frame_row_index, 0] = input_grid[r,c]
                frame_row_index += 1

        # Place inside objects starting from the second column
        col_index = 1
        for obj in inside_objects:
            for r, c in obj:
              if r < output_grid.shape[0]:
                output_grid[r, col_index] = input_grid[r, c]
            
            col_index += 1


    else:  # Example 2 type
        output_grid = np.full((len(inside_objects) + 1, cols), -1)

        # Place frame along first row
        frame_col_index = 0
        for obj in frame_objects:
            for r,c in obj:
                if frame_col_index < output_grid.shape[1]:
                    output_grid[0, frame_col_index] = input_grid[r,c]
                    frame_col_index+=1

        # Place inside objects, stacked
        row_index = 1
        for obj in inside_objects:
          for r, c in obj:
              if c < output_grid.shape[1]:
                output_grid[row_index, c] = input_grid[r, c]

          row_index += 1
            
    output_grid = np.where(output_grid == -1, 9, output_grid) # Fill empty with 9

    return output_grid.tolist()
```