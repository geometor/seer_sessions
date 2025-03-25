"""
The transformation takes a 1D input array and generates a 2D output array. The first row of the output is identical to the input. Subsequent rows expand by repeating the last non-zero element of the input row one additional time per row, replacing zeros. The output height is one plus the number of non-zero elements in the input, and the output width matches the input width.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # 1. Identify Last Non-Zero Element
    non_zero_elements = input_array[input_array != 0]
    last_non_zero = non_zero_elements[-1] if len(non_zero_elements) >0 else 0
    n = len(non_zero_elements)

    # 2. Determine Output Dimensions
    output_height = n + 1
    output_width = len(input_array)
    
    # 3. Initialize Output Grid
    output_array = np.zeros((output_height, output_width), dtype=int)

    # 4. First Row: Identical to Input
    output_array[0, :] = input_array

    # 5. Subsequent Rows (Expansion)
    for i in range(1, output_height):
        output_array[i,:] = input_array #copy first row
        for j in range(i):
            # find the j-th zero in the input
            zeros = np.where(input_array == 0)[0]
            if j < len(zeros):
               idx_to_replace = zeros[j]
               output_array[i,idx_to_replace] = last_non_zero #replace with last non-zero
            else:
              break

    return output_array.tolist()