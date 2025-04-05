import math

"""
Transforms a sequence of 0s and 2s based on contiguous subsequences of 2s.
For each maximal contiguous subsequence of '2's of length N, the first floor(N/2) 
elements of that subsequence are changed to '8' in the output sequence. 
All '0's and the remaining '2's (those not in the first floor(N/2) of a subsequence) 
remain unchanged.
"""

def transform(input_sequence_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_sequence_str: A string containing space-separated integers (0s and 2s).

    Returns:
        A string containing the transformed sequence, space-separated.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_sequence_str.split()]
    n = len(input_list)
    
    # Initialize the output list as a copy of the input
    output_list = list(input_list)
    
    # Iterate through the input list to find and process subsequences of 2s
    i = 0
    while i < n:
        if input_list[i] == 2:
            # Found the start of a potential subsequence of 2s
            start_index = i
            # Find the end of the subsequence
            j = i
            while j < n and input_list[j] == 2:
                j += 1
            end_index = j - 1 # Inclusive end index
            
            # Calculate the length of the subsequence
            subsequence_length = end_index - start_index + 1
            
            # Calculate the number of elements to change to 8
            num_to_change = subsequence_length // 2 # Integer division handles floor
            
            # Change the first 'num_to_change' elements in the output list to 8
            for k in range(start_index, start_index + num_to_change):
                output_list[k] = 8
                
            # Move the main loop index past this processed subsequence
            i = end_index + 1
        else:
            # If the element is not 2 (it must be 0), just move to the next element
            i += 1
            
    # Convert the output list back to a space-separated string
    output_sequence_str = " ".join(map(str, output_list))
    
    return output_sequence_str
