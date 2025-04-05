import copy

def find_groups(sequence):
    """
    Identifies contiguous groups of identical non-zero numbers in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'value', 'start_index', 'end_index', and 'length'.
    """
    groups = []
    i = 0
    n = len(sequence)
    while i < n:
        if sequence[i] != 0:
            value = sequence[i]
            start_index = i
            # Find the end of the group
            j = i + 1
            while j < n and sequence[j] == value:
                j += 1
            end_index = j - 1
            length = end_index - start_index + 1
            groups.append({
                'value': value,
                'start_index': start_index,
                'end_index': end_index,
                'length': length
            })
            # Move the main index past this group
            i = end_index + 1
        else:
            # Move to the next element if it's zero
            i += 1
    return groups

def transform(input_sequence):
    """
    Transforms the input sequence based on identified groups of non-zero numbers.
    If a contiguous group of the same non-zero number has a length greater than 2,
    only the first and last elements of the group are kept, and the elements
    in between are replaced with 0. Groups of length 2 or less remain unchanged.
    Zeros outside of these groups also remain unchanged.
    """
    
    # Initialize the output sequence as a copy of the input sequence.
    # Using list() creates a shallow copy, which is sufficient here as elements are integers.
    output_sequence = list(input_sequence) 
    
    # Iterate through the input sequence to identify all contiguous groups 
    # of identical non-zero numbers.
    groups = find_groups(input_sequence)
    
    # For each identified group:
    for group in groups:
        # Check if the length of the group is greater than 2.
        if group['length'] > 2:
            # If the length is greater than 2, then iterate through the indices 
            # of the output sequence starting from the index *after* the group's 
            # start index up to the index *before* the group's end index.
            # Set the value at each of these indices in the output sequence to 0.
            # range(start, stop) goes up to stop-1, so range(start+1, end) is correct.
            for i in range(group['start_index'] + 1, group['end_index']):
                output_sequence[i] = 0
                
    # Return the final output sequence.
    return output_sequence
