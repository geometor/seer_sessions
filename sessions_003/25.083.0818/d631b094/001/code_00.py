"""
Extracts and repeats non-zero values from a 3x3 input grid to create an output grid. The output grid is a single row where each non-zero value is repeated as many times as it appears in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Find all non-zero elements
    non_zero_elements = input_array[input_array != 0]
    
    # Count occurrences of each non-zero element
    unique_elements, counts = np.unique(non_zero_elements, return_counts=True)

    # build result
    result = []
    for i in range(len(unique_elements)):
      for j in range(counts[i]):
        result.append(unique_elements[i])

    # Reshape output to a single row
    output_grid = np.array(result)
    
    return output_grid.tolist()