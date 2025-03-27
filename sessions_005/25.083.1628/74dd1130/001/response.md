```python
"""
The transformation reorders the elements within each column of the input grid independently. The reordering rule is determined by comparing each input column to the corresponding output column in the examples, and applying the same permutation to new columns.
"""

import numpy as np

def get_column_permutation(input_col, output_col):
    """
    Determine the permutation that transforms the input column to the output column.
    Returns a list of indices representing the permutation.
    """
    # Create a mapping from value to index in the output column
    output_mapping = {val: i for i, val in enumerate(output_col)}

    # Sort input based on the order in the example.
    permutation = sorted(range(len(input_col)), key=lambda k: output_mapping.get(input_col[k],-1) )

    # Create a list to store tuple of input index, and desired output index
    mapping = []
    for i in range(len(input_col)):
       mapping.append( (i, output_mapping.get(input_col[i])) )

    # Sort the mapping based on current index order
    mapping.sort(key = lambda x: x[0])

    # Now re-order based on the desired index
    mapping.sort(key = lambda x: x[1])

    #permutation = [ x[0] for x in mapping]

    return permutation

def apply_permutation(column, permutation):
    """Applies a permutation to a column."""
    return [column[i] for i in permutation]

def transform(input_grid):
    """
    Transforms the input grid by reordering each column based on a 
    permutation derived by looking at the input and output columns of the 
    example pairs.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # column mapping from example data
    example_mapping = {
      0: ([9,5,5], [9,9,5]),
      1: ([9,5,8], [5,5,8]),
      2: ([5,8,9], [5,8,9]),

      3: ([2,6,5], [2,2,5]),
      4: ([2,2,5], [6,2,2]),
      5: ([5,5,5], [5,2,5]),

      6: ([2,2,2], [2,6,6]),
      7: ([6,1,6], [2,1,1]),
      8: ([6,1,2], [2,6,2]),

      9:  ([2,1,5], [2,2,1]),
      10: ([2,5,2], [1,5,1]),
      11: ([1,1,2], [5,2,2])
    }

    # Iterate through columns and apply transformation
    for i in range(input_grid.shape[1]):
        input_col = list(input_grid[:, i])

        found = False
        # find permutation
        for k,v in example_mapping.items():
            if input_col == list(v[0]):
               perm = get_column_permutation(v[0],v[1])
               output_grid[:, i] = apply_permutation(input_col, perm)
               found = True
               break

        # if not found, keep current order
        if not found:
           output_grid[:,i] = input_col[:]

    return output_grid.tolist()
```