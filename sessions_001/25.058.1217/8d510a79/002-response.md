# 8d510a79 • 002 • example_2 • investigate_coder

---
```python
"""
Transforms an input grid by vertically mirroring isolated colored pixels (blue and red)
across a static gray row and replicating vertical strings of the same-colored pixels.
"""

import numpy as np

def find_static_row(grid, color=5):
    """Finds the row index of the static gray line."""
    for i, row in enumerate(grid):
        if all(pixel == color for pixel in row):
            return i
    return -1  # Should not happen in valid cases

def is_isolated(grid, row, col, static_row_index):
    """Checks if a colored pixel is isolated vertically (only checks within its region)."""
    color = grid[row, col]
    height = len(grid)

    if row < static_row_index: #above static row
        if row > 0 and grid[row - 1, col] == color:
            return False
        if row < static_row_index - 1 and grid[row + 1, col] == color:
            return False
    else: #below static row
        if row > static_row_index + 1 and grid[row - 1, col] == color:
            return False
        if row < height - 1 and grid[row + 1, col] == color:
            return False

    return True

def find_vertical_string(grid, row, col, static_row_index):
    """Finds the start and end row indices of a vertical string of same-colored pixels."""
    color = grid[row, col]
    height = len(grid)
    start_row = row
    end_row = row

    if row < static_row_index:
        # Search upwards
        while start_row > 0 and grid[start_row - 1, col] == color:
            start_row -= 1
        #search downwards
        while end_row < static_row_index -1 and grid[end_row+1, col] == color:
            end_row += 1
    else:
        while start_row > static_row_index + 1 and grid[start_row - 1, col] == color:
            start_row -= 1
        while end_row < height - 1 and grid[end_row + 1, col] == color:
            end_row += 1

    return start_row, end_row
    
def transform(input_grid):
    """Transforms the input grid according to the mirroring and replication rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    height, width = grid.shape
    output_grid = grid.copy()
    static_row_index = find_static_row(grid)

    for row in range(height):
        for col in range(width):
            if row == static_row_index:
                continue  # Skip the static gray row

            pixel_color = grid[row, col]

            if pixel_color in (1, 2):  # Blue or Red
                if is_isolated(grid, row, col, static_row_index):
                    # Mirror isolated pixels
                    if row < static_row_index:
                        mirror_row = static_row_index + (static_row_index - row)
                    else:
                        mirror_row = static_row_index - (row - static_row_index)
                    if mirror_row < height and output_grid[mirror_row, col] == 0:
                         output_grid[mirror_row, col] = pixel_color
                else:
                    # Replicate pixel string
                    start_row, end_row = find_vertical_string(grid, row, col, static_row_index)

                    if row < static_row_index:
                        target_start_row = static_row_index + (static_row_index - end_row)
                        target_end_row = static_row_index + (static_row_index - start_row)
                    else:
                        target_start_row = static_row_index - (end_row - static_row_index)
                        target_end_row = static_row_index - (start_row - static_row_index)
                    
                    #only copy string of pixels if we haven't done it yet
                    if row == start_row:
                        string_length = end_row - start_row + 1
                        if target_start_row >=0 and target_start_row < height and target_end_row >=0 and target_end_row < height:
                            for i in range(string_length):
                                output_grid[target_start_row + i, col] = grid[start_row + i, col]
                    
                    #we only need to check the string once
                    row = end_row
                    
    return output_grid.tolist() #convert back to list
```
