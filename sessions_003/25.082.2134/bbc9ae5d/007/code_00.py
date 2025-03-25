"""
The transformation takes a 1D input array and generates a 2D output array. The first row of the output is identical to the input. Subsequent rows are created by iteratively replacing zeros in the input with the last non-zero value. The number of replaced zeros increases by one in each new row, and the number of replaced zeros is equal to the row index (starting from 1).
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # 1. Find Last Non-Zero Element's Index and Value
    last_non_zero_index = -1
    for i, val in enumerate(input_array):
        if val != 0:
            last_non_zero_index = i

    if last_non_zero_index >=0:
        last_non_zero_value = input_array[last_non_zero_index]
    else:
       last_non_zero_value = 0

    # 2. Determine Output Dimensions
    #Correcting the output_height calculation
    output_height = 0
    for i in range(len(input_array)):
      temp_input_array = input_array.copy()
      zeros_count = 0
      for j in range(len(temp_input_array)):
        if temp_input_array[j] == 0:
          zeros_count += 1
        if zeros_count > i:
            break

      if zeros_count > i:
        output_height +=1
    output_width = len(input_array)

    # 3. Initialize Output Grid
    output_array = np.zeros((output_height, output_width), dtype=int)

    # 4. First Row: Identical to Input
    if output_height>0:
        output_array[0, :] = input_array

    # 5. Subsequent Rows (Expansion)
    for i in range(1, output_height):
        output_array[i,:] = input_array.copy() #copy first row
        
        zeros_replaced = 0
        for j in range(len(input_array)):
          if zeros_replaced < i:  # Replace zeros up to the row number
            if output_array[i,j] == 0:
              output_array[i,j] = last_non_zero_value
              zeros_replaced +=1


    return output_array.tolist()