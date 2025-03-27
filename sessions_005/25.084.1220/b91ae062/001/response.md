```python
import numpy as np

"""
Identifies all unique non-white (non-zero) pixel values in the input grid.
Counts the number of these unique non-white values to determine a scaling factor 'N'.
Creates an output grid where each pixel (r, c) of the input grid is expanded into an N x N block of the same color in the output grid, positioned at the top-left coordinate (r * N, c * N).
The final output grid dimensions are N times the input grid dimensions.
"""

def transform(input_grid):
    """
    Scales the input grid by a factor N, where N is the count of unique non-white colors.
    Each input pixel becomes an N x N block in the output grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    
    # Find unique non-white pixel values
    unique_values = np.unique(input_array)
    non_white_values = unique_values[unique_values != 0]
    
    # Determine the scaling factor N
    # If there are no non-white colors, the logic implies N=0. 
    # An output grid of size 0x0 might be the correct interpretation,
    # or perhaps a default scaling of 1 should apply. 
    # Based on examples, N is always >= 2. Let's strictly follow the derived rule.
    N = len(non_white_values)

    # Handle the edge case where N=0 (only white pixels in input)
    if N == 0:
        # Option 1: Return an empty grid (0x0)
        # return [] 
        # Option 2: Return the input grid unchanged (equivalent to N=1)
        # N = 1 
        # Option 3: Default N to 1 if input contains only white. Let's choose this for now as it seems less likely to break.
        N = 1 

    # Get input dimensions
    H, W = input_array.shape
    
    # Calculate output dimensions
    output_H = H * N
    output_W = W * N
    
    # Initialize the output grid (using the background color 0 - white)
    output_array = np.zeros((output_H, output_W), dtype=int)
    
    # Iterate through each pixel of the input grid
    for r in range(H):
        for c in range(W):
            # Get the color of the input pixel
            color = input_array[r, c]
            
            # Calculate the top-left corner of the block in the output grid
            start_row = r * N
            start_col = c * N
            
            # Fill the N x N block in the output grid with the color
            output_array[start_row : start_row + N, start_col : start_col + N] = color
            
    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid

```