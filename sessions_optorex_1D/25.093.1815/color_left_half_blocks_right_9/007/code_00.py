import numpy as np
import math

"""
Transforms a sequence of 0s and 2s (represented as a 1D NumPy array) based on 
contiguous subsequences of 2s. For each maximal contiguous subsequence of '2's 
of length N, the first floor(N/2) elements of that subsequence in the input 
are changed to '8' in the corresponding positions of the output sequence. 
All '0's and the remaining '2's (those not in the first floor(N/2) of a 
subsequence) remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_grid: A 1D NumPy array containing integers (0s and 2s).

    Returns:
        A 1D NumPy array containing the transformed sequence (0s, 2s, and 8s).
    """
    
    # Convert input NumPy array to a list for easier index manipulation and modification
    # Using a list allows straightforward modification of elements within identified ranges.
    input_list = input_grid.tolist() 
    n = len(input_list)
    
    # Initialize the output list as a direct copy of the input list. 
    # This ensures that 0s and any 2s not explicitly changed later are preserved.
    output_list = list(input_list) 
    
    # Iterate through the input list to find and process subsequences of 2s
    i = 0 # Main loop index
    while i < n:
        # Check if the current element is the start of a '2' subsequence
        if input_list[i] == 2:
            # Found the start of a potential subsequence of 2s
            start_index = i
            
            # Find the end of the contiguous subsequence of 2s by checking subsequent elements
            j = i # Inner loop index to find the end
            while j < n and input_list[j] == 2:
                j += 1
            # The loop stops when input_list[j] is not 2 or j reaches the end of the list.
            # The last index included in the '2' subsequence is j - 1.
            end_index = j - 1 
            
            # Calculate the length of the found subsequence
            subsequence_length = end_index - start_index + 1
            
            # Calculate the number of elements to change to 8 using integer division (floor)
            num_to_change = subsequence_length // 2 
            
            # Modify the output_list: Change the first 'num_to_change' elements 
            # of this subsequence within the output_list to 8.
            # Iterate from the start index up to (but not including) start_index + num_to_change
            for k in range(start_index, start_index + num_to_change):
                # Update the element in the output list
                output_list[k] = 8
                
            # Move the main loop index 'i' past this processed subsequence.
            # Start the next iteration right after the end of the current subsequence (which is index j).
            i = j
        else:
            # If the element at input_list[i] is not 2 (it must be 0), 
            # it remains unchanged in the output_list (due to the initial copy).
            # Just move to the next element in the input list.
            i += 1
            
    # Convert the final modified list back to a NumPy array for the return value.
    # Attempt to maintain the original dtype if it's integer-based, otherwise use int.
    output_dtype = input_grid.dtype if np.issubdtype(input_grid.dtype, np.integer) else int
    output_grid = np.array(output_list, dtype=output_dtype) 
    
    return output_grid