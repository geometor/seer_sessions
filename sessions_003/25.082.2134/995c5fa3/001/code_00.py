"""
1.  **Examine Input:** Take the 4xN input grid, where N is the number of columns.
2.  **Consider Columns:** Observe each vertical column.
3. **Determine Output Rows:**
   * The output is a 3x3 grid
   * The output grid's first row consists of the color corresponding to the number of times that all `0`s are in the first row is equivalent to all columns where the `0` are on the bottom, starting from the left side
   * The output grid's second row is constructed by taking the number of columns where `0` are on the bottom, starting from the right side.
   * The output grid's third row are determined by all contiguous groups of 0s, starting from the left side.

4. **Return Output Grid:** Construct and return the 3x3 output grid, where all values in each row is the same.
"""

import numpy as np

def get_contiguous_zeros_start(grid):
    count = 0
    for j in range(grid.shape[1]):
        if grid[0,j] == 0:
            count +=1
        else:
            break
    return count

def count_zeros_bottom_start(grid):
    count = 0
    for j in range(grid.shape[1]):
        if grid[3, j] == 0:
            count += 1
        else:
            break

    return count

def count_zeros_bottom_end(grid):
    count = 0
    for j in range(grid.shape[1] -1, -1, -1):
        if grid[3,j] == 0:
            count += 1
        else:
            break
    return count

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # change output pixels
    output_grid[0, :] = get_contiguous_zeros_start(input_grid) % 10
    output_grid[1, :] = count_zeros_bottom_end(input_grid) % 10
    output_grid[2, :] = count_zeros_bottom_start(input_grid) % 10

    return output_grid