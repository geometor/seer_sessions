```python
import numpy as np

"""
The transformation takes a square input grid (N x N) and produces an output grid of double the dimensions (2N x 2N). 
The output grid is composed of four N x N quadrants, each being a rotation of the original input grid.
Specifically:
- The top-left quadrant is the original input grid (0 degrees rotation).
- The top-right quadrant is the input grid rotated 270 degrees clockwise (or 90 degrees counter-clockwise).
- The bottom-left quadrant is the input grid rotated 180 degrees clockwise.
- The bottom-right quadrant is the input grid rotated 90 degrees clockwise.
"""

def transform(input_grid):
    """
    Constructs a 2x2 tiled grid where each tile is a rotation of the input grid.
    
    Args:
        input_grid (list of lists): A square grid of integers representing colors.

    Returns:
        list of lists: The transformed grid, double the dimensions of the input.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid (assuming square N x N)
    n = input_np.shape[0]
    
    # Ensure the input is square
    if input_np.shape[0] != input_np.shape[1]:
        raise ValueError("Input grid must be square")
        
    # Calculate the four required rotations of the input grid
    # np.rot90 rotates counter-clockwise by default (k=1 is 90 deg CCW)
    rot0 = input_np  # 0 degrees rotation (original)
    rot90_ccw = np.rot90(input_np, k=1)  # 90 degrees counter-clockwise (270 clockwise)
    rot180_ccw = np.rot90(input_np, k=2)  # 180 degrees counter-clockwise (180 clockwise)
    rot270_ccw = np.rot90(input_np, k=3)  # 270 degrees counter-clockwise (90 clockwise)

    # Define the quadrant assignments based on clockwise rotation
    top_left = rot0
    top_right = rot90_ccw  # Corresponds to 270 deg CW
    bottom_left = rot180_ccw # Corresponds to 180 deg CW
    bottom_right = rot270_ccw # Corresponds to 90 deg CW
    
    # Create the output grid, initialized with zeros, size 2N x 2N
    output_size = 2 * n
    output_np = np.zeros((output_size, output_size), dtype=int)
    
    # Place the rotated grids into the corresponding quadrants of the output grid
    output_np[0:n, 0:n] = top_left        # Top-Left
    output_np[0:n, n:output_size] = top_right   # Top-Right
    output_np[n:output_size, 0:n] = bottom_left # Bottom-Left
    output_np[n:output_size, n:output_size] = bottom_right # Bottom-Right
    
    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid

```