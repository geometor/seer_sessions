"""
Rotate the input grid 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise.
    """
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Rotate the array 90 degrees clockwise
    output_array = np.rot90(input_array, k=-1)
            
    return output_array.tolist()