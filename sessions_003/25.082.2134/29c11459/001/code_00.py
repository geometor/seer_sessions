"""
1.  **Identify Non-Zero Pixels:** Locate all pixels in the input grid that have a value other than 0.
2.  **Horizontal Expansion:** For each non-zero pixel, expand it horizontally to the left and to the right. Specifically:
    * Copy input pixel value to 4 spaces to the left.
    * Copy input pixel value to four spaces to the right
3. **Insert Grey Separator** put a gray (5) pixel between expanded groups.
4. **Background Preservation:** All other pixels (where the input is 0) remain 0 in the output.
"""

import numpy as np

def get_non_zero_pixels(grid):
    """Finds the coordinates of non-zero pixels in the grid."""
    coords = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
              coords.append((r,c))
    return coords
def transform(input_grid):
    """Transforms the input grid according to the expansion rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    non_zero_coords = get_non_zero_pixels(input_grid)

    # keep track of the insertion point, starting after expanding the
    # first object to the beginning of the row.
    insert_col = 0
    
    for r, c in non_zero_coords:
        # Get the color of the current non-zero pixel
        color = input_grid[r, c]

        # Expand left
        left_bound = max(0, insert_col)
        for i in range(left_bound, c+1):
            output_grid[r, i] = color

        # expand right from the original location
        right_bound = min(input_grid.shape[1], c + 5)

        # loop to insert the expanded pixels, stopping before the limit
        for i in range(c+1, right_bound):
            output_grid[r, i] = color
            
        # insert a gray separator if this isn't the last element, and set
        # the insertion point for next object to be +1 from the end
        if c < input_grid.shape[1] - 1:
            next_non_zero_index = -1
            for i in range(len(non_zero_coords)):
               if non_zero_coords[i] == (r,c):
                   next_non_zero_index = i + 1
            
            if next_non_zero_index < len(non_zero_coords) :
               next_c = non_zero_coords[next_non_zero_index][1]
               if next_c == c+1:
                  # there is a connected pixel group, so don't insert
                  # the separator
                  insert_col = right_bound
               else:
                   # there is a gap, so insert the separator
                   insert_col = min(right_bound, input_grid.shape[1]-1)
                   output_grid[r,insert_col] = 5
                   insert_col += 1 #next insert is 1 space over

            else:
                # last pixel in the list
                insert_col = right_bound
        else:
            # on the last pixel
            insert_col = right_bound

    return output_grid