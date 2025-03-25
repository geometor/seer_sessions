```python
"""
The transformation rule is a one-to-one color substitution. Every pixel in the input grid is replaced with a corresponding color based on the following mapping:

*   Blue (1) becomes Gray (5).
*   Red (2) becomes Magenta (6).
*   Green (3) becomes Yellow (4).
*  Yellow(4) becomes Green(3)
*   Gray (5) becomes Blue (1).
* Magenta(6) becomes Red(2)
*   Orange (8) becomes Azure (9).
*   Azure (9) becomes Orange (8).

The output grid has the same dimensions as the input grid. The transformation operates element-wise; the position of a pixel within the grid doesn't affect its new value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replacing each pixel's value with a
    corresponding value from a predefined mapping.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Define the complete mapping dictionary.
    mapping = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        6: 2,
        9: 8,
        4: 3,
    }

    # Iterate through each pixel in the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Replace the pixel's value with its mapped value.
            original_value = output_grid[i, j]
            output_grid[i, j] = mapping.get(original_value, original_value) # Use .get() to handle potential missing keys

    return output_grid
```
