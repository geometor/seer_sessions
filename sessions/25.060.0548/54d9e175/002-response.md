# 54d9e175 • 002 • example_4 • investigate_coder

---
```python
"""
This program transforms an input grid by identifying separator rows (all '5's), 
then infilling '0' (white) pixels in regions above and below the separators based on 
the positions of non-zero colored pixels within each region. The colored pixels 
themselves are also replaced with new color values.
"""

import numpy as np

def find_separators(grid):
    # Find rows that are all '5's
    separator_rows = []
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            separator_rows.append(i)
    return separator_rows

def get_colored_pixel_positions(region):
    # Find positions of non-zero pixels in a region.
    positions = []
    for i, pixel in enumerate(region):
        if pixel != 0:
            positions.append(i)
    return positions
    
def get_color_mapping():
    return {1:6, 2:7, 3:8, 4:9}

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find separator rows
    separator_rows = find_separators(output_grid)

    # Define regions based on separators
    regions_bounds = [] # (start_row, end_row)
    if not separator_rows: # handles the case where no separator
      regions_bounds.append((0,rows-1))
    else:
      regions_bounds.append((0, separator_rows[0] -1 )) # region above top separator

    # regions between
    for i in range(len(separator_rows)-1):
          regions_bounds.append((separator_rows[i]+1, separator_rows[i+1]-1))

    # region after separators
    if separator_rows:
      regions_bounds.append((separator_rows[-1]+1, rows -1))


    color_map = get_color_mapping()
    
    # Process each region
    for start_row, end_row in regions_bounds:
        # Get positions of non-zero pixels in the current region
        colored_pixel_positions = get_colored_pixel_positions(input_grid[start_row])
        #Infill the region
        for r in range(start_row, end_row + 1):

            #get colored pixels on this row
            colored_pixel_positions = get_colored_pixel_positions(input_grid[r])

            for c in range(cols):
                #skip separator columns - should never happen, but good practice
                if all(output_grid[:,c] == 5):
                    continue
                
                current_pixel = input_grid[r,c]
                
                if current_pixel == 0:
                    # Determine fill color based on position relative to colored pixels.
                    if c < colored_pixel_positions[0] if colored_pixel_positions else False:
                       output_grid[r,c] = color_map.get(1,0) # default of 0, but should find the right map
                    elif colored_pixel_positions and c > colored_pixel_positions[-1]:
                       output_grid[r,c] = color_map.get(4,0)
                    elif len(colored_pixel_positions) >= 2:
                        filled = False
                        for i in range(len(colored_pixel_positions) - 1):
                            if colored_pixel_positions[i] < c < colored_pixel_positions[i+1]:
                                output_grid[r, c] = color_map.get(3,0)
                                filled = True
                                break
                        if not filled:
                           if len(separator_rows) > 0:
                             if r < separator_rows[0]:
                               output_grid[r,c] = color_map.get(2,0)
                           else:
                             output_grid[r,c] = color_map.get(2,0)
                    elif len(colored_pixel_positions) > 0:  # catch all for adjacent
                        output_grid[r,c] = color_map.get(2,0)

                elif current_pixel in color_map:
                    output_grid[r,c] = color_map[current_pixel] # update the color
                

    return output_grid
```
