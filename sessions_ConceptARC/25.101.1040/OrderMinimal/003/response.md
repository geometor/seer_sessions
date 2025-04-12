```python
import numpy as np
import math 

"""
Transformation Rule:
Processes the grid row by row. For each row:
1. Find the number (N) and indices (C) of all yellow pixels (color 4).
2. If N=0 (no yellow pixels), the row remains all white (color 0).
3. If N > 0, calculate the centroid (mean column index) of the yellow pixels: mean_c = sum(C) / N.
4. Determine the target start index 'k' for a contiguous block of N yellow pixels. The goal is to center this block [k, k+N-1] around the calculated centroid mean_c.
5. The center of the target block is k + (N - 1) / 2.0. Set this equal to mean_c and solve for k: k = mean_c - (N - 1) / 2.0.
6. Since k must be an integer index, round the calculated float value: k = round(k_float). (Uses standard Python 3 round-half-to-even).
7. Clamp the calculated start index k to ensure the block fits within the row boundaries: 0 <= k <= width - N.
8. Create the output row: Place N yellow pixels contiguously starting at the clamped index k. All other cells in the row are white.
9. Combine the transformed rows to form the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the grid by rearranging yellow pixels in each row into a 
    single contiguous block. The block is positioned such that its center 
    is as close as possible to the centroid (mean position) of the 
    original yellow pixels in that row.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with background color (white = 0)
    output_array = np.zeros_like(input_array)

    # Process each row independently
    for r in range(height):
        # Find column indices of yellow pixels (color 4) in the current row
        yellow_indices = np.where(input_array[r] == 4)[0]
        N = len(yellow_indices) # Number of yellow pixels in the row

        # Only proceed if there are yellow pixels in the row
        if N > 0:
            # Calculate the centroid (mean column index) of the yellow pixels
            # Ensure float division
            mean_c = np.sum(yellow_indices) / N 

            # Calculate the ideal floating-point start index 'k_float'
            # This would place the center of the N-block exactly at mean_c
            k_float = mean_c - (N - 1) / 2.0
            
            # Round to the nearest integer to get the actual start index 'k'
            # Uses standard Python 3 round (rounds .5 to nearest even integer)
            k = int(round(k_float)) 

            # Clamp 'k' to ensure the block [k, k+N-1] fits within the grid width [0, width-1]
            # The maximum allowed start index is width - N
            k = max(0, k)           # Lower bound: k >= 0
            k = min(k, width - N)   # Upper bound: k <= width - N
            
            # Handle potential edge case where N > width (block can't fit)
            # The clamping above handles this by setting k=0, and the slice below works.

            # Determine the start and end columns for the yellow block
            start_col = k
            end_col = k + N # The end index is exclusive for slicing

            # Fill the calculated range in the output row with yellow (4)
            # Ensure indices are within bounds (although clamping k should guarantee this)
            if start_col < end_col and start_col < width and end_col <= width:
                 output_array[r, start_col:end_col] = 4

    # Convert the final NumPy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()
    return output_grid
```