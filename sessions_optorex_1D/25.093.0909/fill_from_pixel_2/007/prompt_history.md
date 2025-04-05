
## train_1

**input:**
```
0 0 0 0 0 1 8 8 8 0 0 0
```


**output:**
```
1 1 1 1 1 1 8 8 8 0 0 0
```


## train_2

**input:**
```
0 0 6 8 8 8 8 0 0 0 0 0
```


**output:**
```
6 6 6 8 8 8 8 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 1 1 3 0 0 0 0 0
```


**output:**
```
0 0 1 1 1 1 3 3 3 3 3 3
```


## train_4

**input:**
```
0 0 2 5 5 5 0 0 0 0 0 0
```


**output:**
```
2 2 2 5 5 5 0 0 0 0 0 0
```


## train_5

**input:**
```
9 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
9 4 4 4 4 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 8 1 1 1 1 0 0 0 0 0
```


**output:**
```
8 8 8 1 1 1 1 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 7 7 7 2 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 2 2 2 2 2
```

*   **Perception of the elements:**
    *   The input and output are lists of single-digit integers.
    *   The core transformation involves conditionally replacing sequences of zeros ('0') at the beginning and/or end of the list.
    *   The replacement value is determined by the non-zero number adjacent to the sequence of zeros.
    *   The replacement only occurs under specific conditions related to the values of the first two distinct non-zero numbers (for the beginning) and the last two distinct non-zero numbers (for the end).

*   **YAML Facts:**
    
```yaml
    objects:
      - input_list:
          type: list
          contains: integers (0-9)
      - output_list:
          type: list
          contains: integers (0-9)
          derivation: modified version of input_list
      - element:
          type: integer
          value_range: 0-9
      - zero_sequence:
          type: sublist
          contains_only: 0
          location: start or end of input_list
      - non_zero_element:
          type: integer
          value_range: 1-9
          properties: [value, index]
      - first_non_zero:
          type: non_zero_element
          relation: earliest non_zero element in the list
      - second_non_zero:
          type: non_zero_element
          relation: second earliest non_zero element in the list (if exists)
      - last_non_zero:
          type: non_zero_element
          relation: latest non_zero element in the list
      - second_last_non_zero:
          type: non_zero_element
          relation: second latest non_zero element in the list (if exists)

    actions:
      - find_non_zeros:
          input: input_list
          output: list of (value, index) pairs for non_zero_elements
      - compare_values:
          input: two non_zero_elements
          output: boolean (equal or not equal)
      - fill_zeros:
          target: section of output_list (start or end)
          condition: comparison result of relevant non-zero elements
          value: value of the adjacent non_zero_element (first_non_zero or last_non_zero)

    relationships:
      - adjacency: A zero_sequence is adjacent to a non_zero_element at the start or end.
      - conditional_fill_start: The zero_sequence at the start is filled if the first_non_zero value differs from the second_non_zero value (or if only one non_zero element exists).
      - conditional_fill_end: The zero_sequence at the end is filled if the last_non_zero value differs from the second_last_non_zero value (or if only one non_zero element exists).
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input list to serve as the initial output list.
    2.  Identify all non-zero elements and their indices in the input list.
    3.  If there are no non-zero elements, return the output list unchanged.
    4.  Determine the first non-zero element (value `v1`, index `i1`) and the last non-zero element (value `vL`, index `iL`).
    5.  **Left Fill Check:**
        a.  Find the second non-zero element (value `v2`, index `i2`) if it exists.
        b.  If only one non-zero element exists OR if `v1` is not equal to `v2`, then replace all elements in the output list from index 0 up to (but not including) index `i1` with the value `v1`.
    6.  **Right Fill Check:**
        a.  Find the second-to-last non-zero element (value `vL-1`, index `iL-1`) if it exists.
        b.  If only one non-zero element exists OR if `vL` is not equal to `vL-1`, then replace all elements in the output list from index `iL + 1` to the end of the list with the value `vL`.
    7.  Return the modified output list.
```python
import math
import re # Using re for potential string parsing if needed, although assuming list input for now

"""
Transforms the input list by conditionally filling leading/trailing zeros.
Zeros at the start are filled with the value of the first non-zero element 
if its value differs from the second non-zero element (or if only one non-zero element exists).
Zeros at the end are filled with the value of the last non-zero element 
if its value differs from the second-to-last non-zero element (or if only one non-zero element exists).
"""

