
## train_1

**input:**
```
0 0 1 0 0 1 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 0 0 0 0 0
```


## train_2

**input:**
```
0 7 0 0 7 0 7 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 7 7
```


## train_3

**input:**
```
3 3 3 3 3 3 3 0 3 0 0 3
```


**output:**
```
3 3 3 3 3 3 3 0 0 0 0 0
```


## train_4

**input:**
```
0 6 6 6 6 6 6 0 6 0 0 0
```


**output:**
```
0 6 6 6 6 6 6 0 0 0 0 0
```


## train_5

**input:**
```
8 8 8 8 0 0 8 0 0 8 0 0
```


**output:**
```
8 8 8 8 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 7 0 0 7 7 7 7 0 7 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 0 0 0
```


## train_7

**input:**
```
4 0 4 0 0 4 4 4 4 4 0 4
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```

## Perception

The task involves transforming an input sequence of 12 integers into an output sequence of the same length. The transformation logic focuses on identifying contiguous blocks (groups) of non-zero numbers within the input sequence. The core operation is to filter these groups based on their length, keeping only the longest group(s) and replacing all other elements (including shorter non-zero groups and original zeros) with zeros in the output.

**Observations:**

1.  **Input/Output Format:** Both input and output are fixed-length sequences (length 12) of single-digit integers.
2.  **Grouping:** The key operation involves identifying contiguous runs of non-zero numbers. Zeros act as separators between these groups. The specific non-zero value within a group does not seem to affect the grouping itself, only its distinction from zero.
3.  **Filtering Logic:** The primary criterion for keeping a group is its length (number of consecutive non-zero elements). Only the group(s) with the maximum length found in the input sequence are preserved in the output.
4.  **Output Construction:** The output sequence is constructed by placing the longest group(s) from the input into an initially zero-filled sequence at their original positions. Elements belonging to shorter non-zero groups or original zero elements become zero in the output.

## Facts


```yaml
objects:
  - name: sequence
    properties:
      - type: list of integers
      - length: 12
      - elements: integers (0-9 observed)
  - name: group
    properties:
      - type: contiguous sub-sequence
      - composition: consists of one or more non-zero integers
      - boundaries: delimited by zeros or sequence ends
      - attributes:
          - start_index: integer
          - end_index: integer
          - length: integer (number of elements)
          - elements: list of non-zero integers from the input sequence

actions:
  - name: identify_groups
    description: Scan the input sequence to find all contiguous groups of non-zero numbers.
    inputs:
      - input_sequence: sequence
    outputs:
      - list_of_groups: list of group objects (each with start_index, end_index, length)
  - name: find_max_length
    description: Determine the maximum length among all identified groups.
    inputs:
      - list_of_groups: list of group objects
    outputs:
      - max_length: integer
  - name: filter_groups
    description: Select only those groups whose length equals the maximum length.
    inputs:
      - list_of_groups: list of group objects
      - max_length: integer
    outputs:
      - longest_groups: list of group objects
  - name: construct_output
    description: Create the output sequence by placing the elements of the longest groups at their original positions in a sequence otherwise filled with zeros.
    inputs:
      - input_sequence: sequence
      - longest_groups: list of group objects
      - sequence_length: integer (e.g., 12)
    outputs:
      - output_sequence: sequence

relationships:
  - A group's elements are a subset of the input sequence's elements.
  - The output sequence preserves elements from the input sequence only if they belong to a group with the maximum length.
  - All other positions in the output sequence are filled with zero.
```


## Natural Language Program

1.  Initialize an empty list to store information about identified non-zero groups (start index, end index, length).
2.  Iterate through the input sequence, identifying the start and end indices of each contiguous group of non-zero numbers. For each group found, record its start index, end index, and calculate its length. Add this information to the list of groups.
3.  If no non-zero groups are found, the output is a sequence of zeros of the same length as the input.
4.  If groups were found, determine the maximum length among all recorded groups.
5.  Initialize an output sequence of the same length as the input, filled entirely with zeros.
6.  Iterate through the recorded list of groups. For each group whose length is equal to the determined maximum length:
    a.  Retrieve the segment of the original input sequence corresponding to this group (from its start index to its end index).
    b.  Copy this segment into the output sequence at the same indices.
