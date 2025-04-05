import re # Used for potential pattern finding if needed, though direct iteration seems simpler here.

"""
Transforms a sequence of 12 digits based on the following rules:
1. The input sequence is treated as two parts: data (first 9 digits) and control (last 3 digits).
2. The control digits (indices 9, 10, 11) provide potential replacement values.
3. Only non-zero control digits are used as replacement values, maintaining their relative order.
4. Contiguous groups of the digit '5' in the data part are identified.
5. Each identified group of '5's is replaced sequentially by the next available non-zero replacement value.
6. Digits other than '5' in the data part remain unchanged.
7. The control digits (indices 9, 10, 11) in the output are identical to those in the input.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string of digits.

    Args:
        input_str: A string containing 12 space-separated single digits.

    Returns:
        A string containing the 12 space-separated transformed digits.
    """

    # Parse the input string into a list of integers
    try:
        input_list = [int(digit) for digit in input_str.split()]
        if len(input_list) != 12:
            raise ValueError("Input must contain exactly 12 digits.")
    except ValueError as e:
        print(f"Error parsing input: {e}")
        return "" # Or raise a more specific error

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # Extract the control digits (indices 9, 10, 11)
    control_digits = input_list[9:]

    # Create the ordered list of non-zero replacement values from control digits
    replacement_values = [digit for digit in control_digits if digit != 0]

    # Initialize index for tracking which replacement value to use
    replacement_idx = 0
    # Variable to hold the replacement value for the current group of 5s
    current_replacement_value_for_group = None

    # Iterate through the data part of the input (indices 0 to 8)
    for i in range(9):
        current_digit = input_list[i]

        # Check if this is the start of a new contiguous group of 5s
        is_start_of_group = (current_digit == 5 and (i == 0 or input_list[i-1] != 5))

        # If it's the start of a group, determine the replacement value for this group
        if is_start_of_group:
            # Check if there are still unused replacement values
            if replacement_idx < len(replacement_values):
                # Assign the next available replacement value to this group
                current_replacement_value_for_group = replacement_values[replacement_idx]
                # Move to the next replacement value for the potential next group
                replacement_idx += 1
            else:
                # No more replacement values available for this or subsequent groups
                current_replacement_value_for_group = None

        # If the current digit is 5 and its group has an assigned replacement value
        if current_digit == 5 and current_replacement_value_for_group is not None:
            # Replace the digit in the output list
            output_list[i] = current_replacement_value_for_group
        # If the current digit is not 5, the group context effectively ends,
        # but we don't need to reset current_replacement_value_for_group here
        # as the is_start_of_group logic handles picking the next value correctly.
        # The output_list already holds the correct non-5 value from the initial copy.

    # The control digits (indices 9, 10, 11) are already correct in output_list
    # because it was initialized as a copy of input_list.

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
