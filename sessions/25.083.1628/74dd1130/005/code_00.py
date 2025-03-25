"""
The transformation rule reorders each column of the input grid independently. The reordering is determined by comparing the input column to the corresponding output column in the provided training examples. The input column is permuted such that:

1.  **Output Value Priority:** If an element from the input column exists in the corresponding output column, its new position is determined by the *first* index at which that element appears in the output column.

2.  **Missing Value Handling:** If an element from the input column does *not* exist in the output column, it is placed *after* all elements that *do* exist in the output column.

3.  **Original Order Preservation:** If multiple elements in the input column map to the same position in the output column (or are both missing), their original relative order within the input column is preserved.

4.  **Example Usage:** The permutation is derived from *one* of the provided examples. We select the first example that gives a correct mapping, which is defined as an example where the column length is compatible (input column exists) *and* the permutation applied to the example input column matches the example output column.

5.  **Incomplete Examples:** If an example input is incomplete (it does not have enough columns), the original order of the input column is kept (no transformation).
"""

import numpy as np

def get_column_permutation(input_col, output_col):
    """
    Determine the permutation that transforms the input column to the output column.
    Returns a list of indices representing the permutation.
    """
    # Create a mapping from output value to its first index
    output_mapping = {}
    for i, val in enumerate(output_col):
        if val not in output_mapping:
            output_mapping[val] = i

    # Sort input based on the order in the output, preserving original order for ties.
    def sorting_key(index):
      input_value = input_col[index]
      if input_value in output_mapping:
        return (0, output_mapping[input_value], index) # exists in output, use first output index, use input position
      return (1,index) # not exist, put it at last, use input position

    permutation = sorted(range(len(input_col)), key=sorting_key)

    return permutation

def apply_permutation(column, permutation):
    """Applies a permutation to a column."""
    return [column[i] for i in permutation]

def transform(input_grid, examples):
    """
    Transforms the input grid by reordering each column based on a 
    permutation derived by looking at the input and output columns of the 
    example pairs.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Iterate through columns and apply transformation
    for i in range(input_grid.shape[1]):
        input_col = list(input_grid[:, i])

        # find permutation from all examples
        for example in examples:
           input_ex = np.array(example["input"])
           if i < input_ex.shape[1]:
              input_col_ex = [row[i] for row in example["input"]]
              output_col_ex = [row[i] for row in example["output"]]
              perm = get_column_permutation(input_col_ex, output_col_ex)
              if apply_permutation(input_col_ex, perm) == output_col_ex:
                # found good permutation, use it
                output_grid[:, i] = apply_permutation(input_col, perm)
                break
           else:
             # keep current order
             output_grid[:,i] = input_col[:]


    return output_grid.tolist()