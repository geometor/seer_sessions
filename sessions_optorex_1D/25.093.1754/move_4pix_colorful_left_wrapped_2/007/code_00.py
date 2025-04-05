import typing

"""
Transforms an input string containing 12 space-separated integers by first parsing 
it into a list of integers. Then, it performs a left cyclic shift of 4 positions 
on this list: the first 4 integers are moved to the end, and the remaining 8 
integers are shifted to the beginning, maintaining their relative order. The 
final output is the transformed list of 12 integers.
"""

def parse_input_string_to_list(input_str: str) -> typing.List[int]:
    """
    Parses a string of space-separated integers into a list of integers.

    Args:
        input_str: The input string.

    Returns:
        A list of integers.

    Raises:
        ValueError: If the string cannot be parsed correctly or if the resulting
                    list does not contain exactly 12 integers.
    """
    try:
        # Split the string by spaces
        string_list = input_str.split()
        # Convert each part to an integer
        parsed_list = [int(x) for x in string_list]
    except ValueError:
        raise ValueError("Input string must contain only space-separated integers.")

    # Validate the length of the parsed list
    if len(parsed_list) != 12:
        raise ValueError(f"Input string must contain exactly 12 integers, found {len(parsed_list)}.")

    return parsed_list

def cyclic_left_shift_by_4(data_list: typing.List[int]) -> typing.List[int]:
    """
    Performs a cyclic left shift by 4 positions on a list of 12 elements.

    Args:
        data_list: A list containing 12 integers.

    Returns:
        The transformed list.
        
    Raises:
        ValueError: If the input list does not contain exactly 12 elements.        
    """
    # Although parsing ensures 12 elements, this check makes the helper robust
    if len(data_list) != 12:
        raise ValueError("List must contain exactly 12 elements for this specific shift.")

    # Identify the first 4 elements (indices 0, 1, 2, 3).
    first_part = data_list[0:4]

    # Identify the remaining 8 elements (indices 4 through 11).
    second_part = data_list[4:12]

    # Create the output list by concatenating the second part followed by the first part.
    shifted_list = second_part + first_part

    return shifted_list


def transform(input_str: str) -> typing.List[int]:
    """
    Applies the full transformation pipeline: parsing and cyclic shifting.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Step 1: Parse the input string into a list of integers.
    # This includes validation for format and count (12 integers).
    int_list = parse_input_string_to_list(input_str)

    # Step 2: Perform the left cyclic shift by 4 positions on the list.
    output_list = cyclic_left_shift_by_4(int_list)

    # Step 3: Return the resulting list.
    return output_list