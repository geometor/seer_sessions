
## train_1

**input:**
```
0 0 0 0 0 0 0 4 0 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 4 4
```


## train_2

**input:**
```
0 0 0 0 0 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 3 0 0 0 0 0
```


## train_3

**input:**
```
6 0 0 0 0 0 0 0 0 6 0 0
```


**output:**
```
6 6 6 6 6 6 6 6 6 6 0 0
```


## train_4

**input:**
```
0 1 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 0 0
```


## train_5

**input:**
```
0 0 0 9 0 0 0 0 0 9 0 0
```


**output:**
```
0 0 0 9 9 9 9 9 9 9 0 0
```


## train_6

**input:**
```
0 0 0 2 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 0 0
```


## train_7

**input:**
```
0 0 0 0 4 0 0 0 0 0 0 4
```


**output:**
```
0 0 0 0 4 4 4 4 4 4 4 4
```

*   **Perception of Task Elements:**
    *   The input and output are one-dimensional lists (or arrays) of single-digit integers.
    *   Each input list contains exactly two instances of the same non-zero digit, with all other elements being zero.
    *   The output list is derived from the input list by modifying the elements *between* (and including) the positions of the two non-zero digits.
    *   The modification involves changing all elements within this identified range to the value of the non-zero digit.
    *   Elements outside this range remain unchanged from the input.

*   **YAML Facts:**
    
```yaml
    task_type: array_transformation
    input_element_type: integer (single digit)
    output_element_type: integer (single digit)
    input_structure:
      type: list
      properties:
        - contains exactly two identical non-zero digits (let's call this 'fill_value')
        - all other elements are zero
    output_structure:
      type: list
      derivation: based on input list
    transformation_logic:
      action: fill_range
      parameters:
        - fill_value: the non-zero digit found in the input
        - start_index: the index of the first occurrence of fill_value in the input
        - end_index: the index of the second occurrence of fill_value in the input
      steps:
        - identify the non-zero digit (fill_value) in the input list
        - find the indices of the first and second occurrences of fill_value
        - create the output list, initially identical to the input list
        - modify the output list by setting all elements from start_index to end_index (inclusive) to the fill_value
    invariants:
      - list length remains constant between input and output
      - elements outside the range [start_index, end_index] remain unchanged
    ```


*   **Natural Language Program:**
    1.  Examine the input list to find the single non-zero integer value present; let this value be `V`.
    2.  Locate the index of the first occurrence of `V` in the input list; let this be `start_index`.
    3.  Locate the index of the second occurrence of `V` in the input list; let this be `end_index`.
    4.  Initialize the output list as a copy of the input list.
    5.  Iterate through the output list from `start_index` to `end_index` (inclusive). For each index in this range, set the corresponding element's value to `V`.
    6.  The resulting list is the final output.
