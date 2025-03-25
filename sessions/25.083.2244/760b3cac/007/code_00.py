"""
1.  Yellow Pixels (4): Remain unchanged in their original positions.

2.  Azure Pixels (8): Their behavior depends on whether they are horizontally connected to other azure pixels.

    *   Isolated Azure Pixels: An azure pixel is considered "isolated" if it has no immediate horizontal neighbors (left or right) of the same color (8).
        *   Leftmost Isolated Azure Pixel: If an isolated azure pixel is at the leftmost edge (column 0) of the grid, it duplicates itself to the immediate right.
        *   Other Isolated Azure Pixel: If an isolated azure pixel is *not* at the leftmost edge, and is the *only* azure pixel on its row, it moves to the leftmost position (column 0) of its row.
        *  Multiple Azure Pixels: If an isolate azure pixel is on a row with another azure pixel, all azure pixels are cleared on the row, and two azure pixels are added to the leftmost edge.

    *   Horizontally Connected Azure Pixels: Two or more azure pixels are "horizontally connected" if they are adjacent in the same row.
         *  Duplicate the connected azure pixels to *both* edges, filling from the edges with connected azure pixels.
"""

import numpy as np

def is_horizontally_connected(grid, row, col):
    """Checks if an azure pixel is horizontally connected."""
    if grid[row, col] != 8:
        return False

    rows, cols = grid.shape
    if col > 0 and grid[row, col - 1] == 8:
        return True
    if col < cols - 1 and grid[row, col + 1] == 8:
        return True
    return False

def count_azure_in_row(grid, row):
    """Counts azure pixels in a row"""
    count = 0
    rows, cols = grid.shape
    for c in range(cols):
        if grid[row,c] == 8:
            count += 1
    return count

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Yellow pixels remain unchanged
            if input_grid[r, c] == 4:
                continue

            # Handle azure pixels
            if input_grid[r, c] == 8:
                if not is_horizontally_connected(input_grid, r, c):
                    # Isolated azure pixel
                    if c == 0:
                        # Leftmost Isolated Azure Pixel: duplicate to the right
                        output_grid[r, c+1] = 8
                    elif count_azure_in_row(input_grid,r) > 1:
                        #Multiple Isolated Azure Pixels:
                        for current_c in range(cols):
                            if input_grid[r,current_c] == 8:
                                output_grid[r,current_c] = 0
                        output_grid[r,0] = 8
                        output_grid[r,1] = 8

                    else:
                        # Other Isolated Azure Pixel -  move to the leftmost position
                        output_grid[r, 0] = 8
                        output_grid[r,c] = 0 #clear original

                else:
                    # Horizontally connected azure pixels.
                    azure_group = []
                    #find the connected pixels

                    current_c = c
                    while current_c >= 0 and input_grid[r,current_c] == 8 :
                        azure_group.append(current_c)
                        current_c = current_c - 1
                    current_c = c + 1
                    while current_c < cols and input_grid[r,current_c] == 8:
                        azure_group.append(current_c)
                        current_c = current_c + 1
                    
                    #clear existing
                    for i in azure_group:
                        output_grid[r,i] = 0

                    #fill from left
                    left_count = len(azure_group)
                    for i in range(left_count):
                        output_grid[r,i] = 8

                    #fill from right
                    right_start = cols - len(azure_group)
                    for i in range(right_start,cols):
                        output_grid[r,i] = 8

    return output_grid