7.  Return the constructed output sequence.
```python
import math # Not used, but potentially useful for more complex tasks
from typing import List, Dict, Tuple

# Docstring at the top level of the module
"""
Transforms an input sequence of integers by identifying contiguous groups of 
non-zero numbers. It determines the maximum length among these groups and 
constructs an output sequence containing only the elements from the group(s) 
with the maximum length, placed at their original positions. All other 
elements in the output sequence are set to zero.
"""

def find_groups(sequence: List[int]) -> List[Dict[str, int]]:
    """
    Helper function to find contiguous non-zero groups in a sequence.

    Args:
        sequence: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start', 'end', and 'length' keys.
    """
    groups = []
    current_start = None
    n = len(sequence)

    for i, val in enumerate(sequence):
        # Start of a new group
        if val != 0 and current_start is None:
            current_start = i
            
        # End of a group (found a zero after a non-zero group started)
        elif val == 0 and current_start is not None:
            end_index = i - 1
            length = end_index - current_start + 1
            groups.append({'start': current_start, 'end': end_index, 'length': length})
            current_start = None # Reset for the next potential group

    # Handle case where a group extends to the very end of the sequence
    if current_start is not None:
        end_index = n - 1
        length = end_index - current_start + 1
        groups.append({'start': current_start, 'end': end_index, 'length': length})
        
    return groups

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    1. Finds all contiguous groups of non-zero numbers.
    2. Determines the maximum length among these groups.
    3. Creates an output sequence preserving only the elements of the longest group(s)
       at their original positions, filling the rest with zeros.

    Args:
        input_sequence: The input list of integers.

    Returns:
        The transformed list of integers.
    """
    n = len(input_sequence)

    # Step 1 & 2 (from NL program): Identify groups
    groups = find_groups(input_sequence)

    # Step 3: Handle case with no non-zero groups
    if not groups:
        return [0] * n

    # Step 4: Determine the maximum length
    # Handles the case where groups might be empty, defaulting to 0
    max_length = max((group['length'] for group in groups), default=0) 

    # Step 5: Initialize output sequence with zeros
    output_sequence = [0] * n

    # Step 6: Iterate through groups and populate output with longest ones
    for group in groups:
        # Check if the current group's length matches the maximum
        if group['length'] == max_length:
            start = group['start']
            end = group['end']
            # Copy the segment from input_sequence to output_sequence using slicing
            output_sequence[start : end + 1] = input_sequence[start : end + 1]

    # Step 7: Return the constructed output sequence
    return output_sequence
```
```python
"""
Transforms an input sequence of integers by identifying contiguous groups of 
non-zero numbers. It determines the maximum length among these groups and 
constructs an output sequence containing only the elements from the group(s) 
with the maximum length, placed at their original positions. All other 
elements in the output sequence are set to zero.
"""

from typing import List, Dict, Tuple

def find_groups(sequence: List[int]) -> List[Dict[str, int]]:
    """
    Helper function to find contiguous non-zero groups in a sequence.

    Args:
        sequence: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start', 'end', and 'length' keys.
    """
    groups = []
    current_start = None
    n = len(sequence)

    for i, val in enumerate(sequence):
        # Start of a new group: non-zero value and not currently in a group
        if val != 0 and current_start is None:
            current_start = i
            
        # End of a group: zero value encountered OR end of sequence, while inside a group
        elif (val == 0 or i == n - 1) and current_start is not None:
            # Determine the correct end index
            # If we hit a zero, the group ended at the previous index (i-1)
            # If we hit the end of the sequence AND the last element was non-zero, the group ends at the last index (i or n-1)
            end_index = i - 1 if val == 0 else i 
            
            # Calculate length
            length = end_index - current_start + 1
            
            # Store group info
            groups.append({'start': current_start, 'end': end_index, 'length': length})
            
            # Reset state
            current_start = None 
            
    # Note: The original `find_groups` had a separate check after the loop. 
    # This revised version handles the end-of-sequence case within the loop's final iteration.
        
    return groups

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.
    """
    n = len(input_sequence)

    # Step 1 & 2 (from NL program): Identify all contiguous groups of non-zero numbers
    groups = find_groups(input_sequence)

    # Step 3: Handle case where no non-zero groups are found
    if not groups:
        # If no groups, the output is all zeros
        return [0] * n

    # Step 4: Determine the maximum length among all identified groups
    # Use a generator expression for efficiency, default to 0 if groups is empty (though handled above)
    max_length = max((group['length'] for group in groups), default=0) 

    # Step 5: Initialize an output sequence of the same length as the input, filled with zeros
    output_sequence = [0] * n

    # Step 6 & 7: Iterate through the recorded groups. If a group's length equals the maximum,
    # copy its elements from the input sequence to the output sequence at the same positions.
    for group in groups:
        # Check if the current group is one of the longest
        if group['length'] == max_length:
            start = group['start']
            end = group['end']
            # Copy the segment from the original input_sequence to the output_sequence
            # Slicing handles the start and end indices correctly (end+1 because slice upper bound is exclusive)
            output_sequence[start : end + 1] = input_sequence[start : end + 1]

    # Step 8: Return the constructed output sequence
    return output_sequence
```

