"""
Transforms a 1x5 input grid into a square output grid by replicating non-zero elements diagonally.
The output grid's size is determined by the number of non-zero digits and number of input elements.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Count Non-Zeros
    non_zero_count = np.count_nonzero(input_array)
    
    #Calculate total shifts
    total_shifts = 0
    
    non_zero_indices = []
    for i in range(len(input_array[0])):
        if input_array[0][i] != 0:
            non_zero_indices.append(i)

    for i in range(len(non_zero_indices)):
        total_shifts += len(input_array[0]) - non_zero_indices[i] -1


    # Determine Output Size: max of (input length and sum of shifts)
    output_size = max(total_shifts + non_zero_count, len(input_array[0]))
    
    # Create Output Grid (initialized with zeros)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Iterate through the input array
    
    for i in range(len(input_array[0])):
        current_element = input_array[0][i]

        if current_element != 0:
          row_index = 0
          
          for k in range(i):
              if input_array[0][k] == 0:
                row_index +=1

          
          output_grid[row_index][i] = current_element
          shift = 1

          for j in range(i + 1, len(input_array[0])): # iterate through the right side from current element index
            if input_array[0][j] == 0:
                output_grid[row_index + shift][i + shift] = current_element
                shift += 1

    return output_grid