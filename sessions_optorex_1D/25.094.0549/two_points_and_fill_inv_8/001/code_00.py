import copy

def transform(input_sequence):
    """
    Modifies a sequence of integers by identifying contiguous runs of the same 
    non-zero digit. If a run has a length greater than 2, all elements 
    between the first and last element of the run are changed to 0. Runs of 
    length 1 or 2, and all zero elements, remain unchanged.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    
    # Initialize output_sequence as a copy of the input to preserve original zeros 
    # and runs that don't meet the length criteria.
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)
    i = 0
    
    # Iterate through the sequence to find runs of non-zero numbers
    while i < n:
        # Skip over zeros or start of a potential run
        if input_sequence[i] == 0:
            i += 1
            continue
        
        # Found a non-zero number, mark the start of a potential run
        start_index = i
        current_value = input_sequence[i]
        
        # Find the end of the contiguous run of the same non-zero number
        j = i + 1
        while j < n and input_sequence[j] == current_value:
            j += 1
            
        # The run ends at index j-1
        end_index = j - 1
        run_length = end_index - start_index + 1
        
        # Check if the run length is greater than 2
        if run_length > 2:
            # Modify the output sequence: set interior elements of the run to 0
            for k in range(start_index + 1, end_index):
                output_sequence[k] = 0
                
        # Move the main iterator past the processed run
        i = j 
        
    # Return the modified sequence
    return output_sequence
