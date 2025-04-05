import numpy as np # Using numpy for potential array handling, although list ops are sufficient

"""
Transformation Rule Natural Language Program:

1.  Create a new sequence, `output_sequence`, as a modifiable copy of the `input_sequence`.
2.  Determine the `key_digit` by taking the integer value of the first element (at index 0) of the original `input_sequence`.
3.  Create an empty list named `trigger_indices` to store the locations of the `key_digit` that will trigger modifications.
4.  Iterate through the original `input_sequence` using an index `i`, starting from `i = 3` and ending at `i = length - 2` (inclusive). This range ensures that accessing `i-1` and `i+1` during modification will stay within the sequence bounds.
5.  Inside this loop, check if the element `input_sequence[i]` is equal to the `key_digit`.
6.  If they are equal, add the current index `i` to the `trigger_indices` list.
7.  After checking all elements in the specified range, iterate through the `trigger_indices` list.
8.  For each index `i` found in `trigger_indices`:
    a.  Modify the `output_sequence` by setting the value at index `i-1` to the `key_digit`.
    b.  Modify the `output_sequence` by setting the value at index `i` to the `key_digit`.
    c.  Modify the `output_sequence` by setting the value at index `i+1` to the `key_digit`.
9.  Return the fully modified `output_sequence`.
"""

def _find_trigger_indices(sequence: list, key_digit: int) -> list[int]:
    """
    Helper function to find indices i where sequence[i] == key_digit.
    
    Scans the sequence from index 3 up to length - 2.
    """
    trigger_indices = []
    # Sequence needs at least 4 elements for index 3 to exist and index len-2 >= 3.
    if len(sequence) < 4:
        return []
        
    scan_end_index = len(sequence) - 2 # Inclusive end index for scanning
    for i in range(3, scan_end_index + 1):
        if sequence[i] == key_digit:
            trigger_indices.append(i)
    return trigger_indices

def _apply_modifications(sequence: list, key_digit: int, indices: list[int]) -> list[int]:
    """
    Helper function to apply the triplet replacement rule at the specified indices.
    Modifies the input sequence directly.
    """
    for i in indices:
        # Bounds should be guaranteed by _find_trigger_indices, but check for safety
        if i - 1 >= 0 and i + 1 < len(sequence):
            sequence[i - 1] = key_digit
            sequence[i] = key_digit
            sequence[i + 1] = key_digit
    return sequence # Return the modified sequence

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Identifies a key digit from the start, finds its occurrences later
    in the sequence (from index 3 to length-2), and replaces the element 
    and its immediate neighbors in a copy of the sequence with the key digit.
    """
    
    # Ensure input is treated as a standard Python list for processing
    # Store original type to return the same type.
    original_type = type(input_sequence)
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assuming it's already list-like (list, tuple)
        input_list = list(input_sequence) 
        
    # Handle edge case: sequence too short for the rule to apply meaningfully
    # Needs at least 3 elements for key digit, and 4 for the scan range to be non-empty.
    if len(input_list) < 4: 
        # Return in original format
        return original_type(input_list)

    # --- Workflow ---
    # 1. Create a modifiable copy of the input sequence.
    output_list = list(input_list)

    # 2. Identify the key_digit from the original input.
    key_digit = input_list[0]

    # 3. Find trigger indices by scanning the *original* input_list using a helper function.
    trigger_indices = _find_trigger_indices(input_list, key_digit)

    # 4. Apply modifications to the output_list based on trigger indices using a helper function.
    #    The helper modifies the list in place.
    output_list = _apply_modifications(output_list, key_digit, trigger_indices)

    # 5. Return the modified sequence, converting back to original type if necessary.
    if original_type is np.ndarray:
        return np.array(output_list)
    else:
        # Return as the original type (e.g., list, or potentially tuple if input was tuple)
        # Using list() ensures it's at least a list if the original wasn't np.ndarray
        return list(output_list) 