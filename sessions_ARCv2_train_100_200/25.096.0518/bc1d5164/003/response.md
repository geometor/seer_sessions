```python
import numpy as np # Although not strictly necessary for this logic, it's often useful for grid manipulation

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Creates a 3x3 output grid by sampling cell values from a 5x7 input grid 
    based on specific coordinate mappings, with one mapping being conditional.

    The fixed mappings are:
    - output[0][0] = input[0][0]
    - output[0][1] = input[0][1]
    - output[0][2] = input[0][6]
    - output[1][0] = input[1][0]
    - output[1][2] = input[1][6]
    - output[2][0] = input[4][0]
    - output[2][1] = input[4][5]
    - output[2][2] = input[4][6]
    
    The conditional mapping is for output[1][1]:
    - If input[3][1] is not 0, output[1][1] = input[3][1].
    - If input[3][1] is 0, output[1][1] = input[1][5].
    """

    # Initialize the output grid (3x3) with zeros
    output_grid = [[0 for _ in range(3)] for _ in range(3)]

    # Apply fixed mappings
    output_grid[0][0] = input_grid[0][0]
    output_grid[0][1] = input_grid[0][1]
    output_grid[0][2] = input_grid[0][6]
    output_grid[1][0] = input_grid[1][0]
    # output[1][1] is handled conditionally below
    output_grid[1][2] = input_grid[1][6]
    output_grid[2][0] = input_grid[4][0]
    output_grid[2][1] = input_grid[4][5]
    output_grid[2][2] = input_grid[4][6]

    # Apply conditional mapping for output[1][1]
    primary_value = input_grid[3][1]
    if primary_value != 0:
        output_grid[1][1] = primary_value
    else:
        # Use the secondary value if the primary is 0
        secondary_value = input_grid[1][5]
        output_grid[1][1] = secondary_value

    return output_grid
```