Previous Code:
```python
"""
Transforms an input sequence of integers by identifying contiguous groups of 
non-zero numbers. It determines the maximum length among these groups and 
constructs an output sequence containing only the elements from the group(s) 
with the maximum length, placed at their original positions. All other 
elements in the output sequence are set to zero.
"""

from typing import List, Dict, Tuple

def find_groups(sequence: List[int]) -> List[Dict[str, int]]:
    """
    Helper function to find contiguous non-zero groups in a sequence.

    Args:
        sequence: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start', 'end', and 'length' keys.
    """
    groups = []
    current_start = None
    n = len(sequence)

    for i, val in enumerate(sequence):
        # Start of a new group: non-zero value and not currently in a group
        if val != 0 and current_start is None:
            current_start = i
            
        # End of a group: zero value encountered OR end of sequence, while inside a group
        elif (val == 0 or i == n - 1) and current_start is not None:
            # Determine the correct end index
            # If we hit a zero, the group ended at the previous index (i-1)
            # If we hit the end of the sequence AND the last element was non-zero, the group ends at the last index (i or n-1)
            end_index = i - 1 if val == 0 else i 
            
            # Calculate length
            length = end_index - current_start + 1
            
            # Store group info
            groups.append({'start': current_start, 'end': end_index, 'length': length})
            
            # Reset state
            current_start = None 
            
    # Note: The original `find_groups` had a separate check after the loop. 
    # This revised version handles the end-of-sequence case within the loop's final iteration.
        
    return groups

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.
    """
    n = len(input_sequence)

    # Step 1 & 2 (from NL program): Identify all contiguous groups of non-zero numbers
    groups = find_groups(input_sequence)

    # Step 3: Handle case where no non-zero groups are found
    if not groups:
        # If no groups, the output is all zeros
        return [0] * n

    # Step 4: Determine the maximum length among all identified groups
    # Use a generator expression for efficiency, default to 0 if groups is empty (though handled above)
    max_length = max((group['length'] for group in groups), default=0) 

    # Step 5: Initialize an output sequence of the same length as the input, filled with zeros
    output_sequence = [0] * n

    # Step 6 & 7: Iterate through the recorded groups. If a group's length equals the maximum,
    # copy its elements from the input sequence to the output sequence at the same positions.
    for group in groups:
        # Check if the current group is one of the longest
        if group['length'] == max_length:
            start = group['start']
            end = group['end']
            # Copy the segment from the original input_sequence to the output_sequence
            # Slicing handles the start and end indices correctly (end+1 because slice upper bound is exclusive)
            output_sequence[start : end + 1] = input_sequence[start : end + 1]

    # Step 8: Return the constructed output sequence
    return output_sequence
```
Results for code_00.py:

