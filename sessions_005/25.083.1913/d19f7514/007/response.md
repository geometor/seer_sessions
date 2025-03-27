```python
"""
1. Divide Input: Divide the input grid vertically into N equal parts, where N is the ratio of the input grid's height to the output grid's height.
2. Select Top Portion: Keep only the top portion (first 1/Nth) of the divided grid.
3. Filter Colors: Maintain only the colors that are present in the example output grid. Set all other colors in the selected portion to black (color 0).
"""

import numpy as np

def transform(input_grid, expected_output):  # Added expected_output
    """Transforms the input grid according to the described rule."""

    input_height = input_grid.shape[0]
    output_height = expected_output.shape[0]
    
    if input_height % output_height != 0:
        raise ValueError("Input height must be a multiple of output height.")

    n_parts = input_height // output_height
    top_portion_start = 0
    top_portion_end = input_height // n_parts
    
    # Select the top portion
    output_grid = input_grid[top_portion_start:top_portion_end, :].copy()

    # Get the unique colors present in the expected output.
    allowed_colors = np.unique(expected_output)

    # Create a mask to filter colors not present in the expected output.
    mask = np.isin(output_grid, allowed_colors)

    # Set pixels with disallowed colors to 0 (black).
    output_grid[~mask] = 0

    return output_grid
```
