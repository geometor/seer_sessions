```python
import math # Not strictly required by the logic, but included per template.
import numpy as np # Import numpy to handle potential array inputs

"""
Transforms an input grid (list or array of integers) by conditionally filling 
leading and/or trailing zeros based on the values of adjacent non-zero elements.

1.  Identifies all non-zero elements and their indices in the input grid.
2.  Checks the condition for filling leading zeros:
    - If only one non-zero element exists in total, OR
    - If the value of the first non-zero element is different from the value 
      of the second non-zero element.
    - If the condition is met, fills leading zeros (indices before the first 
      non-zero) with the value of the first non-zero element.
3.  Checks the condition for filling trailing zeros:
    - If only one non-zero element exists in total, OR
    - If the value of the last non-zero element is different from the value 
      of the second-to-last non-zero element.
    - If the condition is met, fills trailing zeros (indices after the last 
      non-zero) with the value of the last non-zero element.
4.  Returns the modified grid as a standard Python list.
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
    # Iterate through the list with index and value
    for index, value in enumerate(data_list):
        # Check if the value is not zero
        if value != 0:
            # Append the non-zero element's value and index as a dictionary
            non_zero_sequence.append({'value': value, 'index': index})
    return non_zero_sequence

def transform(input_grid) -> list[int]:
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid: A list or NumPy array of integers (0-9).

    Returns:
        A new list of integers representing the transformed output.
    """
    # Ensure input is a standard Python list to avoid potential NumPy issues
    # during comparisons or assignments if the environment passes a NumPy array.
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        input_list = list(input_grid) # Ensure it's a mutable list

    # initialize output_grid as a copy of the input list
    output_grid = list(input_list) # Use list() constructor for a shallow copy

    # Find all non-zero elements and their indices
    non_zero_sequence = find_all_non_zeros(output_grid)
    n = len(non_zero_sequence)

    # If no non-zero elements, return the original grid copy
    if n == 0:
        return output_grid

    # Identify first and last non-zero elements
    first_nz = non_zero_sequence[0]
    last_nz = non_zero_sequence[-1] # This will be the same as first_nz if n=1

    # --- Evaluate Left Fill Condition ---
    fill_left = False
    # Condition 1: Only one non-zero element exists
    if n == 1:
        fill_left = True
    # Condition 2: More than one non-zero, compare first and second
    else:
        second_nz = non_zero_sequence[1]
        if first_nz['value'] != second_nz['value']:
            fill_left = True

    # Perform left fill if condition is met
    if fill_left:
        fill_value = first_nz['value']
        # Iterate from the start up to the index of the first non-zero element
        fill_end_index = first_nz['index'] # exclusive end index
        for i in range(fill_end_index):
            # Only modify elements that are currently zero
            if output_grid[i] == 0:
                output_grid[i] = fill_value

    # --- Evaluate Right Fill Condition ---
    fill_right = False
    # Condition 1: Only one non-zero element exists
    if n == 1:
        fill_right = True
    # Condition 2: More than one non-zero, compare last and second-to-last
    else:
        second_last_nz = non_zero_sequence[-2]
        if last_nz['value'] != second_last_nz['value']:
            fill_right = True

    # Perform right fill if condition is met
    if fill_right:
        fill_value = last_nz['value']
        # Iterate from the index after the last non-zero element to the end
        fill_start_index = last_nz['index'] + 1 # inclusive start index
        for i in range(fill_start_index, len(output_grid)):
            # Only modify elements that are currently zero
            if output_grid[i] == 0:
                output_grid[i] = fill_value

    # return the modified grid
    return output_grid
```