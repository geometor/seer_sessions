"""
Combine three vertically stacked 5x5 input layers (from a 15x5 input grid) 
into a single 5x5 output grid based on color priority.

The input grid consists of three 5x5 layers stacked vertically:
- Layer 1 (rows 0-4): Contains white (0) and blue (1).
- Layer 2 (rows 5-9): Contains white (0) and azure (8).
- Layer 3 (rows 10-14): Contains white (0) and magenta (6).

The output grid is a 5x5 grid. Each pixel at (r, c) in the output is 
determined by the pixels at (r, c), (r+5, c), and (r+10, c) in the input,
following this priority rule:
1. If the pixel in Layer 3 is magenta (6), the output pixel is magenta (6).
2. Else, if the pixel in Layer 1 is blue (1), the output pixel is blue (1).
3. Else, if the pixel in Layer 2 is azure (8), the output pixel is azure (8).
4. Else (if all corresponding input pixels are white), the output pixel is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input 15x5 grid into a 5x5 output grid based on layer overlay priority.
    
    Args:
        input_grid (list[list[int]]): A 15x5 grid represented as a list of lists.

    Returns:
        list[list[int]]: A 5x5 grid representing the transformed output.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Define dimensions
    output_height = 5
    output_width = 5
    
    # Initialize the output grid with white (0)
    output_array = np.zeros((output_height, output_width), dtype=int)
    
    # Extract the three layers
    layer1 = input_array[0:5, :]  # Rows 0-4 (Blue layer)
    layer2 = input_array[5:10, :] # Rows 5-9 (Azure layer)
    layer3 = input_array[10:15, :] # Rows 10-14 (Magenta layer)
    
    # Iterate through each pixel position in the 5x5 grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the colors from the corresponding positions in each layer
            color1 = layer1[r, c]
            color2 = layer2[r, c]
            color3 = layer3[r, c]
            
            # Apply the priority rule
            if color3 == 6:  # Check Layer 3 (Magenta) first
                output_array[r, c] = 6
            elif color1 == 1: # Then check Layer 1 (Blue)
                output_array[r, c] = 1
            elif color2 == 8: # Then check Layer 2 (Azure)
                output_array[r, c] = 8
            else: # Otherwise, it remains the default white (0)
                output_array[r, c] = 0
                
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
