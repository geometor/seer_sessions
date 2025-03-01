# e6721834 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Divide the input grid into two primary regions based on the background color (azure and white, respectively, top and bottom).
2.  **Isolate Foreground:** Within each region, identify all non-background colored pixels (the "foreground").
3. **Move Foreground Up**: Within the first region the non-azure pixels are moved to the top rows starting with the non zero and are placed starting from the right hand side of the azure background, maintaining their relative horizontal positions.
4. **Move Foregound Up.** Within the second region the non-white pixels are moved to the top rows starting with the non zero and are placed starting from the left hand side of the white background, maintaining their relative horizontal positions.
5.  **Create Output:** The output grid consists of the moved foreground pixels on the 0-background.
"""

import numpy as np

def get_regions(grid):
    """Divides the grid into regions based on background color changes."""
    # in this case we can look for the row with all 0's
    
    height = len(grid)
    width = len(grid[0])
    
    empty_row = -1
    for i in range(height):
      is_empty = True
      for j in range(width):
        if grid[i][j] != 0:
          is_empty = False
          break
      if is_empty:
        empty_row = i
        break

    if empty_row == -1:
        return [grid] # no split
    else:
      region1 = grid[:empty_row]
      region2 = grid[empty_row:]
      return region1, region2

def move_foreground(region, direction="left"):
    """Moves non-background pixels to the top, maintaining relative order."""
    rows, cols = region.shape
    background_color = region[0,0] # get background
    if background_color==0:
        background_color = region[-1,-1] # or last
    foreground_pixels = []
    
    # get list of just the pixels that are not the background
    for r in range(rows):
        for c in range(cols):
            if region[r, c] != background_color:
                foreground_pixels.append((region[r, c], c))

    # create a blank region to hold the shifted pixels
    new_region = np.zeros((rows, cols), dtype=int)

    # Sort by column to maintain horizontal order.  
    foreground_pixels.sort(key=lambda x: x[1])
    if direction == "right":
        foreground_pixels.reverse()

    # put them back in, but shifted up
    pixel_index = 0
    
    target_row=0
    if direction == "right":
        target_col = cols-1
    else:
        target_col=0
            
    while pixel_index < len(foreground_pixels):
      color, original_col = foreground_pixels[pixel_index]
      
      new_region[target_row, target_col] = color
      pixel_index+=1
      
      if direction == "right":
          target_col -= 1
          if target_col<0:
            target_col = cols-1
            target_row+=1
      else:
        target_col += 1
        if target_col>=cols:
            target_col=0
            target_row+=1          
    return new_region

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Divide the grid into regions
    regions = get_regions(input_grid)
    
    # process per region
    start_row = 0
    if len(regions)==2:

        region1, region2 = regions

        # Move foreground up within each region.
        new_region1 = move_foreground(region1, direction="right")
        new_region2 = move_foreground(region2, direction="left")

        # put back into output grid in correct spot
        output_grid[:new_region1.shape[0], :new_region1.shape[1]] = new_region1
        output_grid[new_region1.shape[0]:, :new_region2.shape[1]] = new_region2

    else: # only one region
        region = regions[0]
        new_region = move_foreground(region)
        output_grid[:new_region.shape[0], :new_region.shape[1]] = new_region

    return output_grid.tolist()
```
