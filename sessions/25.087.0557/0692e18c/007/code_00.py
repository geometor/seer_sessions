"""
Transforms an input grid into an output grid by replacing each pixel with a corresponding 3x3 pattern based on the pixel's color.

The transformation follows these steps:
1.  Define a mapping from input pixel colors to specific 3x3 grid patterns. Based on the examples, this mapping is:
    *   White (0) maps to a 3x3 grid of all White (0).
    *   Orange (7) maps to [[7, 0, 7], [0, 0, 0], [7, 0, 7]].
    *   Magenta (6) maps to [[6, 6, 0], [6, 0, 6], [0, 6, 6]].
    *   Yellow (4) maps to [[0, 0, 4], [4, 4, 0], [4, 4, 0]].
2.  Determine the dimensions (Height_in, Width_in) of the input grid.
3.  Calculate the output grid dimensions: Height_out = Height_in * 3, Width_out = Width_in * 3.
4.  Create a new output grid of size (Height_out, Width_out), initialized with the background color (White, 0).
5.  Iterate through each pixel of the input grid at coordinates (r_in, c_in).
6.  For each input pixel, get its color 'C'.
7.  Retrieve the 3x3 pattern associated with color 'C' from the predefined mapping.
8.  Calculate the top-left coordinates (start_row, start_col) for the corresponding subgrid in the output grid: start_row = r_in * 3, start_col = c_in * 3.
9.  Copy the retrieved 3x3 pattern into the output grid starting at (start_row, start_col).
10. Return the completed output grid.
"""

import numpy as np

# Define the 3x3 patterns associated with each color found in the training examples.
# Using NumPy arrays for easier slicing and assignment.
COLOR_PATTERNS = {
    0: np.array([[0, 0, 0], 
                 [0, 0, 0], 
                 [0, 0, 0]], dtype=int),
    7: np.array([[7, 0, 7], 
                 [0, 0, 0], 
                 [7, 0, 7]], dtype=int),
    6: np.array([[6, 6, 0], 
                 [6, 0, 6], 
                 [0, 6, 6]], dtype=int),
    4: np.array([[0, 0, 4], 
                 [4, 4, 0], 
                 [4, 4, 0]], dtype=int)
}
# Define the scaling factor
SCALE_FACTOR = 3
# Define the background color
BACKGROUND_COLOR = 0

def transform(input_grid):
    """
    Applies the color-to-pattern mapping transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array
    input_np = np.array(input_grid, dtype=int)
    
    # Determine input dimensions
    h_in, w_in = input_np.shape
    
    # Calculate output dimensions
    h_out = h_in * SCALE_FACTOR
    w_out = w_in * SCALE_FACTOR
    
    # Initialize the output grid with the background color
    output_grid = np.full((h_out, w_out), BACKGROUND_COLOR, dtype=int)
    
    # Iterate through each cell of the input grid
    for r_in in range(h_in):
        for c_in in range(w_in):
            # Get the color of the current input cell
            color = input_np[r_in, c_in]
            
            # Retrieve the corresponding 3x3 pattern for the color.
            # If the color is not in our predefined map, default to the background pattern.
            pattern = COLOR_PATTERNS.get(color, COLOR_PATTERNS[BACKGROUND_COLOR])
            
            # Calculate the top-left corner coordinates for placing the pattern in the output grid
            start_r = r_in * SCALE_FACTOR
            start_c = c_in * SCALE_FACTOR
            
            # Calculate the slice for the target 3x3 subgrid
            end_r = start_r + SCALE_FACTOR
            end_c = start_c + SCALE_FACTOR
            
            # Place the pattern into the calculated subgrid in the output grid
            output_grid[start_r:end_r, start_c:end_c] = pattern
            
    # Convert the final NumPy array back to a list of lists before returning
    return output_grid.tolist()
