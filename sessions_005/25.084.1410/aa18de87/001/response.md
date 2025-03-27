```python
import numpy as np
import copy

"""
Iterate through each row of the input grid. For each row, find the column indices
of all non-white pixels (pixels with value != 0). If there are two or more 
non-white pixels in the row, find the minimum (leftmost) and maximum (rightmost)
of these column indices. Then, iterate through the columns strictly between the 
minimum and maximum indices. If a pixel at these intermediate columns in the 
original input row was white (0), change its color to red (2) in the output grid. 
Rows with fewer than two non-white pixels remain unchanged.
"""

def transform(input_grid):
    """
    Fills the horizontal space between the leftmost and rightmost non-white pixels 
    in each row with red (2), provided the original pixel was white (0).

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed grid.
    """
    # Convert input to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a deep copy for the output grid to modify
    output_np = copy.deepcopy(input_np)
    
    # Get the dimensions of the grid
    height, width = input_np.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Find the column indices of all non-white pixels in the current row
        # np.where returns a tuple of arrays (one for each dimension); we need the first element
        non_white_indices = np.where(input_np[r, :] != 0)[0] 

        # Check if there are at least two non-white pixels in the row
        if len(non_white_indices) >= 2:
            # Find the minimum (leftmost) and maximum (rightmost) column index
            min_col = np.min(non_white_indices)
            max_col = np.max(non_white_indices)

            # Iterate through the columns strictly between the min and max indices
            # range(start, stop) excludes stop, so max_col works as intended
            for c in range(min_col + 1, max_col):
                # Check if the pixel in the *original* input grid at this position was white (0)
                if input_np[r, c] == 0:
                    # If it was white, change the corresponding pixel in the output grid to red (2)
                    output_np[r, c] = 2
                    
    # Convert the final numpy array back to a list of lists before returning
    output_grid = output_np.tolist()
    return output_grid

```