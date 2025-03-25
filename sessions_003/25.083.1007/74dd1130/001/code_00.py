"""
Reorders the columns of a 3x3 input grid based on a non-obvious rule 
(potentially relating to color values or positions) to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by reordering its columns.
    The exact reordering rule is determined through analysis of examples and 
    might be a permutation, a sort operation on color values, or a complex conditional reorder.
    """
    # Convert input to a NumPy array
    input_array = np.array(input_grid)
    
    # Initialize the output array
    output_array = np.empty_like(input_array)

    # The core logic is to figure out the mapping between input column indices and output
    # column indices.  We'll create a column_mapping list where column_mapping[i]
    # is the *input* column index that maps to output column i.  This is derived from
    # observing the test cases

    # Based on observing train 1-4 examples, this is the reordering:
    # input column 0 -> output column 0
    # input column 1 -> output column 2
    # input column 2 -> output column 1
    column_mapping = [0, 2, 1]

    # Apply the column reordering.
    for out_col_index, in_col_index in enumerate(column_mapping):
        output_array[:, out_col_index] = input_array[:, in_col_index]

    return output_array.tolist()