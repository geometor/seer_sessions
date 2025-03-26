```python
import numpy as np

"""
Expands an input grid by scaling pixels based on their position relative to the grid boundaries. 
Pixels on the first or last row are duplicated vertically if the grid has more than one row.
Pixels on the first or last column are duplicated horizontally if the grid has more than one column.
Pixels in corners are duplicated both vertically and horizontally (if applicable).
Pixels not on any boundary are copied directly without duplication.
The size of the output grid is determined by the sum of these scale factors.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the boundary expansion rule.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    H_in, W_in = input_grid.shape

    # 1. Determine Scaling Factors for each row and column
    # Row factor is 2 if it's a boundary row (and grid height > 1), else 1
    row_factors = [
        2 if H_in > 1 and (r == 0 or r == H_in - 1) else 1
        for r in range(H_in)
    ]
    # Column factor is 2 if it's a boundary column (and grid width > 1), else 1
    col_factors = [
        2 if W_in > 1 and (c == 0 or c == W_in - 1) else 1
        for c in range(W_in)
    ]

    # 2. Calculate Output Size
    H_out = sum(row_factors)
    W_out = sum(col_factors)

    # 3. Compute Start Offsets for rows and columns in the output grid
    # The starting row/col for input pixel (r, c) is the sum of factors before it.
    # We use np.cumsum for efficient calculation. Prepend 0 for the first element's offset.
    row_starts = np.cumsum([0] + row_factors[:-1])
    col_starts = np.cumsum([0] + col_factors[:-1])

    # 4. Construct Output Grid
    # Initialize the output grid with zeros (or any value, it will be overwritten)
    output_grid = np.zeros((H_out, W_out), dtype=input_grid.dtype)

    # Iterate through each pixel in the input grid
    for r in range(H_in):
        for c in range(W_in):
            # Get the input pixel value
            value = input_grid[r, c]
            
            # Get the scale factors for this pixel's position
            row_factor = row_factors[r]
            col_factor = col_factors[c]
            
            # Get the calculated start row and column in the output grid
            R_start = row_starts[r]
            C_start = col_starts[c]
            
            # Fill the corresponding rectangular block in the output grid
            output_grid[R_start : R_start + row_factor, C_start : C_start + col_factor] = value

    # 5. Return Output
    return output_grid.tolist() # Return as list of lists as per ARC standard

```