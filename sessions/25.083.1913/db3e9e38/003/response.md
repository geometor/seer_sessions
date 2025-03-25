```python
"""
1.  **Identify Columns:** Find all columns in the input grid that contain orange (7) pixels.
2.  **Iterate through Columns:** For each identified column:
    1.  **Count Orange Pixels:** Determine the number of orange pixels present in the current column.
    2.  **Prepend:**  At the top of this column, prepend *n* "8 7" pairs, where *n* is the number of orange pixels originally in that column.
    3. **Shift:** shift any existing pixels (including original 7 pixels) down by 2n.
    4. **Maintain Shape:** keep all other cells unchanged, the input and output grids are the same shape.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find columns containing orange (7) pixels
    orange_cols = np.unique(np.where(input_grid == 7)[1])

    # Iterate through identified columns
    for col in orange_cols:
        # Count orange pixels in the current column
        orange_count = np.count_nonzero(input_grid[:, col] == 7)

        # Create new elements to prepend ("8 7" pairs)
        new_elements = np.array([[8, 7]] * orange_count).flatten()

        # Extract the original column
        original_column = input_grid[:, col]

        # Shift original column down by 2*orange_count positions.  Create
        # space for this by pre-padding with zeros
        shifted_column = np.concatenate((np.zeros(2*orange_count), original_column))

        # Place new elements at the top
        shifted_column[:2*orange_count] = new_elements

        #resize to original column length
        shifted_column = shifted_column[:rows]

        # Update the output grid
        output_grid[:, col] = shifted_column

    return output_grid
```