"""
1.  **Identify Key Pixels:** Find the coordinates of the single azure pixel ('8') and the single orange pixel ('7') in the input grid.
2.  **Calculate Dimensions:** Determine the number of rows above the azure pixel (`rows_above`), the number of rows below the azure pixel (`rows_below`), and the horizontal distance (number of columns) between the azure and orange pixels (`separation`).
3. **Determine Output Grid Size**: The output grid will have the same number of rows as the input grid.
4.  **Vertical Expansion:** Duplicate the row containing the azure and orange pixels. Create `rows_above` copies of this row *above* the original row's position in the new grid, and `rows_below` copies *below* the original row's position.
5.  **Horizontal Expansion:**
    *   Expand the azure pixel ('8') to the *left* by `separation` columns.
    *   Expand the orange pixel ('7') to the *right* by `separation` columns.
6.  **Insert Diagonal:** Insert a diagonal line of red pixels ('2').
    *   The line starts at row index `rows_above` and column index (`col_8` + `separation` - x) , where col_8 is original column position of `8`. The first "2" should appear at the top of the expanded region of 8s.
    *   The line proceeds diagonally downwards and to the right.
"""

import numpy as np

def find_pixels(grid, pixel_values):
    """Finds the coordinates of specified pixels in the grid."""
    coords = {}
    for value in pixel_values:
        coords[value] = []
        for r, row in enumerate(grid):
            for c, pixel in enumerate(row):
                if pixel == value:
                    coords[value].append((r, c))
    return coords

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    

    # 1. Identify key pixels
    pixel_coords = find_pixels(input_grid, [7, 8])

    # Ensure that there's only one of each for this simple case.  Later, handle multiple.
    eight_coord = pixel_coords[8][0]
    seven_coord = pixel_coords[7][0]
    row_8, col_8 = eight_coord
    row_7, col_7 = seven_coord

    # 2. Calculate Dimensions
    separation = col_7 - col_8
    rows_above = row_8
    rows_below = input_grid.shape[0] - row_8 - 1
    
    # 3. Determine Output Grid Size
    output_grid = np.zeros_like(input_grid)

    # 4. Vertical Expansion
    base_row = input_grid[row_8,:]
    
    row_insert = 0
    for i in range(rows_above):
      output_grid[row_insert,:] = base_row
      row_insert += 1
    
    output_grid[row_insert,:] = base_row
    row_insert += 1
    
    for i in range(rows_below):
      output_grid[row_insert,:] = base_row
      row_insert += 1      
    
    # 5. Horizontal Expansion

    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if c < col_8 and output_grid[r,col_8] == 8:
               output_grid[r,c] = 8
            elif c > col_7  and output_grid[r,col_7] == 7:
                output_grid[r,c] = 7

    # 6. insert diagonal
    for i in range(output_grid.shape[0] - rows_above):
      if (col_8 + separation -1 + i) < output_grid.shape[1]:
        output_grid[rows_above + i, col_8 + separation - 1 + i] = 2

    return output_grid