```python
"""
Iterate through the input 3x3 numpy array (grid) row by row, then column by column.
Collect all non-zero integer values encountered during this traversal.
Format the collected non-zero integers into a space-separated string.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> str:
    """
    Transforms a 3x3 numpy array into a space-separated string of its non-zero elements
    in row-major order.

    Args:
        input_grid: A 3x3 numpy array containing integers.

    Returns:
        A string containing the non-zero numbers from the grid, separated by spaces.
        Returns an empty string if the grid contains no non-zero numbers.
    """
    
    # Initialize an empty list to store the non-zero numbers found
    non_zero_numbers = []

    # Get the dimensions of the grid (assuming 3x3 based on examples, but flexible)
    rows, cols = input_grid.shape 

    # Iterate through each row of the input_grid
    for r in range(rows):
        # Iterate through each column within the current row
        for c in range(cols):
            # Get the value of the current cell
            value = input_grid[r, c]
            
            # Check if the value is not zero
            if value != 0:
                # If not zero, append it to the list
                non_zero_numbers.append(value)

    # Convert the collected numbers (which are integers) to strings
    output_strings = [str(num) for num in non_zero_numbers]
    
    # Join the string representations with a single space delimiter
    output_sequence = " ".join(output_strings)

    # Return the final space-separated string
    return output_sequence
```