Train Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 2:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 3:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 4:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 5:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 6:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 7:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

Test Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
## General Assessment

The provided execution results indicate a consistent failure across all examples with the error "The truth value of an array with more than one element is ambiguous." This strongly suggests that the `transform` function, while logically designed for Python lists based on the initial perception, was executed in an environment where the input sequences were NumPy arrays. Standard Python boolean checks (like implicit truthiness checks or potentially certain conditional logic constructs if they were present) can fail when applied directly to multi-element NumPy arrays.

However, simulating the intended logic (find contiguous non-zero groups, determine max length, keep only groups matching max length) against each training example shows that this core logic *does* correctly produce the desired output for all cases.

Therefore, the strategy is to:
1.  Confirm the core transformation logic using metrics gathered from the examples.
2.  Refine the documentation (Facts and Natural Language Program) to accurately reflect this confirmed logic.
3.  Assume the coder will adapt the implementation to handle the input type correctly (either by ensuring list input or by using NumPy-compatible operations) based on the clear description of the logic.

## Metrics

Based on manual analysis and simulation of the core logic (find non-zero groups, find max length, filter):

| Example | Input                                     | Groups (Start, End, Length)                               | Max Length | Longest Group(s) (Start, End) | Predicted Output                          | Matches Target |
| :------ | :---------------------------------------- | :-------------------------------------------------------- | :--------- | :-------------------------- | :---------------------------------------- | :------------- |
| train_1 | `[0,0,1,0,0,1,1,0,0,0,0,0]`               | `(2,2,1), (5,6,2)`                                        | 2          | `(5,6)`                     | `[0,0,0,0,0,1,1,0,0,0,0,0]`               | Yes            |
| train_2 | `[0,7,0,0,7,0,7,7,7,7,7,7]`               | `(1,1,1), (4,4,1), (6,11,6)`                              | 6          | `(6,11)`                    | `[0,0,0,0,0,0,7,7,7,7,7,7]`               | Yes            |
| train_3 | `[3,3,3,3,3,3,3,0,3,0,0,3]`               | `(0,6,7), (8,8,1), (11,11,1)`                             | 7          | `(0,6)`                     | `[3,3,3,3,3,3,3,0,0,0,0,0]`               | Yes            |
| train_4 | `[0,6,6,6,6,6,6,0,6,0,0,0]`               | `(1,6,6), (8,8,1)`                                        | 6          | `(1,6)`                     | `[0,6,6,6,6,6,6,0,0,0,0,0]`               | Yes            |
| train_5 | `[8,8,8,8,0,0,8,0,0,8,0,0]`               | `(0,3,4), (6,6,1), (9,9,1)`                               | 4          | `(0,3)`                     | `[8,8,8,8,0,0,0,0,0,0,0,0]`               | Yes            |
| train_6 | `[0,0,7,0,0,7,7,7,7,0,7,0]`               | `(2,2,1), (5,8,4), (10,10,1)`                             | 4          | `(5,8)`                     | `[0,0,0,0,0,7,7,7,7,0,0,0]`               | Yes            |
| train_7 | `[4,0,4,0,0,4,4,4,4,4,0,4]`               | `(0,0,1), (2,2,1), (5,9,5), (11,11,1)`                    | 5          | `(5,9)`                     | `[0,0,0,0,0,4,4,4,4,4,0,0]`               | Yes            |

