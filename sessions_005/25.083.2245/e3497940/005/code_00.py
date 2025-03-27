"""
1.  **Iterate through each row** of the input grid.
2.  **Locate the first Gray (5) pixel** in the current row. This pixel acts as the dividing point for that row.
3.  **Extract Pixels:** Copy all pixels to the left of the located Gray pixel in the current row.
4.  **Construct Output Grid:** The output grid will have the same number of rows as the input grid. For each row, the number of columns in the output will match the column index of the first Gray pixel found in the corresponding row of the input grid. Copy the extracted pixels into the corresponding row of the output grid.
5.  **Output:** Return the final output grid.
"""

import numpy as np

def find_first_gray_column(row):
    """Finds the column index of the first gray pixel in a row."""
    try:
        return np.where(row == 5)[0][0]
    except IndexError:
        return -1  # No gray pixel found

def transform(input_grid):
    """Transforms the input grid by extracting the region to the left of the first gray pixel in each row."""
    num_rows = input_grid.shape[0]
    
    # Find the gray marker column for each row.
    gray_marker_cols = [find_first_gray_column(row) for row in input_grid]

    # Determine number of columns in the output by using maximum of gray bar
    # columns
    num_cols = max(gray_marker_cols)    
    if num_cols < 0:      
        return np.zeros((num_rows, 0), dtype=int)   
    # Initialize the output grid
    output_grid = np.zeros((num_rows, num_cols), dtype=int)

    # Iterate through each row and copy pixels to the left of the gray marker
    for i, row in enumerate(input_grid):
        gray_col = gray_marker_cols[i]
        if gray_col > 0:  # Only copy if a gray pixel was found
            output_grid[i, :gray_col] = row[:gray_col]

    return output_grid