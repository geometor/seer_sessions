```python
import numpy as np

"""
Transformation Rule:

1. Iterate through each row of the input grid.
2. Identify rows that meet specific criteria:
    a. The row must contain exactly two non-white (non-zero) pixels.
    b. One non-white pixel must be in the first column (index 0).
    c. The other non-white pixel must be in the last column (index width - 1).
3. If a row meets these criteria:
    a. Determine the color of the leftmost pixel (`left_color`) and the rightmost pixel (`right_color`).
    b. Calculate the midpoint column index: `mid_col = floor((width - 1) / 2)`.
    c. Modify the corresponding row in the output grid:
        i. Fill columns from 0 up to (but not including) `mid_col` with `left_color`.
        ii. Fill the column at `mid_col` with gray (5).
        iii. Fill columns from `mid_col + 1` up to (and including) `width - 1` with `right_color`.
4. If a row does *not* meet the criteria, copy it unchanged from the input to the output grid.
5. Return the modified grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the described rule: finds rows with non-white
    pixels only at the edges, then fills the row with the edge colors meeting
    at a gray divider in the middle.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize the output grid as a copy of the input grid.
    # Rows that don't match the criteria will remain unchanged.
    output_array = np.copy(input_array)

    # Iterate through each row
    for r in range(height):
        row = input_array[r, :]
        
        # Find non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        num_non_white = len(non_white_indices)
        
        # Check criteria: exactly 2 non-white pixels, one at the start, one at the end
        if num_non_white == 2 and row[0] != 0 and row[width - 1] != 0:
            # Get the colors from the edges
            left_color = row[0]
            right_color = row[width - 1]
            
            # Calculate the midpoint column index (using integer division)
            mid_col = (width - 1) // 2
            
            # Fill the left part of the output row
            output_array[r, 0:mid_col] = left_color
            
            # Place the gray divider at the midpoint
            output_array[r, mid_col] = 5
            
            # Fill the right part of the output row
            output_array[r, mid_col + 1:width] = right_color
            
    # Convert the output NumPy array back to a list of lists before returning
    return output_array.tolist()

```