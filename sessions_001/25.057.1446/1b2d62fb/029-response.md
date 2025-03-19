# 1b2d62fb • 029 • refine_coder

---
```python
"""
1.  **Identify Blue Columns:** Find all columns in the input grid that contain at least one blue (value 1) pixel.
2. **Determine Output Column**: Select the *first* column index where blue appears.
3.  **Create Output Grid:** Create an output grid with 3 columns and the same number of rows as the input grid.
4. **Transform Column:** In the output grid, replace all pixels in the selected column with azure (value 8).
5. **Other Pixels**: Fill remaining cells in output grid with black (value 0).
"""

import numpy as np

def get_blue_columns(grid):
    # Find columns with '1' (blue)
    return np.where(np.any(grid == 1, axis=0))[0]

def transform(input_grid):
    # Identify Blue Columns
    blue_columns = get_blue_columns(input_grid)

    # Determine Output Dimensions and Column
    output_height = input_grid.shape[0]
    output_width = 3
    
    # Handle cases with no blue columns
    if len(blue_columns) == 0:
        output_grid = np.zeros((output_height, output_width), dtype=int)
        return output_grid

    output_column_index = blue_columns[0]  #select first (leftmost)
    
    # Create Output Grid
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Calculate position for the azure column in the output (centered)
    output_azure_column = 1 # center column

    # Transform Column: set output column to azure
    output_grid[:, output_azure_column] = 8

    return output_grid
```
