```python
import numpy as np

"""
Transforms a sequence of 12 integers based on the following rules:

1.  Accepts an input sequence (list or NumPy array) containing 12 integers.
2.  Creates a mutable copy of the input sequence to serve as the initial output sequence.
3.  Identifies the last three integers (indices 9, 10, 11) as control elements.
4.  Creates an ordered list of replacement values by filtering the control elements, keeping only non-zero values while preserving their original relative order.
5.  Iterates through the first nine elements (data part, indices 0-8) of the input sequence.
6.  Detects the start of contiguous groups of the target value '5'.
7.  For each new group of '5's found, assigns the next available replacement value from the filtered list, if one exists.
8.  Replaces all '5's belonging to an assigned group in the output sequence with the corresponding replacement value.
9.  Elements other than '5' in the data part, and all elements in the control part (indices 9-11), remain unchanged in the output sequence.
10. Returns the modified output sequence as a NumPy array.
"""

def _get_non_zero_replacements(control_elements: np.ndarray) -> list[int]:
    """
    Filters the control elements to extract non-zero values, preserving order.

    Args:
        control_elements: A NumPy array slice containing the control elements.

    Returns:
        A list of non-zero integers from the control elements.
    """
    return [element for element in control_elements if element != 0]

def transform(input_sequence) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence of integers.

    Args:
        input_sequence: A list or NumPy array containing 12 integers.

    Returns:
        A NumPy array containing the 12 transformed integers.
    """
    # 1. Ensure input is a numpy array and validate length
    input_array = np.array(input_sequence)
    if input_array.shape != (12,):
        raise ValueError("Input must contain exactly 12 elements.")

    # 2. Initialize Output: Create a copy of the input array.
    output_array = np.copy(input_array)

    # 3. Extract Controls: Get the control elements (last 3).
    control_elements = input_array[9:]

    # 4. Filter Replacements: Get the non-zero replacement values in order.
    replacement_values = _get_non_zero_replacements(control_elements)

    # 5. Iterate through data part, identify groups, and replace.
    replacement_idx = 0  # Index for the next replacement value to use
    current_replacement_value = None # Holds the value for the current group of 5s being processed

    for i in range(9): # Iterate through the data part indices 0 to 8
        current_digit = input_array[i]
        target_value = 5

        # 6. Detect start of a new contiguous group of the target value (5)
        # A digit is the start if it's the target value AND
        # (it's the first element OR the previous element was not the target value)
        is_start_of_group = (current_digit == target_value and
                             (i == 0 or input_array[i-1] != target_value))

        if is_start_of_group:
            # 7. Assign the next replacement value if available
            if replacement_idx < len(replacement_values):
                # Assign the next available value for this group
                current_replacement_value = replacement_values[replacement_idx]
                # Increment index for the next group
                replacement_idx += 1
            else:
                # No more replacement values available for this or subsequent groups
                current_replacement_value = None # Mark that no replacement is active

        # 8. Replace element if it's the target value and belongs to an assigned group
        if current_digit == target_value and current_replacement_value is not None:
            output_array[i] = current_replacement_value

        # 9. Invariant elements (non-target values in data part, all control elements)
        # are already correct in output_array due to the initial copy.
        # If current_digit is not the target_value, the replacement context
        # (current_replacement_value) effectively ends for assignment purposes,
        # and the next is_start_of_group check will handle the next potential group.

    # 10. Return the modified output sequence.
    return output_array
```