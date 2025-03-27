```python
import numpy as np

"""
Transforms an input grid into an output grid that is twice the height and twice the width.
Each pixel in the input grid corresponds to a 2x2 block in the output grid.

Transformation Rule:
1. If an input pixel color is non-white (not 0), the corresponding 2x2 block in the output grid is filled entirely with that input pixel's color.
2. If an input pixel color is white (0), the corresponding 2x2 block in the output grid is filled with a specific pattern: 
   - Top-left cell: blue (1)
   - Bottom-right cell: blue (1)
   - Top-right cell: white (0)
   - Bottom-left cell: white (0)
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Determine the dimensions of the input grid
    input_height, input_width = input_array.shape
    
    # Calculate the dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_array[r, c]
            
            # Calculate the top-left coordinates of the corresponding 2x2 block in the output grid
            out_r = 2 * r
            out_c = 2 * c
            
            # Apply the transformation rule based on the input color
            if input_color != 0:
                # If input color is non-white, fill the 2x2 block with the input color
                output_grid[out_r:out_r+2, out_c:out_c+2] = input_color
            else:
                # If input color is white, apply the specific blue pattern
                output_grid[out_r, out_c] = 1  # Top-left
                # output_grid[out_r, out_c+1] = 0 # Top-right (already 0 from initialization)
                # output_grid[out_r+1, out_c] = 0 # Bottom-left (already 0 from initialization)
                output_grid[out_r+1, out_c+1] = 1 # Bottom-right

    return output_grid
```