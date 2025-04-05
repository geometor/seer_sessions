"""
Transforms an input string of space-separated digits by parsing it into a list of integers, 
moving the first integer to the end of the list, and then formatting the modified list 
back into a space-separated string.
"""

# No specific imports needed for this basic string/list manipulation.
# import numpy as np # Not used

def _parse_string_to_int_list(s: str) -> list[int]:
    """
    Parses a space-separated string of digits into a list of integers.
    Handles empty or invalid inputs gracefully.
    """
    # Handle empty or whitespace-only strings
    if not s or not s.strip():
        return []
    # Split the string by spaces and convert each part to an integer
    try:
        return [int(x) for x in s.split()]
    except ValueError:
        # Handle cases where splitting might produce non-integer parts
        # In the context of this ARC task, this is unlikely given the examples,
        # but robust parsing includes error handling.
        # For this task, we might assume valid input based on examples, 
        # but returning an empty list or raising an error are options.
        # Let's return an empty list for simplicity matching the initial check.
        print(f"Warning: Input string '{s}' contained non-integer parts after splitting.")
        return []

def _format_int_list_to_string(lst: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    # Convert each integer back to a string and join with spaces
    return " ".join(map(str, lst))

def transform(input_str: str) -> str:
    """
    Applies the transformation: moves the first element of the sequence derived 
    from the input string to the end, returning the result as a space-separated string.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string representing the transformed sequence, with digits separated by spaces.
    """

    # 1. Parse the input string into a list of integers.
    # Use the helper function for parsing.
    integer_list = _parse_string_to_int_list(input_str)

    # 2. Check if transformation is needed.
    # The transformation only applies if the list has at least two elements.
    if len(integer_list) < 2:
        # If fewer than 2 elements, the list remains unchanged.
        # We still need to format it back to a string for the return type.
        output_list = integer_list
    else:
        # 3. Perform the rotation: Move the first element to the end.
        # a. Identify and store the first element.
        first_element = integer_list[0]

        # b. Create a new list with elements from the second position onwards (slicing).
        remaining_elements = integer_list[1:]

        # c. Append the stored first element to the end of the new list.
        output_list = remaining_elements + [first_element]

    # 4. Format the resulting list back into a space-separated string.
    # Use the helper function for formatting.
    output_str = _format_int_list_to_string(output_list)

    # 5. Return the final string.
    return output_str
