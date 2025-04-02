"""
Identifies all 2x2 blocks of a single, non-white color within the input grid. 
Creates an output grid of the same dimensions, initially all white. 
Copies the pixels belonging to any identified 2x2 block from the input to the corresponding positions in the output grid. All other positions remain white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by preserving only the pixels that are part of a 2x2 block 
    of the same non-white color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier slicing and comparison
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid with the same dimensions as input_grid, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Iterate through each possible top-left corner (r, c) of a 2x2 block
    # We only need to iterate up to height-2 and width-2
    for r in range(height - 1):
        for c in range(width - 1):
            # Get the color of the top-left pixel of the potential 2x2 block
            top_left_color = input_array[r, c]

            # Check if the color is non-white (not 0)
            if top_left_color != 0:
                # Check if all four pixels in the 2x2 block have the same color
                if (input_array[r + 1, c] == top_left_color and
                    input_array[r, c + 1] == top_left_color and
                    input_array[r + 1, c + 1] == top_left_color):
                    
                    # If it's a solid non-white 2x2 block, copy these four pixels to the output grid
                    output_array[r, c] = top_left_color
                    output_array[r + 1, c] = top_left_color
                    output_array[r, c + 1] = top_left_color
                    output_array[r + 1, c + 1] = top_left_color

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
