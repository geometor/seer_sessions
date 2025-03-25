"""
Rearranges the pixels within the input grid to produce the output grid. 
The transformation sorts each column independently:
- Column 1: Ascending order.
- Column 2: Descending order.
- Column 3: Descending order.
"""

import numpy as np

def transform(input_grid):
    # Convert input to a NumPy array
    input_array = np.array(input_grid)
    
    # Initialize the output array
    output_array = np.empty_like(input_array)

    # Sort the first column in ascending order
    output_array[:, 0] = np.sort(input_array[:, 0])

    # Sort the second and third columns in descending order
    output_array[:, 1] = np.sort(input_array[:, 1])[::-1]
    output_array[:, 2] = np.sort(input_array[:, 2])[::-1]

    return output_array.tolist()