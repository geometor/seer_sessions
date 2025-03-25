"""
Transforms an input grid by modifying specific subgrids and isolated pixels.
Subgrids are rectangular regions of a single non-zero color. Isolated pixels
are non-zero pixels surrounded by zeros. Subgrids are filled with a new color
based on neighboring colors of the edges, and isolated pixels are changed
based on the most prevalent color in their Moore neighborhood.
"""

import numpy as np
from collections import Counter

def find_subgrids(grid):
    """Finds all maximal rectangular subgrids of a single non-zero color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    subgrids = []

    def is_valid(r, c, color):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and not visited[r, c]

    def expand_subgrid(r, c, color):
        """Expands a subgrid from a starting cell."""
        min_r, max_r = r, r
        min_c, max_c = c, c

        # Expand vertically
        while min_r > 0 and is_valid(min_r - 1, c, color):
            min_r -= 1
        while max_r < rows - 1 and is_valid(max_r + 1, c, color):
            max_r += 1

        # Expand horizontally
        for row in range(min_r, max_r + 1):
            while min_c > 0 and is_valid(row, min_c - 1, color):
                min_c -= 1
            while max_c < cols - 1 and is_valid(row, max_c + 1, color):
                max_c += 1
        
        pixels = []
        for row in range(min_r, max_r+1):
            for col in range(min_c, max_c + 1):
                visited[row,col] = True
                pixels.append( ((row,col), grid[row,col]) )

        return {'top_left': (min_r, min_c), 'bottom_right': (max_r, max_c),
                'height': max_r - min_r + 1, 'width': max_c - min_c + 1,
                'color': color, 'pixels': pixels}

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                subgrids.append(expand_subgrid(r, c, grid[r, c]))
    return subgrids

def find_isolated_pixels(grid):
    """Finds isolated non-zero pixels surrounded by zeros."""
    rows, cols = grid.shape
    isolated_pixels = []

    def is_isolated(r, c):
        if grid[r,c] == 0:
            return False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (dr, dc) == (0, 0):
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if nr == r or nc == c:  # Check immediate neighbors only
                        if grid[nr, nc] != 0:
                            return False
        return True

    for r in range(rows):
        for c in range(cols):
            if is_isolated(r, c):
                isolated_pixels.append( {'position':(r,c), 'color':grid[r,c]} )
    return isolated_pixels

def get_moore_neighborhood(grid, r, c):
    """Gets the Moore neighborhood (8-neighbors) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr, dc) == (0, 0):
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(grid[nr, nc])
    return neighbors

def process_subgrid(grid, subgrid):
    """
    Process one subgrid, changing values inside it based on the neighbors.
    """

    pixels = subgrid['pixels']
    top_left = subgrid['top_left']
    bottom_right = subgrid['bottom_right']

    for (r,c), color in pixels:
      
        neighbors = []
        for dr in [-1,1]:
            nr, nc = (r+dr, c)
            if not (top_left[0] <= nr <= bottom_right[0] and top_left[1] <= nc <= bottom_right[1] ):
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    neighbors.append( grid[nr, nc] )
        for dc in [-1,1]:
            nr, nc = (r, c+dc)
            if not (top_left[0] <= nr <= bottom_right[0] and top_left[1] <= nc <= bottom_right[1] ):
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    neighbors.append( grid[nr, nc] )

        if len(neighbors) > 0:
            counts = Counter(neighbors)
            most_common_color = counts.most_common(1)[0][0]

            cross_neighbors = []
            for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = (r+dr, c+dc)
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    cross_neighbors.append(grid[nr,nc])
            cross_counts = Counter(cross_neighbors)
            
            if len(cross_counts) > 1 and grid[r,c] != most_common_color: # and grid[r,c] != cross_counts.most_common(1)[0][0]:
                grid[r,c] = most_common_color
    return grid

def process_isolated_pixel(grid, isolated_pixel):
  r,c = isolated_pixel['position']
  neighbors = get_moore_neighborhood(grid, r, c)
  if len(neighbors)>0:
      counts = Counter(neighbors)
      most_common_color = counts.most_common(1)[0][0]
      if most_common_color != 0:
          grid[r,c] = most_common_color
      
  return grid
    

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation

    # Find subgrids and isolated pixels
    subgrids = find_subgrids(grid)
    isolated_pixels = find_isolated_pixels(grid)

    # Process subgrids
    for subgrid in subgrids:
      grid = process_subgrid(grid, subgrid)

    # Process isolated pixels
    for isolated_pixel in isolated_pixels:
      grid = process_isolated_pixel(grid, isolated_pixel)
    
    return grid.tolist()  # Convert back to list