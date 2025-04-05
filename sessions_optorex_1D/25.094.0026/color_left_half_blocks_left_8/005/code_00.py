import numpy as np
import math

"""
Transforms a 2D NumPy grid (expected shape (1, N)) containing digits 0 and 2.
It identifies contiguous runs of the digit '2' within the first row. 
For each run of length L, the last floor(L/2) elements of that run 
are changed from 2 to 8. The digit 0 acts as a delimiter and remains unchanged.
The output grid retains the original shape.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array, typically shape (1, N), containing 0s and 2s.

    Returns:
        A 2D NumPy array with the same shape as input_grid, where runs of 2s
        in the first row have been modified according to the rule.
    """
    # Ensure input is at least 1D and not empty
    if input_grid.ndim == 0 or input_grid.size == 0:
        return np.copy(input_grid) # Return copy for empty or scalar

    # Handle potential 1D input by reshaping, or just select first row if 2D
    if input_grid.ndim == 1:
        input_row = input_grid
    elif input_grid.ndim >= 2:
         # 1. Extract the first row of the input grid as the primary 1D sequence.
        input_row = input_grid[0]
    else: # Should not happen with numpy arrays, but defensive
        return np.copy(input_grid)


    # 2. Create a copy of this 1D sequence to store the output modifications.
    output_row = np.copy(input_row)
    n = len(output_row)
    
    # 3. Initialize an index pointer i to 0.
    i = 0

    # 4. Iterate through the copied 1D sequence using the pointer i:
    while i < n:
        # a. If the element at index i is a '2':
        if output_row[i] == 2:
            # i. Mark the current index i as the start of a potential run.
            run_start_index = i
            # ii. Initialize run_length.
            run_length = 0
            
            # iii. Continue advancing i and incrementing run_length for the '2' run.
            while i < n and output_row[i] == 2:
                run_length += 1
                i += 1 # Move pointer along the run
            
            # iv. Calculate the number of elements to change.
            num_to_change = run_length // 2 # Integer division for floor(L/2)
            
            # v. If num_to_change is greater than 0:
            if num_to_change > 0:
                # 1. Calculate the starting index for modification.
                modify_start_index = run_start_index + (run_length - num_to_change)
                
                # 2. Change the required number of '2's to '8's at the end of the run using slicing.
                # The end index for slicing is run_start_index + run_length
                modify_end_index = run_start_index + run_length
                output_row[modify_start_index:modify_end_index] = 8
                
            # vi. The pointer 'i' is already positioned after the processed run.
            # The loop will continue from the element after the run.
            
        # b. If the element at index i is not '2', simply increment i.
        else:
            i += 1

    # 5. Reconstruct the output grid to match the original input grid's shape.
    # If the original was 1D, return 1D. If 2D or more, reconstruct similarly.
    if input_grid.ndim == 1:
         output_grid = output_row
    else: # Assumes original was 2D (1,N) or similar structure we need to mimic
        # Create a new grid with the original shape, placing the modified row
        output_grid = np.copy(input_grid) # Start with a copy to preserve other dimensions/rows if any
        output_grid[0] = output_row     # Replace the first row with the modified one

    # 6. Return the resulting grid.
    return output_grid