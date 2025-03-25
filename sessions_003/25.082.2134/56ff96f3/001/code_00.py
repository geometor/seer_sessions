"""
1.  **Identify Objects:** Find all pixels in the input grid that have a non-zero color (i.e., not white).
2.  **Horizontal Expansion/Replication:** For each identified pixel, replicate its color horizontally.
    *   If there are two pixels of the same color on different rows, replicate it to create a rectangle using those two pixels.
    *   If only one pixel of the color exits, extend to the end of that "object".

3.  **Output:** The output grid is the result of these replications, with all other pixels remaining 0 (white).
Essentially, single non-zero pixels in a row of an object are expanded, so that the row is fully occupied by the color. If more than one colored pixel of same color are present in separate rows, a filled rectangle is created using them.
"""

import numpy as np

def find_objects(grid):
    """Finds all non-zero pixels and groups them by color."""
    objects = {}
    for row_idx, row in enumerate(grid):
        for col_idx, pixel_color in enumerate(row):
            if pixel_color != 0:
                if pixel_color not in objects:
                    objects[pixel_color] = []
                objects[pixel_color].append((row_idx, col_idx))
    return objects

def expand_horizontally(grid, objects):
    """Expands/replicates pixels horizontally based on object locations."""
    output_grid = np.copy(grid)
    for color, positions in objects.items():
      # sort by row
      positions.sort()

      # collect rows
      rows = [r for r, _ in positions]
      min_row = min(rows)
      max_row = max(rows)

      # collect the object columns by looking at connected components on
      # adjacent rows
      # each component is an "object" and the min/max cols are collected
      # from that
      
      # first build adjacency list of row: [(col, adj_row)]
      row_adj = {}
      for r, c in positions:
        if r not in row_adj:
          row_adj[r] = []
        # check for adj
        for ar, ac in positions:
          if ar == r: continue
          if abs(ar - r) == 1 and abs(ac - c) <= 1:
            row_adj[r].append( (c, ar) )

      # now traverse row_adj to build components
      components = []
      
      visited = set()
      
      def visit(r,c, component):
        visited.add((r,c))
        component.append((r,c))
        
        for ac, ar in row_adj.get(r, []):
          if abs(ac - c) <= 1 and (ar, ac) not in visited:
              visit(ar,ac, component)
              
      for r, c in positions:
        if (r,c) not in visited:
            component = []
            visit(r,c, component)
            components.append(component)

      # extract min and max cols
      for component in components:
        cols = [c for _, c in component]          
        min_col = min(cols)
        max_col = max(cols)

        component_rows = [r for r,_ in component]
        min_comp_row = min(component_rows)
        max_comp_row = max(component_rows)

        for r in range(min_comp_row, max_comp_row + 1):
          for c in range(min_col, max_col + 1):
                output_grid[r, c] = color
                
    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the expansion rule."""
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # initialize output grid
    output_grid = np.copy(input_grid)

    # Find objects (non-zero pixels grouped by color)
    objects = find_objects(input_grid)
   
    # expand objects horizontally
    output_grid = expand_horizontally(input_grid, objects)

    return output_grid.tolist()