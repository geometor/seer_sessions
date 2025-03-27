```python
"""
The transformation rule extracts the two rightmost columns of the input grid and then applies a mapping to create the output columns. The mapping is dependent on the original pixel value and its column (within the extracted two columns).
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the two rightmost columns, then remaps values based on column and value.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid)
    height, width = input_array.shape
    last_two_cols = input_array[:, width-2:width]
    output_array = np.zeros_like(last_two_cols)

    # Mapping rules (combined and generalized)
    mapping_rules = {
        0: {0: 0, 1: 0},
        2: {0: 4, 1: 2},
        3: {0: 3, 1: 3},
        4: {0: 4, 1: 4}, #added from example 1
        5: {0: 5, 1: 5}, # added from example 1
        6: {0: 8, 1:8}, #added from example 1
        7: {0: 3, 1:9},
        8: {0: 6, 1: 8},
        9: {0: 9, 1: 7},
    }

    # added mapping for example 2, first column 8 -> 3 second ->8
    mapping_rules[8] = {0 : 3, 1: 8}
      # added mapping for first column 3-> 8, second stays 3
    mapping_rules[3] = {0 : 8, 1: 3}


    for row_index in range(height):
        for col_index in range(2):
            original_value = last_two_cols[row_index, col_index]
            # Apply mapping based on original value and column index (0 or 1)
            if original_value in mapping_rules:
                output_array[row_index, col_index] = mapping_rules[original_value][col_index]

            else: # default if no mapping
                output_array[row_index, col_index] = original_value
    return output_array.tolist()
```