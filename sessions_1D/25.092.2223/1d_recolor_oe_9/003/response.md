```python
"""
Transform the input grid based on contiguous horizontal runs of maroon (9) pixels within each row.
1. Create the output grid as a copy of the input grid.
2. Iterate through each row of the grid.
3. Within each row, scan from left to right to find contiguous horizontal sequences (runs) of maroon (9) pixels.
4. For each identified run:
   - Determine the length of the run.
   - If the length is even, set the replacement color to orange (7).
   - If the length is odd, set the replacement color to blue (1).
   - Update the corresponding pixels in the output grid for that run with the determined replacement color.
5. Pixels that are not part of a maroon (9) run (i.e., white (0) pixels) remain unchanged.
6. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get grid dimensions
    height, width = input_grid.shape

    # Iterate through each row
    for r in range(height):
        c = 0 # Initialize column index for the current row
        while c < width:
            # Check if the current pixel is maroon (9)
            if input_grid[r, c] == 9:
                # Found the start of a potential run
                start_c = c
                run_length = 0
                # Count the length of the contiguous run of maroon pixels
                while c < width and input_grid[r, c] == 9:
                    run_length += 1
                    c += 1 # Move to the next column

                # Determine the replacement color based on run length parity
                if run_length % 2 == 0:
                    replacement_color = 7 # orange for even length
                else:
                    replacement_color = 1 # blue for odd length

                # Apply the replacement color to the output grid for the identified run
                for j in range(start_c, start_c + run_length):
                    output_grid[r, j] = replacement_color
                
                # 'c' is already positioned at the column after the run,
                # so the outer while loop will continue correctly
            else:
                # If the current pixel is not maroon, just move to the next pixel
                c += 1

    # Return the modified grid
    return output_grid
```