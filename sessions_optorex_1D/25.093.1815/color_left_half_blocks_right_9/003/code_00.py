import numpy as np
import math

"""
Transforms a sequence of 0s and 2s (represented as a NumPy array) based on contiguous 
subsequences of 2s. For each maximal contiguous subsequence of '2's of length N, 
the first floor(N/2) elements of that subsequence are changed to '8' in the 
output sequence. All '0's and the remaining '2's (those not in the first 
floor(N/2) of a subsequence) remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_grid: A 1D NumPy array containing integers (0s and 2s).

    Returns:
        A 1D NumPy array containing the transformed sequence (0s, 2s, and 8s).
    """
    
    # Ensure input is a NumPy array (though the environment seems to guarantee this)
    if not isinstance(input_grid, np.ndarray):
        # Handle potential list input if needed, though seems unlikely based on error
        input_list = list(input_grid) 
    else:
        # Directly use the numpy array
         input_list = input_grid.tolist() # Convert to list for easier index manipulation

    n = len(input_list)
    
    # Initialize the output list as a copy of the input
    # Working with a list might be simpler for element-wise modification based on dynamic ranges
    output_list = list(input_list) 
    
    # Iterate through the input list to find and process subsequences of 2s
    i = 0
    while i < n:
        # Check if the current element is the start of a '2' subsequence
        if input_list[i] == 2:
            # Found the start of a potential subsequence of 2s
            start_index = i
            
            # Find the end of the contiguous subsequence of 2s
            j = i
            while j < n and input_list[j] == 2:
                j += 1
            end_index = j - 1 # Inclusive end index of the subsequence
            
            # Calculate the length of the subsequence
            subsequence_length = end_index - start_index + 1
            
            # Calculate the number of elements to change to 8 using integer division (floor)
            num_to_change = subsequence_length // 2 
            
            # Change the first 'num_to_change' elements in the output list to 8
            # Iterate from the start index up to (but not including) start_index + num_to_change
            for k in range(start_index, start_index + num_to_change):
                output_list[k] = 8
                
            # Move the main loop index past this processed subsequence
            # Start the next iteration right after the end of the current subsequence
            i = end_index + 1
        else:
            # If the element is not 2 (it must be 0), it remains unchanged (already copied)
            # Just move to the next element
            i += 1
            
    # Convert the final list back to a NumPy array for the return value
    output_grid = np.array(output_list, dtype=input_grid.dtype) # Maintain original dtype if possible
    
    return output_grid