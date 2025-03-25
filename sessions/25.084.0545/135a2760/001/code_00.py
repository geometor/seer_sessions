"""
The transformation rule is as follows:

1.  **Preserve the Border:** The outermost rows and columns of the grid remain identical in the input and output.
2.  **Interior Transformation:** For cells not on the border:
    *   Examine runs of digits. It appears that alternating elements within long runs of the same color *other than* 2 are changed. The first element within the run *appears* to be very important.
    *   The key difference between train_1 and train_2 is that the position of the 3s, the 1s, 8s, 9s are shifted by one. It *looks* like every other instance of repeating digits is replaced.

"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of grid cell (diagonals included)"""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            # examine horizontal and vertical runs of length > 2
            
            # horizontal
            if input_grid[row, col] != 2:
                horiz_run = []
                #left
                j=col
                while j>=0 and input_grid[row, j] == input_grid[row, col]:
                    horiz_run.insert(0, (row, j))
                    j-=1

                #right
                j = col+1
                while j<cols and input_grid[row, j] == input_grid[row, col]:
                    horiz_run.append((row, j))
                    j+=1
            
                if len(horiz_run)>2:
                   # now replace alternating values
                   for k in range(len(horiz_run)):
                       r,c = horiz_run[k]
                       if k % 2 == 1:  #every other
                           output_grid[r, c] = input_grid[r,c]

            # vertical runs
            if input_grid[row, col] != 2:
                vert_run = []
                # up
                i = row
                while i >= 0 and input_grid[i, col] == input_grid[row, col]:
                    vert_run.insert(0, (i, col))
                    i -= 1

                # down
                i = row + 1
                while i < rows and input_grid[i, col] == input_grid[row, col]:
                    vert_run.append((i, col))
                    i += 1
                if len(vert_run) > 2:
                    for k in range(len(vert_run)):
                        r, c = vert_run[k]
                        if k % 2 == 1:  # every other
                            output_grid[r, c] = input_grid[r,c]



    return output_grid.tolist()