"""
The input grid is rotated 90 degrees clockwise and then reflected vertically.
Pixel values are remapped from input to output.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise.
    rotated_np = np.rot90(input_np, k=-1)

    # Reflect the rotated grid vertically.
    flipped_np = np.flipud(rotated_np)
    
    # Create a mapping dictionary based on unique values in input and output.
    # Get unique values from original and combined flipped grids
    input_values = np.unique(input_np)
    output_values = np.unique(flipped_np)
    
    # Combine unique values and sort
    combined_values = np.unique(np.concatenate((input_values, output_values)))
    
    #create many-to-one dictionary map from input to output
    value_map = {}
    for i in range(len(combined_values)):
        for input_val in input_values:
            if input_val not in value_map:
                #try to find corresponding index in output
                if i < len(output_values):
                    output_val = output_values[i]
                else:
                    #no values left, so map to self
                    output_val = input_val
                value_map[input_val] = output_val
    

    # Apply the value mapping
    output_np = np.vectorize(value_map.get)(flipped_np)

    # Convert the NumPy array back to a list.
    output_grid = output_np.tolist()

    return output_grid