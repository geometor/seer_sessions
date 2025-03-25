"""
The input grid consists of two rows of equal length. The output grid is created by interleaving the digits from the two input rows. The first output row alternates digits starting with the first input row, and the second output row alternates digits starting with the second input row.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Get the two rows from the input array
    row1 = input_array[0, :]
    row2 = input_array[1, :]

    # Initialize the output array with the same dimensions as the input
    output_array = np.zeros_like(input_array)

    # Interleave digits for the first output row, starting with row1
    output_array[0, ::2] = row1[::2]
    output_array[0, 1::2] = row2[1::2]

     # Adjust for cases where row1 and row2 are not composed of entirely identical numbers
    if len(np.unique(row1)) > 1:
      output_array[0, 1::2] = row2[:len(row1)//2 + (len(row1)%2) ]
      output_array[0, ::2] = row1[:len(row1)//2+ (len(row1)%2)]


    # Interleave digits for the second output row, starting with row2
    output_array[1, ::2] = row2[::2]
    output_array[1, 1::2] = row1[1::2]

    #Adjust for cases where row1 and row2 are not composed of entirely identical numbers
    if len(np.unique(row2)) > 1:
        output_array[1, ::2] = row2[:len(row2)//2+(len(row2)%2)]
        output_array[1, 1::2] = row1[:len(row2)//2+(len(row2)%2)]

    # Convert the output NumPy array back to a list
    output_grid = output_array.tolist()

    return output_grid