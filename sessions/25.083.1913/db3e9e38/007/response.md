```python
"""
1.  **Identify Orange Pixels:** Find all pixels with the value '7' (orange) in the input grid.
2.  **Process Each Row:** Iterate through each row of the input grid.
3.  **Conditional Row Construction:**
    *   If a row in the input grid contains one or more orange pixels (7):
        *   Construct a new row for the output grid.
        *   Iterate from n=1 to the number of 7s found at this row in the input
        *   For each n, insert n 8s followed by a 7 into the output.
        *   Fill the remaining spaces of output row to make the row the same with as input.
    *   If a row in the input grid does *not* contain any orange pixels:
        * The output will be the same as the input row

4. **Output Grid:** The result is the output grid, where rows corresponding to those with orange pixels in the input grid are replaced according to the rule above, and other rows remain the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through rows of the input grid
    for row_index in range(input_rows):
        # Find orange pixels in the current row
        orange_pixels_in_row = np.where(input_grid[row_index] == 7)[0]
        num_orange_pixels = len(orange_pixels_in_row)

        if num_orange_pixels > 0:
            # Construct the output row
            output_row = []
            for n in range(1,num_orange_pixels+1):
                # insert n 8s, follow by one 7
                output_row.extend( [8] * n)
                output_row.append(7)
            
            # Fill remaining with zeros
            output_row.extend([0] * (input_cols - len(output_row)))

            # Truncate if the row is too long, to fit input_cols
            output_row = output_row[:input_cols]  
            output_grid[row_index] = output_row
            
        else:
            # Copy the input row to the output grid if no orange pixels are present
            output_grid[row_index] = input_grid[row_index]

    return output_grid
```