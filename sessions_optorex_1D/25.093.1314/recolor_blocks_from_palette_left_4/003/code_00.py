import numpy as np # Use numpy for potential array input and easier slicing/copying

"""
Transforms a sequence of 12 integers based on the following rules:
1. The input sequence (list or numpy array) is treated as two parts: data (first 9 elements) and control (last 3 elements).
2. The control elements (indices 9, 10, 11) provide potential replacement values.
3. Only non-zero control elements are used as replacement values, maintaining their relative order.
4. Contiguous groups of the value '5' in the data part are identified.
5. Each identified group of '5's is replaced sequentially by the next available non-zero replacement value.
6. Elements other than '5' in the data part remain unchanged.
7. The control elements (indices 9, 10, 11) in the output are identical to those in the input.
"""

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence of digits.

    Args:
        input_sequence: A list or numpy array containing 12 integers.

    Returns:
        A numpy array containing the 12 transformed integers.
    """
    # Ensure input is a numpy array for consistent handling
    input_array = np.array(input_sequence)

    if input_array.shape != (12,):
         raise ValueError("Input must contain exactly 12 elements.")

    # Initialize the output array as a copy of the input
    output_array = np.copy(input_array)

    # Extract the control digits (indices 9, 10, 11)
    control_digits = input_array[9:]

    # Create the ordered list of non-zero replacement values from control digits
    replacement_values = [digit for digit in control_digits if digit != 0]

    # Initialize index for tracking which replacement value to use
    replacement_idx = 0
    # Variable to hold the replacement value for the current group of 5s
    current_group_replacement = None # Use None to indicate no active replacement

    # Iterate through the data part of the input (indices 0 to 8)
    for i in range(9):
        current_digit = input_array[i]

        # Check if this is the start of a new contiguous group of 5s
        # A digit is the start if it's 5 AND (it's the first digit OR the previous digit was not 5)
        is_start_of_group = (current_digit == 5 and (i == 0 or input_array[i-1] != 5))

        # If it's the start of a group, determine the replacement value for this group
        if is_start_of_group:
            # Check if there are still unused replacement values
            if replacement_idx < len(replacement_values):
                # Assign the next available replacement value to this group
                current_group_replacement = replacement_values[replacement_idx]
                # Move to the next replacement value for the potential next group
                replacement_idx += 1
            else:
                # No more replacement values available for this or subsequent groups
                current_group_replacement = None # Explicitly set to None

        # If the current digit is 5 AND its group has an assigned replacement value
        if current_digit == 5 and current_group_replacement is not None:
            # Replace the digit in the output array
            output_array[i] = current_group_replacement
        # If the current digit is not 5, the group context effectively ends for assignment purposes.
        # The output_array already holds the correct non-5 value from the initial copy.
        # No need to reset current_group_replacement here, as is_start_of_group handles finding the next value.


    # The control digits (indices 9, 10, 11) are already correct in output_array
    # because it was initialized as a copy of input_array.

    return output_array