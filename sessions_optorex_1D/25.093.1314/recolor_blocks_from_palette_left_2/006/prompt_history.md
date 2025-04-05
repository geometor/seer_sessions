
## train_1

**input:**
```
5 5 5 0 0 5 5 5 0 0 2 6
```


**output:**
```
2 2 2 0 0 6 6 6 0 0 2 6
```


## train_2

**input:**
```
0 0 5 5 0 5 5 0 0 0 3 5
```


**output:**
```
0 0 3 3 0 5 5 0 0 0 3 5
```


## train_3

**input:**
```
5 5 0 0 0 0 0 0 0 0 0 3
```


**output:**
```
3 3 0 0 0 0 0 0 0 0 0 3
```


## train_4

**input:**
```
0 5 5 5 0 5 5 5 0 0 4 1
```


**output:**
```
0 4 4 4 0 1 1 1 0 0 4 1
```


## train_5

**input:**
```
5 5 0 0 0 5 5 0 0 0 5 8
```


**output:**
```
5 5 0 0 0 8 8 0 0 0 5 8
```


## train_6

**input:**
```
5 5 5 0 5 5 5 0 0 0 6 2
```


**output:**
```
6 6 6 0 2 2 2 0 0 0 6 2
```


## train_7

**input:**
```
5 5 5 5 0 0 0 0 0 0 0 2
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 0 2
```

Okay, I will analyze the provided input-output examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are sequences (lists) of 12 integers.
2.  **Key Positions:** The last two integers in the input sequence (`index 10` and `index 11`) appear to act as parameters or control values for the transformation.
3.  **Target Sequence:** The first 10 integers (`index 0` to `index 9`) constitute the primary sequence being modified.
4.  **Target Value:** The integer `5` seems to be the specific value targeted for replacement within the first 10 positions. Other values (specifically `0`) remain unchanged in their positions.
5.  **Replacement Values:** The values from index 10 and index 11 of the input are used to replace the target value (`5`).
6.  **Grouping:** The replacement seems sensitive to contiguous groups (or "runs") of the target value `5`.
7.  **Conditional Replacement Logic:**
    *   If there's only one contiguous group of `5`s in the first 10 positions, the replacement value used depends on the input values at index 10 (`val1`) and index 11 (`val2`). If `val1` is non-zero, it's used; otherwise, `val2` is used.
    *   If there are two contiguous groups of `5`s, the first group is replaced by `val1`, and the second group is replaced by `val2`.
8.  **Preservation:** The values `0` in the first 10 positions and the values at index 10 and 11 are preserved in the output in their original positions.

**Facts:**


```yaml
objects:
  - name: input_sequence
    type: list
    properties:
      length: 12
      elements: integer
  - name: output_sequence
    type: list
    properties:
      length: 12
      elements: integer
  - name: target_subsequence
    type: list slice
    source: input_sequence
    indices: 0-9
  - name: control_values
    type: list slice
    source: input_sequence
    indices: 10-11
    elements:
      - name: val1
        index: 10 (relative to input_sequence)
      - name: val2
        index: 11 (relative to input_sequence)
  - name: target_value
    type: integer
    value: 5
  - name: ignored_value
    type: integer
    value: 0
  - name: groups_of_target
    type: list of list slices
    description: Contiguous sequences of target_value within target_subsequence.

actions:
  - name: identify_groups
    input: target_subsequence, target_value
    output: groups_of_target
    description: Find all contiguous blocks of the target_value.
  - name: generate_output_prefix
    input: target_subsequence, groups_of_target, val1, val2
    output: list (length 10)
    description: >
      Create the first 10 elements of the output by copying the target_subsequence
      and then replacing values within the identified groups based on the number of groups
      and the values of val1 and val2.
      If one group exists: replace with val1 if val1 != 0, else replace with val2.
      If two groups exist: replace first group with val1, second group with val2.
      Leave ignored_value (0) unchanged.
  - name: construct_output
    input: generated_output_prefix, val1, val2
    output: output_sequence
    description: Concatenate the generated_output_prefix with val1 and val2.

relationships:
  - The output_sequence depends on the input_sequence.
  - The transformation primarily affects elements in the target_subsequence that match the target_value.
  - The specific replacement values are determined by control_values (val1, val2).
  - The application logic of control_values depends on the number and position of groups_of_target.
  - Elements equal to ignored_value in the target_subsequence remain unchanged.
  - control_values (val1, val2) are preserved in the last two positions of the output_sequence.

```


