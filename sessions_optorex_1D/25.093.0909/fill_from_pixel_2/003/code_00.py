import math # Although not strictly needed for this logic, included as per template instruction

"""
Transforms the input list by conditionally filling leading and/or trailing zeros.
1. Identifies all non-zero elements and their indices.
2. Checks the condition for filling leading zeros: 
   - If only one non-zero element exists, OR
   - If the value of the first non-zero element is different from the second non-zero element.
   - If the condition is met, fills leading zeros (indices before the first non-zero) with the value of the first non-zero element.
3. Checks the condition for filling trailing zeros:
   - If only one non-zero element exists, OR
   - If the value of the last non-zero element is different from the second-to-last non-zero element.
   - If the condition is met, fills trailing zeros (indices after the last non-zero) with the value of the last non-zero element.
4. Returns the modified list.
"""

def find_all_non_zeros(data_list: list[int]) -> list[dict]:
    """
    Finds all non-zero elements in the input list and returns them as a list
    of dictionaries, each containing the 'value' and 'index'.

    Args:
        data_list: The input list of integers.

    Returns:
        A list of dictionaries [{'value': v, 'index': i}, ...], ordered by index.
        Returns an empty list if no non-zero elements are found.
    """
    non_zero_sequence = []
    for index, value in enumerate(data_list):
        if value != 0:
            non_zero_sequence.append({'value': value, 'index': index})
    return non_zero_sequence

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the described transformation rule to the input list.

    Args:
        input_grid: A list of integers (0-9).

    Returns:
        A new list of integers representing the transformed output.
    """
    # initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find all non-zero elements and their indices
    non_zero_sequence = find_all_non_zeros(input_grid)
    n = len(non_zero_sequence)

    # If no non-zero elements, return the original grid
    if n == 0:
        return output_grid

    # Identify first and last non-zero elements
    first_nz = non_zero_sequence[0]
    last_nz = non_zero_sequence[-1] # same as first_nz if n=1

    # --- Evaluate Left Fill Condition ---
    fill_left = False
    if n == 1:
        fill_left = True
    else:
        # Compare first non-zero with the second non-zero
        second_nz = non_zero_sequence[1]
        if first_nz['value'] != second_nz['value']:
            fill_left = True

    # Perform left fill if condition is met
    if fill_left:
        fill_value = first_nz['value']
        fill_end_index = first_nz['index'] # exclusive end index
        for i in range(fill_end_index):
            # We only modify existing zeros, though the examples suggest
            # the leading section *only* contains zeros anyway.
            # Let's stick to modifying only zeros for robustness.
            if output_grid[i] == 0:
                output_grid[i] = fill_value

    # --- Evaluate Right Fill Condition ---
    fill_right = False
    if n == 1:
        fill_right = True
    else:
        # Compare last non-zero with the second-to-last non-zero
        second_last_nz = non_zero_sequence[-2]
        if last_nz['value'] != second_last_nz['value']:
            fill_right = True

    # Perform right fill if condition is met
    if fill_right:
        fill_value = last_nz['value']
        fill_start_index = last_nz['index'] + 1 # inclusive start index
        for i in range(fill_start_index, len(output_grid)):
            # Modify only existing zeros in the trailing section.
            if output_grid[i] == 0:
                output_grid[i] = fill_value

    # return the modified grid
    return output_grid