
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
