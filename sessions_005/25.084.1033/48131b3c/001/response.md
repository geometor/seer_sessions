```python
import numpy as np

def transform(input_grid):
    """
    Tiles the input grid in a 2x2 arrangement to create the output grid.
    The output grid has double the height and double the width of the input grid.
    The content of the output grid is formed by repeating the input grid pattern
    twice horizontally and twice vertically.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Use np.tile to repeat the input grid 2 times vertically (axis 0)
    # and 2 times horizontally (axis 1)
    output_np = np.tile(input_np, (2, 2))

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```