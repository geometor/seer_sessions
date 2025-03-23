```python
"""
The transformation rule involves transposing the input grid (swapping rows and columns), then reversing the order of the rows and finally reversing the order of the columns. This is equivalent to a 180-degree rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing, reversing rows, and reversing columns.
    
    Args:
        input_grid (list of lists): The input grid.
    
    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Transpose the array
    transposed_array = input_array.T

    # Reverse the order of rows
    rows_reversed = transposed_array[::-1]
    
    #reverse the order of the columns
    cols_reversed = rows_reversed[:, ::-1]

    # Convert back to list of lists
    output_grid = cols_reversed.tolist()

    return output_grid
```