The analysis confirms the "keep only the longest contiguous non-zero group(s)" logic correctly explains the transformation for all training examples. The implementation failure was likely due to type incompatibility (NumPy vs. List) in the execution environment, not a flaw in the intended algorithm.

## Facts


```yaml
objects:
  - name: sequence
    properties:
      - type: list or 1D array of integers
      - length: 12 (fixed in examples)
      - elements: integers (0 represents a separator/absence, non-zero represents content)
  - name: group
    properties:
      - type: contiguous sub-sequence within the input sequence
      - composition: consists only of non-zero integers
      - boundaries: delimited by zeros or the sequence ends
      - attributes:
          - start_index: integer (0-based index of the first element)
          - end_index: integer (0-based index of the last element)
          - length: integer (number of elements in the group)
          - elements: the actual non-zero integer values from the input sequence belonging to this group

actions:
  - name: identify_groups
    description: Scan the input sequence to find all contiguous groups of non-zero numbers.
    inputs:
      - input_sequence: sequence
    outputs:
      - list_of_groups: list of group objects (each with start_index, end_index, length, and potentially elements)
  - name: find_max_group_length
    description: Determine the maximum length among all identified groups. Returns 0 if no groups exist.
    inputs:
      - list_of_groups: list of group objects
    outputs:
      - max_length: integer
  - name: filter_longest_groups
    description: Select only those groups from the list whose length equals the maximum length.
    inputs:
      - list_of_groups: list of group objects
      - max_length: integer
    outputs:
      - longest_groups: list of group objects (containing only groups with length == max_length)
  - name: construct_output
    description: Create the output sequence. Initialize it with zeros. Then, for each group in the 'longest_groups' list, copy its original elements from the input sequence into the corresponding positions in the output sequence.
    inputs:
      - input_sequence: sequence (needed to retrieve original elements)
      - longest_groups: list of group objects (identified as having the max length)
      - sequence_length: integer (length of the input/output sequence)
    outputs:
      - output_sequence: sequence (same length as input, containing only elements from the longest groups, zeros elsewhere)

relationships:
  - The output sequence has the same length as the input sequence.
  - Elements in the output sequence are either zero or are identical to elements from the input sequence.
  - A non-zero element appears in the output sequence *if and only if* it was part of a contiguous non-zero group in the input sequence, *and* that group's length was equal to the maximum length found among *all* contiguous non-zero groups in the input sequence.
  - If multiple groups share the maximum length, all of them are preserved in the output.
  - If the input contains no non-zero elements, the output consists entirely of zeros.
```


## Natural Language Program

1.  Receive the input sequence (assume it's a list or array of 12 integers).
2.  Initialize an empty list to store details of identified non-zero groups.
3.  Iterate through the input sequence from start to end:
    a.  If a non-zero number is encountered and we are not currently tracking a group, mark the current index as the start of a new group.
    b.  If a zero is encountered or the end of the sequence is reached while tracking a group, mark the end of the current group (at the previous index if a zero was found, or the current index if the end of the sequence was reached with a non-zero number). Calculate the group's length (end index - start index + 1). Record the group's start index, end index, and length in the list of groups. Stop tracking the group.
4.  After scanning the entire sequence, check the list of identified groups.
5.  If the list of groups is empty (meaning the input sequence contained only zeros), create an output sequence of the same length filled entirely with zeros and return it.
6.  If groups were found, calculate the `max_length` by finding the maximum value among the 'length' attributes of all recorded groups.
7.  Create a new output sequence of the same length as the input, initially filled entirely with zeros.
8.  Iterate through the recorded list of groups again.
9.  For each group, compare its 'length' to the `max_length`.
10. If a group's length equals `max_length`:
    a.  Identify the segment of the *original input sequence* corresponding to this group's `start_index` and `end_index`.
    b.  Copy this segment of values into the `output_sequence` at the exact same indices (from `start_index` to `end_index`, inclusive).
11. After checking all groups, return the final `output_sequence`.
