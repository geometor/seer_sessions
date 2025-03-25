"""
The transformation rearranges the pixels of the input grid to create the output
grid. The output grid is constructed column by column. Each column in the
output grid contains all the *unique* values that appeared *anywhere* in the
input grid. There does not seem to be any clear relationship to their order.
The number of times a color/value appears in an output column is the number of
times it appeared in the whole input.
"""

import numpy as np

def transform(input_grid):
    # Convert input to a NumPy array
    input_array = np.array(input_grid)
    
    # Initialize the output array with the same shape and type
    output_array = np.zeros_like(input_array)

    # Get all unique values from the input grid
    unique_values = np.unique(input_array)

    # Iterate through each column of the output grid
    for j in range(output_array.shape[1]):
      # get all values in the grid
      all_values = []
      for val in unique_values:
        for _ in range(np.count_nonzero(input_array == val)):
          all_values.append(val)


      # Fill the column.
      row_index = 0
      for i in range(len(all_values)):
          output_array[row_index, j] = all_values[i]
          row_index += 1
          if row_index >= output_array.shape[0]:
            row_index = 0 # reset row index if necessary


    return output_array.tolist()