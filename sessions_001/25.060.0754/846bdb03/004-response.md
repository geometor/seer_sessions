# 846bdb03 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation extracts the connected red, the adjacent blue, and the specific yellow pixels from the input grid, maintaining their relative positions (though scaled down), and discards everything else. It then reconstructs a smaller grid based on these extracted elements. The program focuses on specific color clusters and their spatial relationship within the structure.
"""

import numpy as np

def find_object(grid, color):
    """Finds coordinates of pixels of a specific color."""
    coords = np.argwhere(grid == color)
    return coords

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
    # initialize output_grid
    output_grid = np.zeros((6, 8), dtype=int)
    
    # 1. Identify Key Structures
    red_pixels = find_object(input_grid, 2)
    blue_pixels = find_object(input_grid, 1)
    yellow_pixels = find_object(input_grid, 4)

    #2 & 3. extract connected components
    if len(red_pixels) > 0:
      red_component = extract_connected_component(input_grid, red_pixels[0], 2)
      #normalize and add to output
      min_red_row = np.min(red_component[:, 0])
      min_red_col = np.min(red_component[:, 1])
      for r, c in red_component:
          output_grid[r - min_red_row, c - min_red_col] = 2
    
    if len(blue_pixels) > 0:
      #find blue pixel adjacent to red
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
        min_blue_row = np.min(red_component[:, 0]) #use red component min
        min_blue_col = np.min(red_component[:, 1])
        for r, c in blue_component:
          output_grid[r - min_blue_row, c-min_blue_col] = 1

    # 4. Extract Yellow Corners
    corners = get_corners(input_grid)

    yellow_corners = []
    for yr, yc in yellow_pixels:
        if (yr,yc) in corners:
            yellow_corners.append((yr,yc))
    
    out_corners = get_corners(output_grid)

    #find yellow at bottom of red structure
    max_red_row = 0
    if len(red_pixels) > 0:
      max_red_row = np.max(red_component[:,0])
    for yr, yc in yellow_pixels:
      if yr > max_red_row: #check below
        yellow_corners.append((yr,yc))

    if len(yellow_corners) >=2 :
      for i in range(min(len(yellow_corners),len(out_corners))):
        in_r, in_c = yellow_corners[i]
        out_r, out_c = out_corners[i]

        #check which corner and scale to output
        if in_r == corners[0][0] and in_c == corners[0][1]: #top left
            output_grid[out_corners[0]] = 4
        if in_r == corners[1][0] and in_c == corners[1][1]:#top right
            output_grid[out_corners[1]] = 4

        if in_r == corners[2][0] and in_c == corners[2][1]:#bottom left - not in output
            output_grid[out_corners[2]] = 0
        if in_r == corners[3][0] and in_c == corners[3][1]:#bottom right
            output_grid[out_corners[3]] = 4


    return output_grid
```
