```python
"""
Iterate through each cell of the input grid row by row, top to bottom, and left to right within each row. 
Collect any non-zero integer encountered during this scan. 
Format the collected non-zero integers into a single string, separated by spaces.
"""

import numpy as np 

# No external libraries needed beyond standard types for this specific task, 
# but numpy could be useful for more complex grid operations if the task evolved.

def transform(input_grid: list[list[int]]) -> str:
    """
    Extracts non-zero elements from a grid in row-major order and returns them as a space-separated string.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A string containing the non-zero elements from the grid, 
        in row-major order, separated by spaces.
    """
    
    # Initialize an empty list to store the non-zero numbers found
    non_zero_elements = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Iterate through each element (cell) in the current row
        for element in row:
            # Check if the element is not zero
            if element != 0:
                # If it's non-zero, convert it to a string and add it to our list
                non_zero_elements.append(str(element))

    # Join the collected non-zero elements into a single string with spaces in between
    output_str = " ".join(non_zero_elements)

    # Return the final string
    return output_str

```