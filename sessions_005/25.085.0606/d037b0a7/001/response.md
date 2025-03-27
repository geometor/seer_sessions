```python
import numpy as np

"""
For each column independently, iterate from top to bottom. Maintain the most recently seen non-White color ('last_color', initially White). 
If the current pixel in the input grid is non-White, update 'last_color'. 
If 'last_color' is currently non-White, set the corresponding pixel in the output grid to 'last_color'. Otherwise, leave it White.
Essentially, non-White colors 'fall' or 'fill' downwards into White spaces within their respective columns.
"""

def transform(input_grid):
    """
    Applies a downward fill transformation to each column of the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid representing colors.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid. 
    # We will modify this grid based on the fill logic.
    output_grid = np.copy(input_np) 

    # Iterate through each column
    for c in range(width):
        # Initialize the last non-white color seen in this column
        last_color = 0  # 0 represents White

        # Iterate through each row in the current column, from top to bottom
        for r in range(height):
            # Get the color of the pixel in the original input grid
            input_color = input_np[r, c]

            # If the input pixel is not White, update the last seen color
            if input_color != 0:
                last_color = input_color
            
            # If the last seen color is not White (meaning we've encountered a non-white pixel above or at this row)
            # and the current pixel in the *output* grid is White (meaning it was originally White or hasn't been filled yet),
            # then fill the current output pixel with the last seen color.
            # Note: We check output_grid[r,c] == 0 because a pixel might have been non-white initially, 
            # and we don't want to overwrite it with a color from higher up if it already has its own color.
            # However, the simpler logic based on the NL description is:
            # If last_color is not White, set the output pixel to last_color.
            # Let's refine: Check the *input* pixel. If it was white and we have a last_color, fill it.
            
            # Revision based on NL program step 7:
            # If `last_color` is not White (i.e., `last_color != 0`), set the color of the pixel at `(r, c)` 
            # in the *output* grid to `last_color`.
            if last_color != 0:
                 output_grid[r, c] = last_color
            # If last_color is still 0 (White), the output pixel at (r, c) should remain 0 (White),
            # which is handled because output_grid was initialized with 0s or copied and might already be 0.
            # Let's re-check the copy logic. If we copy, we need to be careful.
            # If input is [0, 2, 0], last_color becomes 2 at row 1. At row 2, input is 0, last_color is 2.
            # Output should be [0, 2, 2].
            # If input is [7, 0, 8], output should be [7, 7, 8]. -> Wait, example 1 output is [0,2,0], [7,2,8], [7,2,8]
            # Input Col 0: [0, 7, 0] -> last_color=0, then 7, then 7. Output Col 0: [0, 7, 7] -> Correct.
            # Input Col 1: [2, 0, 0] -> last_color=2, then 2, then 2. Output Col 1: [2, 2, 2] -> Correct.
            # Input Col 2: [0, 8, 0] -> last_color=0, then 8, then 8. Output Col 2: [0, 8, 8] -> Correct.
            
            # The simple logic seems correct: once a non-white is seen, fill downwards with it.
            # Let's trace example 1 again carefully.
            # Input:
            # 0 2 0
            # 7 0 8
            # 0 0 0
            # Output:
            # 0 2 0  -> Hmm, looks like initial non-white pixels AREN'T overwritten by colors from above.
            # 7 2 8
            # 7 2 8
            
            # Okay, refined logic:
            # If input_color is non-white, update last_color.
            # If the *original* input_color at (r, c) was WHITE *and* last_color is non-white, update output_grid[r, c] = last_color.
            
    # Let's re-implement with this refined logic, starting from a fresh output grid of zeros.
    output_grid_zeros = np.zeros_like(input_np, dtype=int)
    for c in range(width):
        last_color = 0 
        for r in range(height):
            input_color = input_np[r, c]
            
            # Update last_color if the current input pixel is non-white
            if input_color != 0:
                last_color = input_color
                # Set the output pixel to this non-white color immediately
                output_grid_zeros[r, c] = input_color 
            
            # If the input pixel was originally white, but we have a fill color...
            elif input_color == 0 and last_color != 0:
                # Set the output pixel to the fill color
                output_grid_zeros[r, c] = last_color
            
            # If input_color is 0 and last_color is 0, output remains 0 (already initialized)

    # This looks correct now and matches the NL program step 7 more closely.
    return output_grid_zeros

```