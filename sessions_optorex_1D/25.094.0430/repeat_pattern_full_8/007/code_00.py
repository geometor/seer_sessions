import numpy as np

"""
Transforms an input sequence (expected as a NumPy array of integers) by:
1. Identifying the 'core pattern' - the sequence of integers from the start 
   up to the first zero.
2. Repeating this 'core pattern' cyclically to generate a new sequence of 
   exactly 12 integers. If the core pattern is empty (input starts with 0), 
   the output sequence is 12 zeros.
3. Formatting the generated 12-integer sequence into a single string with 
   elements separated by spaces.
"""

def _flatten_and_convert_to_list(input_sequence):
    """
    Flattens a NumPy array and converts it to a list of Python integers.
    Handles both 1D and 2D (1xN) arrays.
    """
    # Flatten the array to handle both 1D and 2D (like [[...]]) inputs
    flat_array = np.array(input_sequence).flatten()
    # Convert numpy integers to standard Python integers
    return [int(x) for x in flat_array]

def _extract_core_pattern(int_list):
    """
    Extracts the sequence of integers from the start of a list until the first 0.
    """
    core_pattern = []
    for num in int_list:
        if num == 0:
            break
        core_pattern.append(num)
    return core_pattern

def _generate_output_sequence(core_pattern, target_length):
    """
    Repeats the core pattern cyclically to build a sequence of the target length.
    Returns a list of zeros if the core_pattern is empty.
    """
    output_sequence = []
    if not core_pattern:
        # Handle empty pattern case
        return [0] * target_length

    pattern_len = len(core_pattern)
    # Use modulo arithmetic to cycle through the pattern
    for i in range(target_length):
        output_sequence.append(core_pattern[i % pattern_len])
    return output_sequence

def _format_sequence_to_string(int_list):
    """
    Converts a list of integers to a space-separated string.
    """
    return " ".join(map(str, int_list))

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A NumPy array of integers (potentially 2D with one row).

    Returns:
        A string containing 12 space-separated integers based on the transformation rule.
    """
    
    # 1. Preprocess Input: Flatten the input NumPy array and convert to a Python list.
    input_list = _flatten_and_convert_to_list(input_sequence)

    # 2. Extract Core Pattern: Find the sequence before the first zero.
    core_pattern = _extract_core_pattern(input_list)

    # 3. Define Target Length: The output sequence must have 12 elements.
    target_length = 12

    # 4. Generate Output Sequence: Repeat the core pattern cyclically to the target length.
    #    Handles the case where the core pattern might be empty.
    output_list_int = _generate_output_sequence(core_pattern, target_length)

    # 5. Format Output: Convert the list of integers into a space-separated string.
    output_string = _format_sequence_to_string(output_list_int)

    # 6. Return Result: Return the final formatted string.
    return output_string