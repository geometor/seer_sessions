# 846bdb03 • 006 • refine_coder

---
```python
"""
The transformation extracts the connected red component, the adjacent blue component, and specific yellow pixels from the input grid. It determines the output grid size dynamically based on the bounding box of the red and blue components and places these components, maintaining their relative positions. Yellow pixels are included based on specific criteria related to the other components.
"""

import numpy as np

def find_object(grid, color):
    """Finds coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def extract_connected_component(grid, start_coord, color):
    """Extracts a connected component of a given color using Breadth-First Search."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    component = []
    queue = [tuple(start_coord)]

    while queue:
        r, c = queue.pop(0)
        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and not visited[r, c]:
            visited[r, c] = True
            component.append((r, c))
            # Add adjacent cells to the queue
            queue.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
    return np.array(component)

def get_corners(grid):
     """returns the coordinates for the 4 corners of the grid"""
     rows, cols = grid.shape
     return [(0,0), (0, cols-1), (rows-1, 0), (rows-1, cols-1)]

def transform(input_grid):
    # 1. Identify Components
    red_pixels = find_object(input_grid, 2)
    blue_pixels = find_object(input_grid, 1)
    yellow_pixels = find_object(input_grid, 4)

    # 2. Extract Red and Blue Components
    red_component = []
    if len(red_pixels) > 0:
        red_component = extract_connected_component(input_grid, red_pixels[0], 2)

    blue_component = []
    if len(blue_pixels) > 0 and len(red_component) > 0:
        # Find blue pixel adjacent to red
        start_blue = None
        for br, bc in blue_pixels:
            for rr, rc in red_component:
                if abs(br - rr) + abs(bc - rc) == 1:
                    start_blue = (br, bc)
                    break
            if start_blue:
                break
        if start_blue:
            blue_component = extract_connected_component(input_grid, start_blue, 1)

    # 3. Determine Output Size
    if len(red_component) > 0 or len(blue_component) > 0:
        all_points = np.concatenate((red_component, blue_component))
        min_row = np.min(all_points[:, 0])
        max_row = np.max(all_points[:, 0])
        min_col = np.min(all_points[:, 1])
        max_col = np.max(all_points[:, 1])

        output_rows = max_row - min_row + 1
        output_cols = max_col - min_col + 1
    else:
      output_rows = 0
      output_cols = 0

    # Initialize output_grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)


    # 4. Place Red and Blue
    if len(red_component) >0:
      for r, c in red_component:
          output_grid[r - min_row, c - min_col] = 2
    if len(blue_component) > 0:
      for r, c in blue_component:
          output_grid[r - min_row, c - min_col] = 1

    # 5. Determine Yellow Pixel Placement
    corners = get_corners(input_grid)
    out_corners = get_corners(output_grid) if (output_rows > 0 and output_cols > 0) else []

    yellow_corners = []
    for yr, yc in yellow_pixels:
        if (yr, yc) in corners:
            yellow_corners.append((yr, yc))

    max_red_row = 0
    if len(red_pixels) > 0:
        max_red_row = np.max(red_component[:, 0])

    for yr, yc in yellow_pixels:
        if yr > max_red_row:  # Check below
            yellow_corners.append((yr, yc))

    if len(yellow_corners) >= 2 and len(out_corners) > 0:
        for i in range(min(len(yellow_corners), len(out_corners))):
            in_r, in_c = yellow_corners[i]
            #check which corner and scale to output
            if in_r == corners[0][0] and in_c == corners[0][1]: #top left
                if len(out_corners) > 0: output_grid[out_corners[0]] = 4
            if in_r == corners[1][0] and in_c == corners[1][1]:#top right
                if len(out_corners) > 1: output_grid[out_corners[1]] = 4
            if in_r == corners[2][0] and in_c == corners[2][1]:#bottom left - not in output
                if len(out_corners) > 2: output_grid[out_corners[2]] = 0
            if in_r == corners[3][0] and in_c == corners[3][1]:#bottom right
                if len(out_corners) > 3: output_grid[out_corners[3]] = 4

    return output_grid
```
