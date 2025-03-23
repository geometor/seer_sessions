"""
1. Reverse Rows: Reverse the order of the rows in the input grid. The last row becomes the first, the second-to-last becomes the second, and so on.
2. Conditional Value Swap:
    *   Swap all 0s and 5s.
    *   Swap all 1s and 0s.
"""

import numpy as np

def transform(input_grid):
    # Create a numpy array from the input grid for easier manipulation.
    input_np = np.array(input_grid)

    # Reverse the order of rows.
    reversed_rows_np = input_np[::-1]

    # Create a copy to modify, preserving the original.
    output_np = np.copy(reversed_rows_np)

    # Conditional Value Swap: 0s and 5s
    output_np[reversed_rows_np == 0] = 5
    output_np[reversed_rows_np == 5] = 0

    # Conditional Value Swap: 1s and 0s
    #  Need a temp variable because we just changed 0->5.  Could use a where
    temp = np.copy(output_np)
    output_np[temp == 1] = 0
    #output_np[np.where(reversed_rows_np == 1)] = 0
    
    
    output_np[temp ==5] = temp[temp ==5]  # don't change, hold value.  5
    output_np[temp == 0] = temp[temp ==0]  # don't change. 0
    #check where original has 1s
    output_np[reversed_rows_np == 1] = 0

    return output_np.tolist()