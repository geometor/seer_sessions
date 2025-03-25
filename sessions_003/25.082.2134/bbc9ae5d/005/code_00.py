"""
The transformation takes a 1D input array and generates a 2D output array. The first row of the output is identical to the input. Subsequent rows are created by iteratively replacing zeros in the input with the last non-zero value, up to the index of the last non-zero value. The number of replaced zeros increases by one in each new row.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # 1. Find Last Non-Zero Element's Index
    last_non_zero_index = -1
    for i, val in enumerate(input_array):
        if val != 0:
            last_non_zero_index = i

    # 2. Determine Output Dimensions
    output_height = last_non_zero_index + 1
    output_width = len(input_array)
    
    # Find last non-zero value
    if last_non_zero_index >=0:
        last_non_zero_value = input_array[last_non_zero_index]
    else:
       last_non_zero_value = 0

    # 3. Initialize Output Grid
    output_array = np.zeros((output_height, output_width), dtype=int)

    # 4. First Row: Identical to Input
    output_array[0, :] = input_array

    # 5. Subsequent Rows (Expansion)
    for i in range(1, output_height):
        output_array[i,:] = input_array #copy first row
        
        zeros_replaced = 0
        for j in range(len(input_array)):
          if zeros_replaced < i and j <= last_non_zero_index:  #important to check we don't go over the original last_non_zero_index
            if output_array[i,j] == 0:
              output_array[i,j] = last_non_zero_value
              zeros_replaced +=1
          else:
              break  # Stop after replacing the required number of zeros, or we have reached to the index of last non zero element


    return output_array.tolist()