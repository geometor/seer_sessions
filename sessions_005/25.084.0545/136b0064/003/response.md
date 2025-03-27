```python
"""
The transformation identifies vertical stripes of different colors in the input grid, filters out yellow stripes and single-pixel stripes, and then rearranges and resizes these stripes into a new output grid. The output grid has a fixed width of 7, and a variable height. The order and placement of stripes in the output grid are determined by their color and, in some cases, their original position in the input.
"""

import numpy as np

def get_non_yellow_stripes(grid):
    """
    Identifies and returns non-yellow and non-single-black colored vertical stripes.
    """
    stripes = []
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)

    for x in range(width):
        for y in range(height):
            if not visited[y, x] and grid[y, x] != 0 and grid[y,x] != 4:
                color = grid[y, x]
                stripe = []
                
                # Check for adjacent cells, skip if adjacent to a yellow
                # Assume it must be vertical stripe
                yy = y
                valid = True
                while yy < height and grid[yy, x] == color:
                    if x > 0 and grid[yy, x-1] == 4:
                        valid = False
                        break

                    if x < width-1 and grid[yy, x+1] == 4:
                        valid = False
                        break
                    
                    stripe.append((yy, x))
                    visited[yy, x] = True
                    yy += 1
                
                if valid and len(stripe) > 1:
                    # double check that this isn't part of a yellow adjacent stripe
                    okay = True
                    for yy, xx in stripe:
                        if xx > 1 and grid[yy, xx-2] == 4:
                            okay = False
                        if xx < width - 2 and grid[yy, xx+2] == 4:
                            okay = False
                    if okay:
                        stripes.append((color, stripe))
    return stripes

def find_adjacent_stripes(stripes, color):
    """Finds adjacent stripes of the specified color."""
    adjacent_groups = []
    current_group = []

    # Sort stripes by starting x coordinate
    color_stripes = sorted([s for c, s in stripes if c == color], key=lambda s: s[0][1])


    for stripe in color_stripes:
        x = stripe[0][1]
        if not current_group:
            current_group.append((x, stripe))
        else:
            last_x, _ = current_group[-1]
            if x == last_x + 1:  # Adjacent
                current_group.append((x, stripe))
            else:
                 # Check for adjacent with space
                if len(current_group) > 0:
                    adjacent_groups.append(current_group)
                    current_group = []
                current_group.append((x, stripe))
    if len(current_group) > 0:
        adjacent_groups.append(current_group)
    
    return adjacent_groups

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    input_grid = np.array(input_grid)
    stripes = get_non_yellow_stripes(input_grid)

    # Determine output grid size.
    output_width = 7
    output_height = input_grid.shape[0] # use input height
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Determine stripe order.  Create a mapping
    stripe_order = {
      5: 0, # Gray
      2: 1, # Red
      1: 2, # Blue
      6: 3,  # Magenta
      3: 4, # Green
    }

    # Place the transformed stripes.
    
    # Gray
    gray_stripes = [s for c, s in stripes if c == 5]
    if gray_stripes:
       output_grid[0, stripe_order[5]] = 5

    # Red
    red_stripes = [s for c, s in stripes if c == 2]
    red_col = stripe_order[2]
    if len(red_stripes) > 0:
        output_grid[1:3, red_col] = 2

    # Blue
    blue_groups = find_adjacent_stripes(stripes, 1)
    blue_col = stripe_order[1]
    for group in blue_groups:
      if len(group) >= 2: # two adjacent blue stripes
        output_grid[2:4, blue_col:blue_col+3] = np.array([[1,1,1],[0,1,1]])
        blue_col += 4
      elif len(group) > 0:
        output_grid[1, blue_col:blue_col+3] = 1 # horizontal 3
        blue_col += 3
    
    # Magenta
    magenta_col = stripe_order[6]
    magenta_stripes = [s for c, s in stripes if c == 6]

    if len(magenta_stripes) > 1:
      output_grid[4:6, magenta_col] = 6
      output_grid[5:7, magenta_col+1] = 6 # second stripe
    else:
        for color, stripe in magenta_stripes:
            for i in range(min(2, len(stripe))):
                output_grid[4+i, magenta_col] = 6

    # Green
    green_col = stripe_order[3]
    green_stripes = [s for c, s in stripes if c == 3]

    
    for i, (color, stripe) in enumerate(green_stripes):
        for j in range(min(4, len(stripe))):
            output_grid[8, green_col ] = 3

    return output_grid
```