```python
import numpy as np

"""
Scale the input grid by a factor of 2x. Each pixel in the input grid at 
position (r, c) with color C is replaced by a 2x2 block of color C 
in the output grid, with the top-left corner of the block at 
position (r*2, c*2).
"""

def transform(input_grid):
    """
    Scales the input grid by a factor of 2 in both height and width.

    Args:
        input_grid (list[list[int]] or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid, scaled 2x.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Calculate the dimensions of the output grid
    H_out = H * 2
    W_out = W * 2
    
    # Initialize the output grid with zeros (or any placeholder)
    # Using the same dtype as input is good practice
    output_grid = np.zeros((H_out, W_out), dtype=input_np.dtype)
    
    # Iterate through each pixel in the input grid
    for r in range(H):
        for c in range(W):
            # Get the color of the current input pixel
            color = input_np[r, c]
            
            # Determine the top-left corner coordinates in the output grid
            r_out = r * 2
            c_out = c * 2
            
            # Fill the corresponding 2x2 block in the output grid with the color
            # Using slicing for concise assignment
            output_grid[r_out : r_out + 2, c_out : c_out + 2] = color
            
    # Return the completed output grid
    return output_grid

```