```python
"""
Transforms an input list of integers based on the following rule:
1. Find the single non-zero integer value (V) present in the input list.
2. Locate the indices of the first (start_index) and second (end_index) occurrences of V.
3. Initialize the output list as a copy of the input list.
4. Fill the elements in the output list from start_index to end_index (inclusive) with the value V.
5. Return the modified list.
"""

import numpy as np

def find_non_zero_value_and_indices(data):
    """
    Finds the non-zero value and its first and second indices in a list.

    Args:
        data: A list of integers containing exactly two identical non-zero values.

    Returns:
        A tuple (value, start_index, end_index) or (None, -1, -1) if not found.
    """
    non_zero_value = None
    indices = []
    for i, x in enumerate(data):
        if x != 0:
            if non_zero_value is None:
                non_zero_value = x
            if x == non_zero_value:
                indices.append(i)
            # Optional: Add check if a different non-zero value is found
            # elif x != 0: 
            #     raise ValueError("Input list contains more than one distinct non-zero value")

    if len(indices) == 2:
        return non_zero_value, indices[0], indices[1]
    else:
        # Handle cases where input assumption isn't met (e.g., fewer/more than 2 non-zeros)
        # For this specific problem based on examples, we assume exactly two are always present.
        # If only one non-zero found, or none, the behavior might need clarification.
        # Based on train_2, if the two values are adjacent, the logic still holds.
        if len(indices) == 1: # Should not happen based on problem description
             return non_zero_value, indices[0], indices[0]
        return None, -1, -1


def transform(input_list):
    """
    Applies the transformation rule to fill the range between two identical non-zero numbers.

    Args:
        input_list: A list of integers with exactly two identical non-zero numbers.

    Returns:
        A new list with the range between the non-zero numbers filled with their value.
    """
    # Find the non-zero value and its start and end indices
    fill_value, start_index, end_index = find_non_zero_value_and_indices(input_list)

    # Initialize the output list as a copy of the input list
    output_list = list(input_list) # Ensure we are working with a copy

    # If valid indices were found
    if start_index != -1 and end_index != -1:
        # Fill the range from start_index to end_index (inclusive) with the fill_value
        for i in range(start_index, end_index + 1):
            output_list[i] = fill_value

    # Return the modified list
    return output_list

```
```python
"""
Transforms an input list or 1D NumPy array of integers based on the following rule:
1. Find the single non-zero integer value (V) present in the input sequence.
2. Locate the indices of the first (start_index) and second (end_index) occurrences of V.
3. Initialize the output sequence as a copy of the input sequence.
4. Fill the elements in the output sequence from start_index to end_index (inclusive) with the value V.
5. Return the modified sequence (as a list).
"""

import numpy as np # Import numpy, as input might be a numpy array

def find_non_zero_value_and_indices(data_list):
    """
    Finds the non-zero value and its first and second indices in a list.

    Args:
        data_list: A list of integers containing exactly two identical non-zero values.

    Returns:
        A tuple (value, start_index, end_index) or (None, -1, -1) if not found
        or if the input assumptions are violated.
    """
    non_zero_value = None
    indices = []
    for i, x in enumerate(data_list):
        if x != 0:
            # Found a non-zero value
            if non_zero_value is None:
                # This is the first non-zero value encountered
                non_zero_value = x
                indices.append(i)
            elif x == non_zero_value:
                # This is the second occurrence of the same non-zero value
                indices.append(i)
            else:
                # Found a different non-zero value - violates assumption
                # Handle error or return indicative values
                return None, -1, -1 # Indicate error/violation

    # Check if exactly two indices were found for the non_zero_value
    if len(indices) == 2:
        return non_zero_value, indices[0], indices[1]
    else:
        # Handle cases where fewer or more than 2 were found (e.g., all zeros, only one non-zero)
        # Based on problem constraints, this shouldn't happen with valid input.
        # If they are adjacent (like train_2), len(indices) will still be 2.
        return None, -1, -1 # Indicate error or unexpected input format


def transform(input_sequence):
    """
    Applies the transformation rule to fill the range between two identical non-zero numbers.

    Args:
        input_sequence: A list or 1D NumPy array of integers with exactly two identical non-zero numbers.

    Returns:
        A new list with the range between the non-zero numbers filled with their value.
        Returns the original list if the input format is invalid.
    """
    # Convert input to a standard Python list to avoid NumPy array ambiguity issues
    # This handles both list and 1D NumPy array inputs safely.
    try:
        input_list = list(input_sequence)
    except TypeError:
        # Handle cases where input is not iterable or convertible to list
        print(f"Error: Input could not be converted to a list. Input type: {type(input_sequence)}")
        # Depending on requirements, could raise an error or return input as is
        return input_sequence # Or potentially return None or raise ValueError

    # Find the non-zero value and its start and end indices using the helper function
    fill_value, start_index, end_index = find_non_zero_value_and_indices(input_list)

    # Initialize the output list as a copy of the input list
    # Making a copy is crucial to avoid modifying the original input
    output_list = list(input_list)

    # Check if valid indices and a fill value were found
    if start_index != -1 and end_index != -1 and fill_value is not None:
        # Fill the range in the output list
        # Iterate from start_index to end_index (inclusive)
        for i in range(start_index, end_index + 1):
            # Set the element at the current index to the fill_value
            output_list[i] = fill_value
    # else:
        # Handle the case where valid indices/value weren't found (e.g., invalid input)
        # Currently, it will just return the unmodified copy.
        # Optionally, add logging or raise an error here.
        # print("Warning: Could not find exactly two identical non-zero values. Returning original list.")


    # Return the modified list
    return output_list
```
