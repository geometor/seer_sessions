"""
Moves the first three elements of a space-separated sequence of 12 digits to the end of the sequence, preserving the relative order of both the moved elements and the remaining elements. Handles potential byte input by decoding it.
"""

import re # Although split() is preferred, keep import just in case, or remove if definitively not needed.

def transform(input_data) -> str:
    """
    Transforms a sequence of 12 space-separated digits by moving the first three to the end.

    Args:
        input_data: A string or bytes object containing 12 space-separated digits.

    Returns:
        A string containing the transformed sequence of 12 space-separated digits.
    """

    # --- Input Handling and Parsing ---

    # Check if input is bytes and decode if necessary
    if isinstance(input_data, bytes):
        input_str = input_data.decode('utf-8') # Assume UTF-8 encoding
    elif isinstance(input_data, str):
        input_str = input_data
    else:
        raise TypeError("Input must be a string or bytes object.")

    # Split the string into a list of elements based on spaces
    # This handles potential multiple spaces between digits correctly
    digits = input_str.split()

    # Validate the number of elements
    if len(digits) != 12:
        # Attempt fallback parsing if split yields incorrect number, maybe due to inconsistent spacing
        digits = re.findall(r'\S+', input_str) # Find non-whitespace sequences
        if len(digits) != 12:
             # Final attempt: maybe it's just digits without proper spaces
             digits = re.findall(r'\d', input_str)
             if len(digits) != 12:
                 raise ValueError(f"Input string must contain exactly 12 space-separated elements. Found {len(digits)} in '{input_str}'. Parsed as: {digits}")


    # --- Transformation Logic ---

    # Extract the first three elements
    first_three = digits[:3]

    # Extract the remaining elements (from index 3 to the end)
    remaining = digits[3:]

    # Concatenate the remaining elements followed by the first three
    output_digits = remaining + first_three

    # --- Output Formatting ---

    # Format the output list back into a space-separated string
    output_str = " ".join(output_digits)

    return output_str