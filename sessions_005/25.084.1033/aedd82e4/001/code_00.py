"""
Iterate through each pixel of the input grid. If a pixel is 'red' (2), check its
orthogonal neighbors (up, down, left, right). If all existing orthogonal
neighbors are 'white' (0), change the color of that pixel to 'blue' (1) in the
output grid. Otherwise, keep the original color. 'white' pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the rule:
    Change 'red' (2) pixels to 'blue' (1) if they have no 'red' orthogonal neighbors.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Create a copy of the input array to modify, this will be the output
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is 'red' (2)
            if input_array[r, c] == 2:
                # Assume the pixel is isolated initially
                is_isolated = True
                # Define orthogonal neighbor offsets
                neighbors_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                
                # Check each orthogonal neighbor
                for dr, dc in neighbors_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # If a neighbor is 'red' (2), the current pixel is not isolated
                        if input_array[nr, nc] == 2:
                            is_isolated = False
                            break # No need to check other neighbors
                
                # If the pixel is isolated (all orthogonal neighbors are not 'red')
                if is_isolated:
                    # Change the corresponding pixel in the output array to 'blue' (1)
                    output_array[r, c] = 1
                    
    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
