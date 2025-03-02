"""
1.  **Identify Shapes:** Locate all closed shapes formed by contiguous blue (1) pixels on the input grid.
2.  **Determine Fill Color:**
    *   If the shape is the *upper* shape, the fill color is orange (7).
    *   If the shape is the *lower* shape, the fill color is red (2).
3.  **Fill Shapes:** For each identified shape, replace all interior white (0) pixels with the designated fill color determined in step 2.
4. **Preserve outlines:** Keep the original blue pixels unchanged.
"""

import numpy as np

def find_shapes(grid, outline_color):
    # Find all outline pixels
    outline_pixels = np.where(grid == outline_color)
    shapes = []
    visited = set()

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_shape):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != outline_color:
            return
        visited.add((x, y))
        current_shape.append((x, y))

        # Explore adjacent pixels
        dfs(x + 1, y, current_shape)
        dfs(x - 1, y, current_shape)
        dfs(x, y + 1, current_shape)
        dfs(x, y - 1, current_shape)


    for x, y in zip(*outline_pixels):
        if (x, y) not in visited:
            current_shape = []
            dfs(x, y, current_shape)
            shapes.append(current_shape)
    return shapes

def flood_fill(grid, x, y, fill_color, outline_color):
     # classic flood fill algorithm

    if not (0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]):
        return
    if grid[x, y] == outline_color or grid[x,y] == fill_color:
        return

    grid[x, y] = fill_color
    flood_fill(grid, x + 1, y, fill_color, outline_color)
    flood_fill(grid, x - 1, y, fill_color, outline_color)
    flood_fill(grid, x, y + 1, fill_color, outline_color)
    flood_fill(grid, x, y - 1, fill_color, outline_color)



def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find shapes outlined in blue (1)
    blue_shapes = find_shapes(input_grid, 1)

    # Sort shapes by their topmost y-coordinate to determine upper and lower shapes
    sorted_shapes = sorted(blue_shapes, key=lambda shape: min(y for x, y in shape))
    
    if len(sorted_shapes) >= 1:
      # fill top
      top_shape = sorted_shapes[0]
      min_x = min(x for x,y in top_shape)
      max_x = max(x for x,y in top_shape)
      min_y = min(y for x,y in top_shape)
      max_y = max(y for x,y in top_shape)
      for x in range(min_x + 1, max_x):
          for y in range(min_y+1, max_y):
              if output_grid[x,y] != 1:
                flood_fill(output_grid, x, y, 7, 1) #fill orange

    if len(sorted_shapes) >= 2:
        #fill bottom shape
        bottom_shape = sorted_shapes[1]
        min_x = min(x for x,y in bottom_shape)
        max_x = max(x for x,y in bottom_shape)
        min_y = min(y for x,y in bottom_shape)
        max_y = max(y for x,y in bottom_shape)

        for x in range(min_x + 1, max_x ):
            for y in range(min_y + 1, max_y):
                if output_grid[x,y] != 1:
                    flood_fill(output_grid, x, y, 2, 1) # fill red

    return output_grid