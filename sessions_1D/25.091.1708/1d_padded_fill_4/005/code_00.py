import numpy as np

"""
Transforms the input grid based on row index parity and the location of the leftmost non-background pixel.

For each row in the input grid:
1. Find the column index (`first_col`) and color (`fill_color`) of the leftmost non-background pixel (color != 0).
2. If no non-background pixel exists in the row, the row remains unchanged in the output.
3. If the row index is even (0, 2, 4, ...):
   Fill the corresponding row in the output grid from column `first_col` to the right edge (last column) with `fill_color`.
4. If the row index is odd (1, 3, 5, ...):
   Fill the corresponding row in the output grid from the left edge (column 0) up to and including column `first_col` with `fill_color`.
"""

def find_leftmost_non_background(row):
    """
    Finds the index and color of the leftmost non-background pixel in a row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
                        Background color is assumed to be 0.

    Returns:
        tuple: (column_index, color) if found, otherwise (None, None).
    """
    for col_index, pixel_color in enumerate(row):
        # Check if the pixel color is not the background color (0)
        if pixel_color != 0:
            return col_index, pixel_color
    # Return None if no non-background pixel is found in the row
    return None, None

def transform(input_grid):
    """
    Applies the alternating row fill transformation based on row index parity.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid. Modifications will be made to this copy.
    output_grid = np.copy(input_np)
    
    # Get the dimensions (number of rows and columns) of the grid
    num_rows, num_cols = output_grid.shape

    # Iterate through each row of the grid using its index 'r'
    for r in range(num_rows):
        # Get the current row from the *original* input grid to find the trigger pixel
        current_row_input = input_np[r, :]
        
        # Find the column index and color of the leftmost non-background pixel in the current input row
        first_col, fill_color = find_leftmost_non_background(current_row_input)
        
        # Proceed only if a non-background pixel was found in this row
        if first_col is not None:
            # Check if the row index 'r' is even
            if r % 2 == 0:
                # Even row: Fill the output grid's row from the 'first_col' to the right edge
                for c in range(first_col, num_cols):
                    output_grid[r, c] = fill_color
            else:
                # Odd row: Fill the output grid's row from the left edge (column 0) up to and including 'first_col'
                for c in range(0, first_col + 1):
                    output_grid[r, c] = fill_color
                    
    # Convert the resulting numpy array back to a list of lists for the standard ARC output format
    return output_grid.tolist()