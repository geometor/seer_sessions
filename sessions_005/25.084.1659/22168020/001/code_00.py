import numpy as np

"""
Fill horizontally between the extreme points of each non-white color within each row.

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Identify all unique colors present in the input grid, excluding white (color 0).
3.  For each unique non-white color found:
    a.  Iterate through each row index of the grid (from top to bottom).
    b.  Scan the current row in the input grid to find all column indices where the current non-white color exists.
    c.  If one or more pixels of the current color are found in this row:
        i.  Determine the minimum (leftmost) column index (`min_col`) and the maximum (rightmost) column index (`max_col`) among these pixels.
        ii. Iterate through the columns from `min_col` to `max_col` (inclusive) in the current row of the *output* grid.
        iii. Set the color of each pixel within this range (`min_col` to `max_col`) in the current row of the *output* grid to the current non-white color.
4.  After processing all unique non-white colors for all rows, return the final output grid.
"""

def transform(input_grid):
    """
    Fills horizontally between the leftmost and rightmost occurrences of each 
    non-white color within each row of the input grid.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Create a copy of the input grid to serve as the initial output grid.
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # 2. Identify all unique colors present in the input grid, excluding white (color 0).
    unique_colors = np.unique(input_np)
    non_white_colors = unique_colors[unique_colors != 0]
    
    # 3. For each unique non-white color found:
    for color in non_white_colors:
        # a. Iterate through each row index of the grid.
        for r in range(height):
            # b. Scan the current row in the input grid to find all column indices where the current non-white color exists.
            row = input_np[r, :]
            cols_with_color = np.where(row == color)[0]
            
            # c. If one or more pixels of the current color are found in this row:
            if cols_with_color.size > 0:
                # i. Determine the minimum (min_col) and maximum (max_col) column index.
                min_col = np.min(cols_with_color)
                max_col = np.max(cols_with_color)
                
                # ii & iii. Set the color of each pixel within this range in the output grid.
                # Note: NumPy slicing is inclusive of the start index and exclusive of the end index,
                # so we use max_col + 1 to include the rightmost column.
                output_grid[r, min_col:max_col + 1] = color
                
    # 4. Return the final output grid.
    # Convert back to list of lists if necessary for the environment, otherwise return the numpy array
    return output_grid.tolist()