**Natural Language Program:**

1.  Accept the input sequence of 12 integers.
2.  Identify the two control values: `val1` is the element at index 10, and `val2` is the element at index 11.
3.  Create a working copy of the first 10 elements of the input sequence.
4.  Scan the working copy to identify the start and end indices of all contiguous groups of the integer `5`. Store these groups.
5.  Count the number of identified groups of `5`s.
6.  If exactly one group was found:
    *   Determine the replacement value: if `val1` is not equal to `0`, use `val1`; otherwise, use `val2`.
    *   Replace all `5`s within that single group in the working copy with the determined replacement value.
7.  If two or more groups were found (examples show only up to two):
    *   Replace all `5`s within the first identified group in the working copy with `val1`.
    *   Replace all `5`s within the second identified group in the working copy with `val2`.
8.  Construct the final output sequence by taking the modified working copy (the first 10 elements) and appending the original `val1` and `val2` to its end.
9.  Return the final output sequence.
```python
import math

def find_contiguous_groups(sub_list, target_value):
    """
    Finds the start and end indices of contiguous groups of a target value in a list.

    Args:
        sub_list: The list to search within.
        target_value: The value to find contiguous groups of.

    Returns:
        A list of tuples, where each tuple contains the (start_index, end_index)
        of a contiguous group. End_index is inclusive.
    """
    groups = []
    start_index = -1
    for i, val in enumerate(sub_list):
        if val == target_value and start_index == -1:
            # Start of a new group
            start_index = i
        elif val != target_value and start_index != -1:
            # End of the current group
            groups.append((start_index, i - 1))
            start_index = -1
    # Check if the list ends with a group
    if start_index != -1:
        groups.append((start_index, len(sub_list) - 1))
    return groups

def transform(input_list):
    """
    Transforms an input list of 12 integers based on the following rules:
    1. The last two integers (index 10 and 11) are control values (val1, val2).
    2. The first 10 integers are the target sequence.
    3. Contiguous groups of the integer 5 within the target sequence are identified.
    4. If one group of 5s is found:
       - It's replaced by val1 if val1 is not 0, otherwise by val2.
    5. If two groups of 5s are found:
       - The first group is replaced by val1.
       - The second group is replaced by val2.
    6. Integers other than 5 (specifically 0) in the target sequence remain unchanged.
    7. The control values (val1, val2) are appended to the end of the modified target sequence.
    """
    # Check if input is a string, split if necessary
    if isinstance(input_list, str):
        input_list = [int(x) for x in input_list.split()]

    # 1. Identify control values
    val1 = input_list[10]
    val2 = input_list[11]

    # 2. Create a working copy of the target sequence
    working_copy = list(input_list[:10])

    # 3. Identify contiguous groups of 5
    target_value = 5
    groups = find_contiguous_groups(working_copy, target_value)

    # 4. Apply replacement logic based on the number of groups
    num_groups = len(groups)

    if num_groups == 1:
        # 4.1. One group found
        replacement_value = val1 if val1 != 0 else val2
        start, end = groups[0]
        for i in range(start, end + 1):
            if working_copy[i] == target_value: # Ensure we only replace the target value
                 working_copy[i] = replacement_value
    elif num_groups >= 2: # Handle cases with 2 or more groups as per examples (up to 2 shown)
        # 4.2. Two groups found (assuming only the first two are relevant based on examples)
        # Replace first group
        start1, end1 = groups[0]
        for i in range(start1, end1 + 1):
             if working_copy[i] == target_value:
                 working_copy[i] = val1
        # Replace second group
        start2, end2 = groups[1]
        for i in range(start2, end2 + 1):
            if working_copy[i] == target_value:
                 working_copy[i] = val2

    # 5 & 6. Other values (0s) remain unchanged as we only modified specific indices.

    # 7. Construct the final output sequence
    output_list = working_copy + [val1, val2]

    return output_list
```
```python
import math
import re # Using re for potential group finding, although manual iteration is also fine

"""
Transforms an input sequence (list or string of 12 integers) based on the following rules:
1. Parses the input into a list of 12 integers.
2. Identifies the last two integers (index 10 and 11) as control values (val1, val2).
3. Focuses on the first 10 integers as the target subsequence.
4. Finds contiguous groups (runs) of the integer 5 within the target subsequence.
5. If exactly one group of 5s is found:
   - Replaces all 5s in that group with val1 if val1 is not 0, otherwise with val2.
6. If two or more groups of 5s are found:
   - Replaces all 5s in the first group with val1.
   - Replaces all 5s in the second group with val2.
   (Assumes transformation logic only applies to the first two groups found if more exist, based on examples).
7. Integers other than 5 (e.g., 0) in the target subsequence remain unchanged.
8. Constructs the final output sequence by appending the original control values (val1, val2) to the modified target subsequence.
"""

def find_contiguous_groups(sub_list, target_value):
    """
    Finds the start and end indices of contiguous groups of a target value in a list.

    Args:
        sub_list: The list to search within.
        target_value: The value to find contiguous groups of.

    Returns:
        A list of tuples, where each tuple contains the (start_index, end_index)
        of a contiguous group. End_index is inclusive. Returns an empty list if no groups found.
    """
    groups = []
    start_index = -1
    for i, val in enumerate(sub_list):
        if val == target_value and start_index == -1:
            # Start of a new group
            start_index = i
        elif val != target_value and start_index != -1:
            # End of the current group (non-inclusive index is i)
            groups.append((start_index, i - 1))
            start_index = -1 # Reset for finding next group

    # Check if the list ends with an ongoing group
    if start_index != -1:
        groups.append((start_index, len(sub_list) - 1))

    return groups

def transform(input_data):
    """
    Applies the transformation rule to the input data.
    """
    # 1. Parse input into a list of 12 integers
    if isinstance(input_data, str):
        # Assuming space-separated integers if input is a string
        try:
            input_list = [int(x) for x in input_data.split()]
        except ValueError:
            raise ValueError("Input string must contain space-separated integers.")
    elif isinstance(input_data, list):
        # Ensure all elements are integers if it's already a list
        if not all(isinstance(x, int) for x in input_data):
             raise ValueError("Input list must contain only integers.")
        input_list = input_data
    else:
        raise TypeError("Input must be a list of integers or a string of space-separated integers.")

    if len(input_list) != 12:
        raise ValueError("Input must contain exactly 12 integers.")

    # 2. Extract control values
    val1 = input_list[10]
    val2 = input_list[11]

    # 3. Isolate the target subsequence and create a modifiable copy
    target_subsequence = list(input_list[:10]) # Make a copy

    # 4. Find contiguous groups of 5
    target_value = 5
    groups = find_contiguous_groups(target_subsequence, target_value)
    num_groups = len(groups)

    # 5. & 6. Apply replacement logic based on the number of groups
    if num_groups == 1:
        # Determine replacement value for the single group
        replacement_value = val1 if val1 != 0 else val2
        start, end = groups[0]
        # Replace 5s within the group
        for i in range(start, end + 1):
            # Check again to ensure we only replace the target value
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = replacement_value

    elif num_groups >= 2:
        # Apply replacement for the first group using val1
        start1, end1 = groups[0]
        for i in range(start1, end1 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val1

        # Apply replacement for the second group using val2
        start2, end2 = groups[1]
        for i in range(start2, end2 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val2

    # 7. Integers other than 5 remain unchanged implicitly as we only modify specific indices/values.

    # 8. Construct the final output sequence
    output_list = target_subsequence + [val1, val2]

    return output_list
```
```python
import math
import re # Although not strictly used in the final version, kept for potential alternative group finding

"""
Transforms an input sequence (list or string of 12 integers) based on the following rules:
1. Parses the input into a list of 12 integers.
2. Identifies the last two integers (index 10 and 11) as control values (val1, val2).
3. Focuses on the first 10 integers as the target subsequence.
4. Finds contiguous groups (runs) of the integer 5 within the target subsequence.
5. If exactly one group of 5s is found:
   - Replaces all 5s in that group with val1 if val1 is not 0, otherwise with val2.
6. If two or more groups of 5s are found:
   - Replaces all 5s in the first group with val1.
   - Replaces all 5s in the second group with val2.
   (Assumes transformation logic only applies to the first two groups found if more exist, based on examples).
7. Integers other than 5 (e.g., 0) in the target subsequence remain unchanged.
8. Constructs the final output sequence by appending the original control values (val1, val2) to the modified target subsequence.
"""

def find_contiguous_groups(sub_list, target_value):
    """
    Helper function to find the start and end indices of contiguous groups of a target value.

    Args:
        sub_list: The list (or list slice) to search within.
        target_value: The integer value to find contiguous groups of.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index) inclusive.
        Returns an empty list if no groups are found.
    """
    groups = []
    start_index = -1
    for i, val in enumerate(sub_list):
        if val == target_value and start_index == -1:
            # Start of a new group
            start_index = i
        elif val != target_value and start_index != -1:
            # End of the current group (non-inclusive index is i)
            groups.append((start_index, i - 1))
            start_index = -1 # Reset for finding next group

    # Check if the list ends with an ongoing group
    if start_index != -1:
        groups.append((start_index, len(sub_list) - 1))

    return groups

def transform(input_data):
    """
    Applies the transformation rule to the input data.
    """
    # 1. Parse Input: Convert input string/list to a list of 12 integers
    if isinstance(input_data, str):
        try:
            input_list = [int(x) for x in input_data.split()]
        except ValueError:
            # Handle cases where splitting or conversion fails
            raise ValueError("Input string must contain 12 space-separated integers.")
    elif isinstance(input_data, list):
        if not all(isinstance(x, int) for x in input_data):
             raise TypeError("Input list must contain only integers.")
        input_list = input_data # Use the list directly
    else:
        raise TypeError("Input must be a list of integers or a string of space-separated integers.")

    # Validate length
    if len(input_list) != 12:
        raise ValueError("Input must contain exactly 12 integers.")

    # 2. Extract Components: Get target sequence and control values
    val1 = input_list[10]
    val2 = input_list[11]
    # Create a mutable copy for modifications
    target_subsequence = list(input_list[:10])

    # 3. Find Target Groups: Identify contiguous runs of '5'
    target_value = 5
    groups = find_contiguous_groups(target_subsequence, target_value)
    num_groups = len(groups)

    # 4. Apply Conditional Replacement: Modify the target subsequence based on groups found
    if num_groups == 1:
        # Case 1: Exactly one group found
        replacement_value = val1 if val1 != 0 else val2
        start, end = groups[0]
        # Replace all 5s within this group's range
        for i in range(start, end + 1):
            if target_subsequence[i] == target_value: # Ensure we only replace the target
                 target_subsequence[i] = replacement_value

    elif num_groups >= 2:
        # Case 2: Two or more groups found (apply logic to first two)
        # Replace first group with val1
        start1, end1 = groups[0]
        for i in range(start1, end1 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val1

        # Replace second group with val2
        start2, end2 = groups[1]
        for i in range(start2, end2 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val2
    # Else (num_groups == 0): No groups found, no changes needed to target_subsequence

    # 5. Construct Output: Combine modified subsequence with original control values
    output_list = target_subsequence + [val1, val2]

    return output_list
```
