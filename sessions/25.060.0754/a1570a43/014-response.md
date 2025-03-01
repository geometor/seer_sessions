# a1570a43 • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:**
    *   Locate the contiguous block of red pixels (color 2).
    *   Locate all green pixels (color 3).

2.  **Analyze Red Object Shape:**
    *   Determine if the red block forms a horizontal line, a vertical line, or another shape.
    *   Calculate the center of the red block.

3.  **Analyze Green Object Positions:**
    *  Determine the number of green pixels.
    *  Check their positions relative to the red block (e.g. surrounding, below, etc.)

4.  **Transformation Rules:**

    *   **Rule 1 (Rotation):** If the red block is a horizontal line, and there is *at least* one green pixel directly above, and one green pixel directly below the center of the red line, then the red block rotates 90 degrees clockwise around its center.
    *   **Rule 2 (No Transformation):** If the red block is a vertical line and the green pixels form a horizontal line directly below *and are equal in length*, there is no transformation. The red block stays in place.
    *   **Rule 3 (Horizontal Translation):** If the red block is a vertical line, and the green pixels are in a line below the red block, and the green pixels extend at least one pixel beyond the width of the red block on either side, then the red block translates horizontally. The leftmost pixel of the translated red block aligns with the column of the original rightmost red pixel.
    *   **Rule 4 (Default - No Change):**  If none of the above conditions are met, the red object does not move.

5.  **Output:**
    *   Create a new grid, retaining all original green pixels.
    *  Apply the determined transformation (or no transformation) of the red block to the new grid.
"""

import numpy as np

def get_red_block(grid):
    # Find coordinates of all red pixels
    return np.argwhere(grid == 2)

def get_green_pixels(grid):
    # Find coordinates of all green pixels
    return np.argwhere(grid == 3)

def is_horizontal(coords):
    #check that all coordinates are on the same row
    return all([coords[0][0] == c[0] for c in coords])

def is_vertical(coords):
    #check that all coordinates are on the same column
    return all([coords[0][1] == c[1] for c in coords])

def calculate_center(coords):
    min_x = min(coords[:, 0])
    max_x = max(coords[:, 0])
    min_y = min(coords[:, 1])
    max_y = max(coords[:, 1])
    return np.array([(min_x + max_x) / 2.0, (min_y + max_y) / 2.0])

def rotate_90(coords, center):
    # Rotate coordinates 90 degrees clockwise around a center point
    centered_coords = coords - center
    rotated_coords = np.array([[-y, x] for x, y in centered_coords])
    return rotated_coords + center

def check_green_above_below(red_center, green_pixels):
    #check that green pixels are above and below the center
    above = False
    below = False
    for gx, gy in green_pixels:
        if gy == int(red_center[1]) and gx < int(red_center[0]):
            above = True
        if gy == int(red_center[1]) and gx > int(red_center[0]):
            below = True
    return above and below

def green_line_below(red_block, green_pixels):
    #check that green pixels are only below the red block

    #all green must be below red
    red_rows = set(red_block[:,0])
    green_rows = set(green_pixels[:,0])

    if(len(green_rows) > 0 and max(green_rows) <= min(red_rows)):
      return False

    #check that its a line
    if(len(green_rows) != 1):
        return False;

    return True

def is_green_line_extended(red_block, green_pixels):
    #return if green line extends beyond edges of the red block
    if(len(green_pixels) == 0):
        return False

    red_cols = sorted(red_block[:, 1])
    green_cols = sorted(green_pixels[:,1])

    return green_cols[0] < red_cols[0] and green_cols[-1] > red_cols[-1]
    

def transform(input_grid):
    # Initialize output grid with the original colors
    output_grid = np.copy(input_grid)

    # Get the red block and green pixels coordinates
    red_block = get_red_block(input_grid)
    green_pixels = get_green_pixels(input_grid)

    #if no red block return
    if(len(red_block) == 0):
        return output_grid

    #remove original red pixels
    output_grid[output_grid == 2] = 0

    # Rule 1: Horizontal Rotation
    if is_horizontal(red_block):
        red_center = calculate_center(red_block)
        if check_green_above_below(red_center, green_pixels):
            rotated_red_block = rotate_90(red_block, red_center)
            rotated_red_block = np.round(rotated_red_block).astype(int) #convert back
             #place back into array
            for x, y in rotated_red_block:
                if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
                    output_grid[x,y] = 2
            return output_grid

    # Rule 2 & 3: Vertical line (translation or no change)
    elif is_vertical(red_block):
        if green_line_below(red_block, green_pixels):
            if len(green_pixels) == len(red_block):  # Rule 2: No change
                #place original red block
                for x, y in red_block:
                    output_grid[x,y] = 2
                return output_grid
            elif is_green_line_extended(red_block, green_pixels):  #Rule 3 translate
                rightmost_col = max(red_block[:,1])
                translated_red_block = []
                for x,y in red_block:
                    new_y = rightmost_col
                    translated_red_block.append( (x,new_y) )

                for x, y in translated_red_block:
                    if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
                        output_grid[x,y]=2
                return output_grid

    # Rule 4: Default, no change
    for x, y in red_block:
        output_grid[x,y] = 2
    return output_grid
```
