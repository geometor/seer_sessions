# 29623171 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Horizontal Boundaries:** Locate the horizontal lines of grey (5) pixels that span the entire width of the grid. These lines act as delimiters.
2.  **Isolate Colored Regions:** Within each section bounded by the grey lines (or the edge of the grid), identify any connected regions of non-white (0) and non-grey(5) colors.
3. **Identify replication zone:** Locate the zone at the bottom, beneath the last horizontal grey(5) line.
4.  **Replicate Colored Regions:** For each identified colored region above the last horizontal grey line, check if the region to be replicated is composed by 1 or more pixels.
    * if the colored region is one single pixel replicate a 3x1 region of the same color in the replication zone.
    * if the original region is already 3x1, create a copy.
    Maintain the horizontal order of the replicated colored pixels in the last section. The vertical order within the section does not matter as long as the copied sections are contiguous.
"""

import numpy as np

def find_horizontal_lines(grid, color=5):
    """Finds rows that are entirely a single color."""
    lines = []
    for i, row in enumerate(grid):
        if np.all(row == color):
            lines.append(i)
    return lines

def find_colored_regions(grid, horizontal_lines):
    """Identifies colored regions between horizontal lines."""
    regions = []
    # Add grid boundaries to list
    boundaries = sorted([0, grid.shape[0]] + horizontal_lines)

    for i in range(len(boundaries) - 1):
        start_row = boundaries[i]
        end_row = boundaries[i+1]
        section = grid[start_row:end_row, :]

        for x in range(0,grid.shape[1]):
            for y in range(start_row,end_row):
                color = grid[y,x]
                if color != 0 and color != 5:
                  regions.append( ((y,x) , color) )

    return regions
    
def transform(input_grid):
    """Transforms the input grid according to the replication rule."""
    grid = np.array(input_grid)  # Convert to NumPy array
    horizontal_lines = find_horizontal_lines(grid)
    colored_regions = find_colored_regions(grid, horizontal_lines)
    
    last_grey_line_index = -1
    
    if len(horizontal_lines)>0:
        last_grey_line_index = horizontal_lines[-1]
    
    #find the zone to start to replicate.
    replication_zone_start_y = last_grey_line_index + 1
    current_x = 0;
    #order the pixels for x position.
    colored_regions.sort(key=lambda x: x[0][1])

    # Replicate colored regions
    for region in colored_regions:
      pos, color = region
      #check if the region to replicate is above the replication zone.
      if pos[0] < replication_zone_start_y :
        
        #replicate the color in the replication zone.
        #Check bounds
        if replication_zone_start_y<grid.shape[0] and current_x+2<grid.shape[1]:
          grid[replication_zone_start_y, current_x:current_x+3] = color
        current_x = current_x+3

    return grid.tolist()
```
