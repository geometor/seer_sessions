```python
"""
Yellow pixels remain in their original positions. Azure pixels move based on their connectivity and initial location.
Isolated azure pixels are duplicated within its row. If it starts at column 0, it adds a copy to its right. If not, it moves to column 0.
Horizontally connected azure pixels expands to the nearest edge of the grid, keeping the relative position (left, right)
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Get the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                neighbors.append((r, c))
    return neighbors

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

def count_same_color_in_row(grid, row, col):
    """Counts the number of pixels of the same color in a row."""
    count = 0
    rows, cols = grid.shape
    for c in range(cols):
        if grid[row,c] == grid[row,col]:
            count = count + 1
    return count

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Yellow pixels remain unchanged
            if input_grid[r, c] == 4:
                continue  # Yellow pixels are already in place

            # Handle azure pixels
            if input_grid[r, c] == 8:
                if not is_horizontally_connected(input_grid, r, c):
                    # Isolated azure pixel
                    if c == 0:
                        # Duplicate to the right
                        output_grid[r, c+1] = 8
                    elif count_same_color_in_row(input_grid,r,c) > 1:
                        first_c = -1
                        for current_c in range(cols):
                            if input_grid[r,current_c] == 8:
                                if first_c == -1:
                                    first_c = current_c
                                output_grid[r,current_c] = 0

                        output_grid[r,0] = 8
                        output_grid[r,1] = 8

                    else:
                        # Move to the leftmost position
                        output_grid[r, 0] = 8
                        output_grid[r,c] = 0 #clear original

                else:
                    # Horizontally connected azure pixels: expand to border.
                    azure_group = []
                    current_c = c
                    
                    while current_c < cols and input_grid[r,current_c] == 8:
                        azure_group.append(current_c)
                        current_c += 1
                    if(len(azure_group) == 0):
                       current_c = c-1
                       while current_c >= 0 and input_grid[r,current_c] == 8:
                            azure_group.append(current_c)
                            current_c -= 1

                    first = min(azure_group)
                    last  = max(azure_group)
                    for i in range(first,last+1):
                            output_grid[r,i]=0

                    if first == 0:

                        #expand right
                         for i in range(len(azure_group)):
                            output_grid[r,i]=8

                    else:
                        #expand left
                         for i in range(first,last+1):
                            output_grid[r,i-first]=8


    return output_grid
```