def find_non_zeros(data_list):
    """
    Identifies all non-zero elements and their indices in a list.

    Args:
        data_list: A list of numbers.

    Returns:
        A list of tuples, where each tuple is (value, index) for a non-zero element.
        Returns an empty list if no non-zero elements are found.
    """
    non_zeros = []
    for index, value in enumerate(data_list):
        if value != 0:
            non_zeros.append((value, index))
    return non_zeros

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_grid: A list of integers (0-9).

    Returns:
        A new list of integers representing the transformed output.
    """
    # initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find all non-zero elements and their indices
    non_zeros = find_non_zeros(input_grid)

    # If there are no non-zero elements, return the original list
    if not non_zeros:
        return output_grid

    num_non_zeros = len(non_zeros)

    # --- Left Fill Check ---
    # Get the first non-zero element
    v1, i1 = non_zeros[0]
    
    # Determine if the left side (leading zeros) should be filled
    fill_left = False
    if num_non_zeros == 1:
        # If there's only one non-zero number, always fill the left
        fill_left = True
    else:
        # If there are multiple non-zeros, compare the first two
        v2, i2 = non_zeros[1]
        if v1 != v2:
            fill_left = True

    # Perform the left fill if the condition is met
    if fill_left:
        for i in range(i1): # Iterate from index 0 up to (but not including) i1
            if output_grid[i] == 0: # Only fill existing zeros
                 output_grid[i] = v1

    # --- Right Fill Check ---
    # Get the last non-zero element
    vL, iL = non_zeros[-1]

    # Determine if the right side (trailing zeros) should be filled
    fill_right = False
    if num_non_zeros == 1:
         # If there's only one non-zero number, always fill the right
        fill_right = True
    else:
        # If there are multiple non-zeros, compare the last two
        vL_minus_1, iL_minus_1 = non_zeros[-2]
        if vL != vL_minus_1:
            fill_right = True

    # Perform the right fill if the condition is met
    if fill_right:
        for i in range(iL + 1, len(output_grid)): # Iterate from index iL + 1 to the end
             if output_grid[i] == 0: # Only fill existing zeros
                output_grid[i] = vL

    return output_grid

# Example Usage (parsing string input as seen in examples)
def parse_input_string(s: str) -> list[int]:
    return [int(x) for x in s.split()]

def format_output_list(lst: list[int]) -> str:
    return " ".join(map(str, lst))

# Test cases from the problem description
train_examples = [
    ("0 0 0 0 0 1 8 8 8 0 0 0", "1 1 1 1 1 1 8 8 8 0 0 0"),
    ("0 0 6 8 8 8 8 0 0 0 0 0", "6 6 6 8 8 8 8 0 0 0 0 0"),
    ("0 0 1 1 1 1 3 0 0 0 0 0", "0 0 1 1 1 1 3 3 3 3 3 3"),
    ("0 0 2 5 5 5 0 0 0 0 0 0", "2 2 2 5 5 5 0 0 0 0 0 0"),
    ("9 4 4 4 4 0 0 0 0 0 0 0", "9 4 4 4 4 0 0 0 0 0 0 0"), # No change expected here
    ("0 0 8 1 1 1 1 0 0 0 0 0", "8 8 8 1 1 1 1 0 0 0 0 0"),
    ("0 0 0 0 7 7 7 2 0 0 0 0", "0 0 0 0 7 7 7 2 2 2 2 2"),
]

# print("Testing transform function:")
# for i, (input_str, expected_output_str) in enumerate(train_examples):
#     input_list = parse_input_string(input_str)
#     output_list = transform(input_list)
#     output_str = format_output_list(output_list)
#     print(f"Train {i+1}:")
#     print(f"  Input:    {input_str}")
#     print(f"  Output:   {output_str}")
#     print(f"  Expected: {expected_output_str}")
#     print(f"  Match:    {output_str == expected_output_str}")
#     print("-" * 10)
```
```python
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
```
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 1 8 8 8 0 0 0
```
Expected Output:
```
1 1 1 1 1 1 8 8 8 0 0 0
```
Transformed Output:
```
0 0 0 0 0 1 8 8 8 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 83.33333333333333

## Example 2:
Input:
```
0 0 6 8 8 8 8 0 0 0 0 0
```
Expected Output:
```
6 6 6 8 8 8 8 0 0 0 0 0
```
Transformed Output:
```
0 0 6 8 8 8 8 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

## Example 3:
Input:
```
0 0 1 1 1 1 3 0 0 0 0 0
```
Expected Output:
```
0 0 1 1 1 1 3 3 3 3 3 3
```
Transformed Output:
```
0 0 1 1 1 1 3 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 83.33333333333333

## Example 4:
Input:
```
0 0 2 5 5 5 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 5 5 5 0 0 0 0 0 0
```
Transformed Output:
```
0 0 2 5 5 5 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

## Example 5:
Input:
```
9 4 4 4 4 0 0 0 0 0 0 0
```
Expected Output:
```
9 4 4 4 4 0 0 0 0 0 0 0
```
Transformed Output:
```
9 4 4 4 4 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 6:
Input:
```
0 0 8 1 1 1 1 0 0 0 0 0
```
Expected Output:
```
8 8 8 1 1 1 1 0 0 0 0 0
```
Transformed Output:
```
0 0 8 1 1 1 1 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

## Example 7:
Input:
```
0 0 0 0 7 7 7 2 0 0 0 0
```
Expected Output:
```
0 0 0 0 7 7 7 2 2 2 2 2
```
Transformed Output:
```
0 0 0 0 7 7 7 2 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 66.66666666666669

Test Set Results:

## Example 1:
Input:
```
0 0 0 3 3 3 3 3 9 0 0 0
```
Expected Output:
```
0 0 0 3 3 3 3 3 9 9 9 9
```
Transformed Output:
```
0 0 0 3 3 3 3 3 9 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0
## General Assessment

The provided execution results indicate that the Python code (`code_00.py`) failed to produce the expected outputs for most examples where a modification (filling of leading/trailing zeros) was required. The code correctly handled Example 5 where no change was needed.

Analysis of the expected input/output pairs reveals a consistent rule:
1.  Leading zeros are filled with the value of the first non-zero element *if* that element's value differs from the second non-zero element's value (or if there's only one non-zero element).
2.  Trailing zeros are filled with the value of the last non-zero element *if* that element's value differs from the second-to-last non-zero element's value (or if there's only one non-zero element).

A step-by-step trace of the provided `code_00.py` suggests its logic *does* implement this rule correctly. The discrepancy between the code's apparent logic and the reported execution results is significant. The failure mode (zeros not being filled when the conditions are met) points towards an issue either in the execution environment or a very subtle bug in the fill implementation within the loops (e.g., the `output_grid[i] = fill_value` assignment not taking effect).

**Strategy:**
The strategy is to refine the documentation (YAML, Natural Language Program) based on the clearly discernible pattern in the *expected* input/output pairs, assuming this represents the correct transformation rule. The previous code's failure is noted, but the description will target the *correct* transformation. The code execution metrics confirm the conditions under which fills should occur based on the expected outputs.

## Metrics

The following metrics were gathered by analyzing the non-zero elements in each input list and determining the fill conditions based on the derived rule.


```json
{
  "Example 1": {
    "Input": "0 0 0 0 0 1 8 8 8 0 0 0",
    "NonZeros": [{"value": 1, "index": 5}, {"value": 8, "index": 6}, {"value": 8, "index": 7}, {"value": 8, "index": 8}],
    "ShouldFillLeft": true, "ShouldFillRight": false, "LeftFillValue": 1, "RightFillValue": null
  },
  "Example 2": {
    "Input": "0 0 6 8 8 8 8 0 0 0 0 0",
    "NonZeros": [{"value": 6, "index": 2}, {"value": 8, "index": 3}, {"value": 8, "index": 4}, {"value": 8, "index": 5}, {"value": 8, "index": 6}],
    "ShouldFillLeft": true, "ShouldFillRight": false, "LeftFillValue": 6, "RightFillValue": null
  },
  "Example 3": {
    "Input": "0 0 1 1 1 1 3 0 0 0 0 0",
    "NonZeros": [{"value": 1, "index": 2}, {"value": 1, "index": 3}, {"value": 1, "index": 4}, {"value": 1, "index": 5}, {"value": 3, "index": 6}],
    "ShouldFillLeft": false, "ShouldFillRight": true, "LeftFillValue": null, "RightFillValue": 3
  },
  "Example 4": {
    "Input": "0 0 2 5 5 5 0 0 0 0 0 0",
    "NonZeros": [{"value": 2, "index": 2}, {"value": 5, "index": 3}, {"value": 5, "index": 4}, {"value": 5, "index": 5}],
    "ShouldFillLeft": true, "ShouldFillRight": false, "LeftFillValue": 2, "RightFillValue": null
  },
  "Example 5": {
    "Input": "9 4 4 4 4 0 0 0 0 0 0 0",
    "NonZeros": [{"value": 9, "index": 0}, {"value": 4, "index": 1}, {"value": 4, "index": 2}, {"value": 4, "index": 3}, {"value": 4, "index": 4}],
    "ShouldFillLeft": false, "ShouldFillRight": false, "LeftFillValue": null, "RightFillValue": null
  },
  "Example 6": {
    "Input": "0 0 8 1 1 1 1 0 0 0 0 0",
    "NonZeros": [{"value": 8, "index": 2}, {"value": 1, "index": 3}, {"value": 1, "index": 4}, {"value": 1, "index": 5}, {"value": 1, "index": 6}],
    "ShouldFillLeft": true, "ShouldFillRight": false, "LeftFillValue": 8, "RightFillValue": null
  },
  "Example 7": {
    "Input": "0 0 0 0 7 7 7 2 0 0 0 0",
    "NonZeros": [{"value": 7, "index": 4}, {"value": 7, "index": 5}, {"value": 7, "index": 6}, {"value": 2, "index": 7}],
    "ShouldFillLeft": false, "ShouldFillRight": true, "LeftFillValue": null, "RightFillValue": 2
  },
  "Test Example 1 (Example 8 overall)": {
    "Input": "0 0 0 3 3 3 3 3 9 0 0 0",
    "NonZeros": [{"value": 3, "index": 3}, {"value": 3, "index": 4}, {"value": 3, "index": 5}, {"value": 3, "index": 6}, {"value": 3, "index": 7}, {"value": 9, "index": 8}],
    "ShouldFillLeft": false, "ShouldFillRight": true, "LeftFillValue": null, "RightFillValue": 9
  }
}
```

These metrics confirm that the conditions derived (fill if adjacent non-zeros differ or only one exists, and if there are zeros to fill) align perfectly with the transformations seen in the expected outputs.

## YAML Facts


```yaml
objects:
  - input_list:
      type: list
      contains: integers (0-9)
  - output_list:
      type: list
      contains: integers (0-9)
      derivation: modified version of input_list
  - element:
      type: integer
      value_range: 0-9
  - non_zero_element:
      type: dict
      properties:
        - value: integer (1-9)
        - index: integer (position in list)
  - non_zero_sequence:
      type: list
      contains: non_zero_element
      ordering: by index (ascending)
      derivation: extracted from input_list
  - leading_zeros:
      type: sublist
      location: start of input_list (indices 0 to first_non_zero.index - 1)
      condition: exists only if first_non_zero.index > 0
  - trailing_zeros:
      type: sublist
      location: end of input_list (indices last_non_zero.index + 1 to end)
      condition: exists only if last_non_zero.index < len(input_list) - 1

actions:
  - find_non_zeros:
      input: input_list
      output: non_zero_sequence
  - check_left_fill_condition:
      input: non_zero_sequence
      output: boolean
      logic: >
        True if len(non_zero_sequence) == 1 OR
        (len(non_zero_sequence) > 1 AND
         non_zero_sequence[0].value != non_zero_sequence[1].value)
  - check_right_fill_condition:
      input: non_zero_sequence
      output: boolean
      logic: >
        True if len(non_zero_sequence) == 1 OR
        (len(non_zero_sequence) > 1 AND
         non_zero_sequence[-1].value != non_zero_sequence[-2].value)
  - fill_leading_zeros:
      target: output_list
      condition: check_left_fill_condition is True AND leading_zeros exist
      range: indices from 0 up to (but not including) non_zero_sequence[0].index
      value: non_zero_sequence[0].value
  - fill_trailing_zeros:
      target: output_list
      condition: check_right_fill_condition is True AND trailing_zeros exist
      range: indices from non_zero_sequence[-1].index + 1 to end of list
      value: non_zero_sequence[-1].value

relationships:
  - fill_dependency: Filling leading/trailing zeros depends on the comparison of values between adjacent non-zero elements in the sequence (first vs second, last vs second-last).
  - edge_case_single_nonzero: If only one non-zero element exists, both fill conditions are met (if corresponding zeros exist).
  - existence_dependency: Filling only occurs if there are actual zero elements in the leading or trailing sections.
```


## Natural Language Program

1.  Create a mutable copy of the input list, this will be the `output_list`.
2.  Identify all non-zero elements in the `input_list` and store them along with their original indices in an ordered list called `non_zero_sequence`.
3.  If `non_zero_sequence` is empty, return the `output_list` unchanged.
4.  Determine the number of non-zero elements, `n`.
5.  **Left Fill Check:**
    a.  Define the left fill condition as `True` if `n == 1`.
    b.  If `n > 1`, set the left fill condition to `True` if the value of the first element in `non_zero_sequence` is *not equal* to the value of the second element. Otherwise, set it to `False`.
    c.  If the left fill condition is `True` and the index of the first non-zero element is greater than 0 (meaning leading zeros exist):
        i.  Get the value (`v1`) and index (`i1`) of the first non-zero element.
        ii. Iterate from index 0 up to (but not including) `i1`. For each index `i` in this range, set `output_list[i]` to `v1`.
6.  **Right Fill Check:**
    a.  Define the right fill condition as `True` if `n == 1`.
    b.  If `n > 1`, set the right fill condition to `True` if the value of the last element in `non_zero_sequence` is *not equal* to the value of the second-to-last element. Otherwise, set it to `False`.
    c.  If the right fill condition is `True` and the index of the last non-zero element is less than the last index of the list (meaning trailing zeros exist):
        i.  Get the value (`vL`) and index (`iL`) of the last non-zero element.
        ii. Iterate from index `iL + 1` to the end of the `output_list`. For each index `i` in this range, set `output_list[i]` to `vL`.
7.  Return the modified `output_list`.
