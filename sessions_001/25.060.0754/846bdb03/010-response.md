# 846bdb03 • 010 • example_2 • investigate_coder

---
```python
"""
Transforms the input grid by cropping, selecting, and rearranging objects of color 3 (green), 8 (azure), and 4 (yellow).
The output grid's boundaries are determined by the positions of the yellow objects. The green object is moved to the right,
the azure object to the left, and the yellow objects remain in the top-left and bottom-left corners.
"""

import numpy as np

def find_objects(grid, colors):
    objects = {}
    for color in colors:
        objects[color] = []
        visited = np.zeros_like(grid, dtype=bool)
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color and not visited[r, c]:
                    object_coords = []
                    stack = [(r, c)]
                    while stack:
                        cr, cc = stack.pop()
                        if 0 <= cr < rows and 0 <= cc < cols and grid[cr, cc] == color and not visited[cr, cc]:
                            visited[cr, cc] = True
                            object_coords.append((cr, cc))
                            stack.extend([(cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)])
                    objects[color].append(object_coords)
    return objects

def get_yellow_boundary(objects):
     yellow_coords = objects.get(4, [])
     if len (yellow_coords) < 2:
         return (0,0), (0,0)

     min_row = min(coord[0] for obj in yellow_coords for coord in obj)
     max_row = max(coord[0] for obj in yellow_coords for coord in obj)

     min_col = min(coord[1] for obj in yellow_coords for coord in obj)
     
     first = None
     second = None
     for obj in yellow_coords:
         for r,c in obj:
             if first is None:
                first = (r,c)
             elif c < first[1]:
                 second = first
                 first = (r,c)
             elif second is None:
                 second = (r,c)
             elif c < second[1]:
                 second = (r,c)

     if first[0] > second[0]:
        first, second = second, first
     
     return first, second

def transform(input_grid):
    # Find objects of interest (colors 3, 8, and 4)
    objects = find_objects(input_grid, [3, 8, 4])

    # Determine output grid boundaries based on yellow objects
    yellow_top, yellow_bottom = get_yellow_boundary(objects)

    min_col = yellow_top[1]
    max_col = min_col + 7
    
    
    min_row = yellow_top[0] # objects[4][0][0][0]
    max_row = yellow_bottom[0]

    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)


    # place yellow pixels
    output_grid[0,0] = 4
    output_grid[-1,0] = 4

    # Reposition and resize green object (3) - brute force fitting
    green_objects = objects.get(3, [])
    green_row_offset = min_row
    green_col_offset = max_col - input_grid.shape[1] + min_col
    
    for obj in green_objects:
      for r,c in obj:
        out_r = r - green_row_offset
        out_c = c + green_col_offset
        if 0 <= out_r < output_height and 0 <= out_c < output_width:
            output_grid[out_r,out_c] = 3


    # Reposition and resize azure pixels (8) - brute force fit
    azure_objects = objects.get(8,[])
    azure_col_offset = min_col
    azure_row_offset = min_row
    
    for obj in azure_objects:
      for r,c in obj:
        out_r = r - azure_row_offset
        out_c = c - azure_col_offset
        
        if 0 <= out_r < output_height and 0 <= out_c < output_width:
          output_grid[out_r,out_c] = 8


    return output_grid
```
