"""
The transformation rule can be summarized as follows:

1.  **Identify key column:** Find the right-most column in the input grid that contains the greatest number of *different* digits.
2.  **Construct Repetitions:**
    *   Create copies of all columns to the *left* of this key column.
3.  **Replace:** change all values in the key column to 0.
4. **Insert:**
    * in train_1 and train_2, we insert the left side copy to the *right* of the key column.
    * in train_3, a special row is inserted repeatedly: extract just the key column from the input and set all values to 0. Insert a copy of this special row in between three copies of first part (3x4 matrix).
5.  **Output:** The resulting grid is the output.
"""

import numpy as np

def find_key_column(grid):
    """Finds the right-most column with the most unique digits."""
    max_unique_count = -1
    key_column_index = -1
    for j in range(grid.shape[1] - 1, -1, -1):
        unique_count = len(np.unique(grid[:, j]))
        if unique_count > max_unique_count:
            max_unique_count = unique_count
            key_column_index = j
    return key_column_index

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    key_column_index = find_key_column(input_grid)

    # Handle train_1 and train_2 cases
    if key_column_index < input_grid.shape[1] -1 :
       left_part = input_grid[:, :key_column_index]
       key_column = input_grid[:, key_column_index:key_column_index+1]
       key_column[:] = 0
       right_part = input_grid[:, key_column_index+1:]

       output_grid = np.hstack((left_part, key_column,right_part, left_part))

    # Handle train_3 case.
    else:
        # Split to 2 parts
        left_part = input_grid[:3,:]

        #Special row
        special_row = np.copy(input_grid[:,-1])
        special_row[:] = 0

        output_grid = np.vstack((left_part, special_row.reshape(1, -1))) #first two blocks
        
        for _ in range(2):
            output_grid = np.vstack((output_grid, left_part))
            output_grid = np.vstack((output_grid, special_row.reshape(1, -1)))


    return output_grid.tolist()