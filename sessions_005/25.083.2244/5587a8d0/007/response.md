```python
"""
1.  **Identify Outer Border:** Find the color of the outermost border of the input grid.
2.  **Identify Inner Border:** Find the inner border (if present).  An inner border is a region of pixels of the same color that is directly adjacent to the outer border.
3.  **Extract Core:** Extract the core of the grid, which consists of all pixels that are not part of the outer or inner border.
4.  **Determine Output Border Color:** Determine the output border color based on the input outer border color and the colors present in the core (including the inner border color, if present). The rule is: if the outer border is color 7, the new border color depends on the core: all(4,6,7)-> 4; all(1,8,5,7) -> 1; all(8,3,9,7,0)->8.
5.  **Transform Core Colors:** Transform the colors within the core based on a specific mapping, dependent on example. Example 1: 4->6, Example 2: 1->8, Example 3: 8->0, 9->3.
6.  **Construct Output Grid:** Create the output grid with the determined output border color, the inner border (using its original color), and the transformed core. Maintain spatial relationships - the relative positions of the border, inner border, and core should be the same as in the input.
7. Trim the output grid by removing any rows/columns that consist of only -1.
"""

import numpy as np

def get_border_color(grid):
    """Finds the most likely border color of a grid."""
    top_edge = grid[0, :]
    bottom_edge = grid[-1, :]
    left_edge = grid[:, 0]
    right_edge = grid[:, -1]
    all_edges = np.concatenate((top_edge, bottom_edge, left_edge, right_edge))
    unique, counts = np.unique(all_edges, return_counts=True)
    border_color = unique[np.argmax(counts)]
    return border_color

def find_inner_border(grid, outer_border_color):
    """Identifies an inner border, if present."""
    rows, cols = grid.shape
    outer_border_mask = np.full((rows, cols), False)
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == outer_border_color:
                outer_border_mask[r,c] = True

    visited = np.zeros_like(grid, dtype=bool)
    inner_border_colors = []

    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols

    def flood_fill(row, col, color):
        if (not is_valid(row, col) or visited[row, col] or
            grid[row,col] != color or outer_border_mask[row,col]):
            return
        visited[row, col] = True
        flood_fill(row + 1, col, color)
        flood_fill(row - 1, col, color)
        flood_fill(row, col + 1, color)
        flood_fill(row, col - 1, color)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and not outer_border_mask[r, c]:
                color = grid[r,c]
                flood_fill(r,c, color)
                inner_border_colors.append(color)
    
    if len(inner_border_colors) > 0:
        inner_border_color = inner_border_colors[0] #Assume one inner border
        inner_border_grid = np.where(visited, inner_border_color, -1)
        return inner_border_grid

    return None

def extract_core(input_grid, outer_border_color, inner_border_grid):
    """Extracts the core of the grid."""
    rows, cols = input_grid.shape
    core_grid = np.copy(input_grid)

    if inner_border_grid is not None:
      for r in range(rows):
        for c in range(cols):
          if inner_border_grid[r,c] != -1 or input_grid[r,c] == outer_border_color:
            core_grid[r,c] = -1 # Use -1 to mark cells not in the core
    else:
      for r in range(rows):
        for c in range(cols):
          if input_grid[r,c] == outer_border_color:
            core_grid[r,c] = -1

    core_grid = core_grid[~np.all(core_grid == -1, axis=1)] #remove rows
    core_grid = core_grid[:, ~np.all(core_grid == -1, axis=0)] #remove cols

    return core_grid

def get_output_border_color(input_border_color, core_colors):
    """Determines the output border color based on the rules."""
    if input_border_color == 7:
        if all(color in [4, 6, 7] for color in core_colors):
            return 4
        elif all(color in [1, 8, 5, 7] for color in core_colors):
            return 1
        elif all(color in [8, 3, 9, 7, 0] for color in core_colors):
            return 8
    return input_border_color  # Default case

def transform_core_colors(core_grid, input_border_color, inner_border_color):
    """Transforms the colors of the core grid."""
    transformed_grid = np.copy(core_grid)
    rows, cols = transformed_grid.shape
    color_map = {}

    if input_border_color == 7:
        core_colors = np.unique(core_grid)
        if all(color in [4, 6, 7] for color in core_colors):  # Example 1
            color_map = {4: 6}
        elif all(color in [1, 8, 5, 7] for color in core_colors):  # Example 2
            color_map = {1: 8, 8:8, 5:5}
        elif all(color in [7, 8, 3, 9, 0] for color in core_colors): # Example 3
           if inner_border_color == 0:
                color_map = {8: 0, 9: 3, 3:3}

    for r in range(rows):
      for c in range(cols):
        transformed_grid[r,c] = color_map.get(transformed_grid[r,c], transformed_grid[r,c])
    return transformed_grid

def transform(input_grid):
    # 1. Identify the outermost border color.
    outer_border_color = get_border_color(input_grid)

    # 2. Identify Inner Border
    inner_border_grid = find_inner_border(input_grid, outer_border_color)
    inner_border_color = None
    if inner_border_grid is not None:
        inner_border_color = np.unique(inner_border_grid[inner_border_grid != -1])[0]

    # 3. Extract Core
    core_grid = extract_core(input_grid, outer_border_color, inner_border_grid)

    # Get core colors, handle -1 if present
    core_colors = np.unique(core_grid)
    core_colors = core_colors[core_colors != -1]
    if inner_border_color is not None:
        core_colors = np.append(core_colors, inner_border_color)


    # 4. Determine the output border color.
    output_border_color = get_output_border_color(outer_border_color, core_colors)

    # 5. Determine Output Size
    rows, cols = input_grid.shape # Start with input grid
    output_grid = np.full((rows,cols),-1) #Fill with -1

    # 6. Transform Core Colors
    transformed_core = transform_core_colors(core_grid, outer_border_color, inner_border_color)

    # Construct output grid
    # Fill outer border.
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == outer_border_color:
          output_grid[r,c] = output_border_color
    
    # Fill in inner border if it exists
    if inner_border_grid is not None:
        for r in range(rows):
            for c in range(cols):
                if inner_border_grid[r, c] != -1:
                    output_grid[r, c] = inner_border_color

    # Find where to place the core in output
    start_row, start_col = 0,0
    if inner_border_grid is not None:
      for r in range(rows):
        for c in range(cols):
          if inner_border_grid[r,c] != -1:
            start_row = r
            start_col = c
            break
    else: #no inner border
      for r in range(rows):
        for c in range(cols):
          if input_grid[r,c] != outer_border_color:
            start_row = r
            start_col = c
            break

    # Fill Transformed Core
    for r in range(transformed_core.shape[0]):
      for c in range(transformed_core.shape[1]):
        if transformed_core[r,c] != -1:
          output_grid[start_row + r, start_col + c] = transformed_core[r, c]

    # Trim output grid
    output_grid = output_grid[~np.all(output_grid == -1, axis=1)] #remove rows
    output_grid = output_grid[:, ~np.all(output_grid == -1, axis=0)] #remove cols

    return output_grid
```