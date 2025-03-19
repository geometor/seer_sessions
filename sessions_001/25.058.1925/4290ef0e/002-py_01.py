"""
1.  **Identify Enclosed Regions:** Scan the input grid to identify all distinct, enclosed regions of color. A region is considered "enclosed" if it's completely surrounded by pixels of a single, different color.

2.  **Extract Representative Shape:** For each enclosed region/object detected get it's shape.

3.  **Reduce and Position:**
    *   Create smaller grid
    *   transfer relative position of the shapes

4.  **Output:** Present the resulting, smaller grid as the output.
"""

import numpy as np

def get_enclosed_objects(grid):
    """Identifies and returns distinct, enclosed objects within the grid."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                     (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
        for nr, nc in neighbors:
            dfs(nr, nc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                     objects.append((grid[r,c],current_object)) #add the color
    
    #check it is enclosed
    enclosed_objects = []
    for color, obj in objects:
      is_enclosed = True
      border_color = -1 #init
      for r,c in obj:
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                     (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]

        for nr, nc in neighbors:
          if is_valid(nr,nc):
            if grid[nr,nc] != color:
              if border_color == -1:
                border_color = grid[nr,nc]
              elif border_color != grid[nr,nc]:
                is_enclosed = False
                break
          else:
              is_enclosed = False
              break #object touches the edge

      if is_enclosed:
        enclosed_objects.append((color, obj, border_color))

    return enclosed_objects

def get_shape(obj):
    """Extracts a representative shape for the object (rectangle)."""
    min_r = min(p[0] for p in obj)
    max_r = max(p[0] for p in obj)
    min_c = min(p[1] for p in obj)
    max_c = max(p[1] for p in obj)
    return (min_r, min_c), (max_r, max_c)


def transform(input_grid):
    """Transforms the input grid to the output grid based on the defined rules."""
    grid = np.array(input_grid)
    
    # 1. Identify enclosed regions
    enclosed_objects = get_enclosed_objects(grid)
    
    # 2. & 3. Extract shapes and determine output grid size
    
    #calculate relative position and size
    centers = []
    enclosing_size = [] #min distance between shapes
    shapes = []

    for color, obj, border_color in enclosed_objects:
        (min_r, min_c), (max_r, max_c) = get_shape(obj)
        center_r = (min_r + max_r) // 2
        center_c = (min_c + max_c) // 2
        centers.append( (center_r, center_c))
        shapes.append( ((min_r,min_c),(max_r, max_c)))

    #calculate the scale
    min_r_dist = float('inf')
    min_c_dist = float('inf')

    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            r_dist = abs(centers[i][0] - centers[j][0])
            c_dist = abs(centers[i][1] - centers[j][1])

            #get shape dist
            s1 = shapes[i]
            s2 = shapes[j]
            r_dist_shape = 0
            c_dist_shape = 0

            if s1[1][0] < s2[0][0]: #s1 top is less than s2 bottom
              r_dist_shape = s2[0][0] - s1[1][0]
            elif s2[1][0] < s1[0][0]: #s2 top is less than s1 bottom
              r_dist_shape = s1[0][0] - s2[1][0]
            #else they overlap

            if s1[1][1] < s2[0][1]: #s1 left is less than s2 right
              c_dist_shape = s2[0][1] - s1[1][1]
            elif s2[1][1] < s1[0][1]: #s2 left is less than s1 right
              c_dist_shape = s1[0][1] - s2[1][1]           


            if r_dist_shape > 0 and r_dist_shape < min_r_dist:
              min_r_dist = r_dist_shape
            
            if c_dist_shape > 0 and c_dist_shape < min_c_dist:
              min_c_dist = c_dist_shape

    scale_r = min_r_dist
    scale_c = min_c_dist

    if min_r_dist == float('inf'):
      scale_r = max( (s[1][0] - s[0][0]) for s in shapes) + 1 #height
    if min_c_dist == float('inf'):
      scale_c = max( (s[1][1] - s[0][1]) for s in shapes) + 1 #width

    #determine output size
    input_rows, input_cols = grid.shape

    #calculate offset
    all_min_r = min( c[0] for c in centers)
    all_min_c = min( c[1] for c in centers)


    output_rows = (input_rows // scale_r) + 2
    output_cols = (input_cols // scale_c) + 2


    
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # 4. Create output grid and place representative shapes
    for color, obj, border_color in enclosed_objects:
      
        (min_r, min_c), (max_r, max_c) = get_shape(obj)

        center_r = (min_r + max_r) // 2
        center_c = (min_c + max_c) // 2

        out_min_r = (center_r-all_min_r) // scale_r
        out_min_c = (center_c-all_min_c) // scale_c

        # print(f"scale {scale_r} {scale_c} in:{input_rows}x{input_cols} out:{output_rows}x{output_cols} offset:{all_min_r} {all_min_c} center:{center_r} {center_c}  out:{out_min_r} {out_min_c}" )

        for r in range(max_r - min_r + 1):
            for c in range(max_c - min_c + 1):
                output_r = out_min_r + r
                output_c = out_min_c + c
                if 0 <= output_r < output_rows and 0 <= output_c < output_cols:
                   output_grid[output_r, output_c] = grid[min_r + r, min_c+c]


    return output_grid