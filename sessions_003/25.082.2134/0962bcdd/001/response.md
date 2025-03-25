```python
"""
Transforms the input grid by identifying 3-pixel objects, expanding the central pixel, 
mirroring and expanding the wing pixels, and applying color changes based on the 
original wing pixel color.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies 3-pixel objects in the grid.
    Returns a list of objects, where each object is a dictionary containing the
    central pixel coordinates and the wing pixel coordinates.
    """
    objects = []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj):
        visited[r, c] = True
        obj['pixels'].append((r, c))

        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if is_valid(nr, nc) and grid[nr, nc] != 0 and not visited[nr, nc]:
                dfs(nr, nc, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = {'pixels': []}
                dfs(r, c, obj)
                if len(obj['pixels']) == 3:
                    # Determine central pixel and wing pixels.
                    obj['pixels'].sort() # sorting helps to determine the central pixel by its location
                    obj['central'] = obj['pixels'][1]
                    obj['wings'] = [obj['pixels'][0], obj['pixels'][2]]
                    
                    objects.append(obj)

    return objects



def transform(input_grid):
    """
    Transforms the input grid according to the identified rules.
    """
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.zeros_like(input_grid)

    objects = get_objects(input_grid)
    
    for obj in objects:
      central_row, central_col = obj['central']
      central_color = input_grid[central_row, central_col]
      
      # central pixel expansion
      output_grid[central_row, max(0, central_col - 1)] = central_color
      output_grid[central_row, central_col] = central_color
      output_grid[central_row, min(output_grid.shape[1] - 1, central_col + 1)] = central_color
      
      for wing_row, wing_col in obj['wings']:
          wing_color = input_grid[wing_row, wing_col]
          
          # Determine the mirrored position based on offset from central pixel
          row_offset = wing_row - central_row
          col_offset = wing_col - central_col
          
          mirrored_row = central_row - row_offset
          mirrored_col = central_col - col_offset
          
          # Color changes
          if wing_color == 7:  # Orange
              mirrored_color = 2  # Red
          elif wing_color == 8:  # Azure
              mirrored_color = 6 # Magenta
          else:
              mirrored_color = wing_color

          # wing pixel mirroring + expansion
          if 0 <= mirrored_row < output_grid.shape[0] and 0 <= mirrored_col < output_grid.shape[1]:
            output_grid[mirrored_row, max(0, mirrored_col - 1)] = mirrored_color
            output_grid[mirrored_row, mirrored_col] = mirrored_color
            output_grid[mirrored_row, min(output_grid.shape[1] - 1, mirrored_col + 1)] = mirrored_color
          
          # handle the original wing pixel
          if wing_color == 7:  # Orange
                wing_color_transformed = 2  # Red
          elif wing_color == 8:  # Azure
                wing_color_transformed = 6 # Magenta
          else:
                 wing_color_transformed = wing_color
          
          output_grid[wing_row, max(0, wing_col - 1)] = wing_color_transformed
          output_grid[wing_row, wing_col] = wing_color_transformed
          output_grid[wing_row, min(output_grid.shape[1] - 1, wing_col + 1)] = wing_color_transformed


    return output_grid
```