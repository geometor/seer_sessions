import math

"""
Identifies the core repeating pattern of non-zero integers at the beginning of the input sequence. 
Then, repeats this core pattern cyclically to generate an output sequence of exactly 12 integers. 
Finally, formats the output sequence as a space-separated string.
"""

def extract_core_pattern(int_list):
    """
    Extracts the sequence of integers from the start until the first 0.
    """
    core_pattern = []
    for num in int_list:
        if num == 0:
            break
        core_pattern.append(num)
    return core_pattern

def generate_output_sequence(core_pattern, target_length):
    """
    Repeats the core pattern cyclically to build a sequence of the target length.
    """
    output_sequence = []
    if not core_pattern: # Handle case where input starts with 0 or is empty
        # Fill with a default value if needed, or handle as an error.
        # Based on examples, the pattern seems guaranteed. Let's assume it exists.
        # If no non-zero elements, maybe return 12 zeros? Let's stick to repeating the pattern.
        # If core_pattern is empty, this loop won't run, returning an empty list.
        # Let's refine based on expected behavior for edge cases if they arise.
        # For now, assume core_pattern is never empty based on examples.
        pass

    pattern_len = len(core_pattern)
    for i in range(target_length):
        output_sequence.append(core_pattern[i % pattern_len])
    return output_sequence

def format_sequence_to_string(int_list):
    """
    Converts a list of integers to a space-separated string.
    """
    return " ".join(map(str, int_list))

def transform(input_string):
    """
    Transforms the input string according to the described pattern repetition rule.

    Args:
        input_string: A string containing space-separated single-digit integers.

    Returns:
        A string containing 12 space-separated single-digit integers,
        formed by repeating the initial non-zero pattern from the input.
    """
    # 1. Read the input string and parse it into a list of integers.
    input_list_str = input_string.split()
    input_list_int = [int(s) for s in input_list_str]

    # 2. Identify the "core pattern".
    core_pattern = extract_core_pattern(input_list_int)

    # 3. Define the target length for the output.
    target_length = 12

    # 4. Generate the output sequence by repeating the core pattern.
    output_list_int = generate_output_sequence(core_pattern, target_length)

    # 5. Format the output list into a space-separated string.
    output_string = format_sequence_to_string(output_list_int)

    return output_string
