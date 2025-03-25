"""
The transformation rule identifies regions of uniform size (3x3, 1x3, or 3x1) within the input grid. 
When a change is detected in pixels adjacent to these regions in the output grid, it swaps the colors 
between the changed pixel group and a uniform region of matching size and changed pixel's color elsewhere on grid.
The background color is maintained throughout.
"""

import numpy as np

def find_uniform_regions(grid):
    """Finds 3x3, 1x3, and 3x1 uniform regions in the grid."""
    rows, cols = grid.shape
    uniform_regions = []

    # Find 3x3 uniform regions
    for r in range(rows - 2):
        for c in range(cols - 2):
            region = grid[r:r+3, c:c+3]
            if np.all(region == region[0, 0]):
                uniform_regions.append(((r, c), (3, 3)))

    # Find 1x3 uniform regions
    for r in range(rows):
        for c in range(cols - 2):
            region = grid[r, c:c+3]
            if np.all(region == region[0]):
                uniform_regions.append(((r, c), (1, 3)))

    # Find 3x1 uniform regions
    for r in range(rows - 2):
        for c in range(cols):
            region = grid[r:r+3, c]
            if np.all(region == region[0]):
                uniform_regions.append(((r, c), (3, 1)))

    return uniform_regions

def find_changed_pixels(input_grid, output_grid):
    """Finds pixels that have changed between input and output grids."""
    return np.where(input_grid != output_grid)

def find_matching_region(grid, size, color):
    """Finds a uniform region of specified size and color."""
    rows, cols = grid.shape
    h, w = size
    for r in range(rows - h + 1):
        for c in range(cols - w + 1):
            region = grid[r:r+h, c:c+w]
            if np.all(region == color):
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    uniform_regions = find_uniform_regions(input_grid)
    changed_pixels = find_changed_pixels(input_grid, output_grid)
    changed_coords = list(zip(changed_pixels[0], changed_pixels[1]))
    processed = []

    for (r, c), (h, w) in uniform_regions:
        if h==3 and w==3:
            neighbors = []
            if c + 3 < cols:
               neighbors.extend([(r + i, c + 3) for i in range(3)])  # Right
            if r + 3 < rows:
               neighbors.extend([(r + 3, c + i) for i in range(3)]) # Bottom
            if r > 0:
               neighbors.extend([(r - 1, c + i) for i in range(3)])    # Top
            if c > 0:
                neighbors.extend([(r+i, c -1) for i in range(3)])   # Left
        elif h == 3 and w == 1:
             neighbors = []
             if c + 1 < cols:
                neighbors.append((r, c + 1)) #right
                neighbors.append((r+1, c + 1))
                neighbors.append((r+2, c + 1))

             if r > 0:
                neighbors.append((r - 1, c ))  # Top
             if r + 3 < rows:
                neighbors.append((r + 3, c))  # Bottom
             if c > 0:
                neighbors.append((r, c-1)) #left
                neighbors.append((r+1, c - 1))
                neighbors.append((r+2, c - 1))
        elif h == 1 and w == 3:
             neighbors = []
             if r + 1 < rows:
                neighbors.append((r+1, c))
                neighbors.append((r+1, c+1))
                neighbors.append((r+1, c+2))
             if c + 3 < cols:
                neighbors.append((r, c + 3))  # Right
             if r > 0:
                neighbors.append((r - 1, c)) # Top
                neighbors.append((r - 1, c+1))
                neighbors.append((r - 1, c+2))

             if c > 0:
                neighbors.append((r, c - 1))  # Left


        for nr, nc in neighbors:
             if (nr, nc) in changed_coords and (nr,nc) not in processed:
                changed_color = output_grid[nr, nc]
                original_color = input_grid[nr,nc]
                if h==3 and w==3:
                    changed_size = (1,1)
                    
                    
                else:
                    changed_size = (h,w)
                
                
                if h==1 and w ==3:
                  match_start = find_matching_region(output_grid, changed_size, changed_color)
                  if match_start is not None:
                    mr, mc = match_start
                    
                    output_grid[nr, nc] = original_color
                    
                    output_grid[mr:mr+1, mc:mc+3] = changed_color
                    processed.append((nr,nc))
                elif h==3 and w==1:
                  match_start = find_matching_region(output_grid, changed_size, changed_color)

                  if match_start is not None:
                      mr, mc = match_start
                      output_grid[nr, nc] = original_color
                      output_grid[mr:mr+3, mc:mc+1] = changed_color
                      processed.append((nr,nc))
                else:
                    
                  match_start = find_matching_region(output_grid, (1,1), changed_color)
                  if match_start is not None:
                      mr, mc = match_start
                      output_grid[mr, mc] = original_color
                      output_grid[nr, nc] = changed_color
                      processed.append((nr,nc))


    return output_grid