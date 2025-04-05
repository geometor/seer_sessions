
## train_1

**input:**
```
0 0 4 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 5 5 5 5 0 0 0
```


**output:**
```
0 0 0 0 0 5 0 0 5 0 0 0
```


## train_3

**input:**
```
4 4 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
4 0 0 0 0 4 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 7 7 7 7 0 0
```


**output:**
```
0 0 0 0 0 0 7 0 0 7 0 0
```


## train_6

**input:**
```
0 0 9 9 9 9 9 9 9 9 9 9
```


**output:**
```
0 0 9 0 0 0 0 0 0 0 0 9
```


## train_7

**input:**
```
6 6 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
6 0 0 0 0 6 0 0 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a 1D sequence of single-digit integers. The input sequences contain blocks (contiguous runs) of identical non-zero digits, surrounded by zeros. The transformation rule appears to operate specifically on these non-zero blocks. By comparing the input and output sequences across the examples, a pattern emerges:

1.  **Identification of Blocks:** The core operation is identifying contiguous sequences of the *same non-zero* digit.
2.  **Length Dependency:** The transformation applied to a block depends on its length.
3.  **Modification Rule:** If a block's length is greater than 2, only the first and last elements of the block are retained in their original positions in the output. All the elements *between* the first and last elements of that block are replaced with 0.
4.  **Short Blocks:** If a block's length is 2 or less (as seen in `train_1` and `train_4`), the block remains unchanged in the output.
5.  **Zeros:** Zeros in the input that are not part of the identified non-zero blocks remain unchanged in the output.

## YAML Fact Documentation


```yaml
Objects:
  - Sequence:
      description: A 1D list of single-digit integers.
      roles: [Input, Output]
  - Element:
      description: A single integer within a sequence (0-9).
  - Group:
      description: A contiguous subsequence of identical non-zero Elements within the Input Sequence.
      properties:
        - value: The non-zero integer that makes up the group.
        - start_index: The index of the first element of the group in the Input Sequence.
        - end_index: The index of the last element of the group in the Input Sequence.
        - length: The number of elements in the group (end_index - start_index + 1).

Relationships:
  - An Input Sequence is transformed into an Output Sequence.
  - A Group is identified within the Input Sequence.
  - The transformation rule depends on the `length` property of the Group.

Actions:
  - Identify_Groups: Scan the Input Sequence to find all Groups, noting their value, start_index, end_index, and length.
  - Modify_Sequence: Create a copy of the Input Sequence. For each identified Group:
      - Condition: Check if the Group's `length` is greater than 2.
      - If True:
          - Modify the copied sequence by setting the elements from `start_index + 1` up to `end_index - 1` (inclusive) to 0.
      - If False:
          - Make no changes to the copied sequence for this Group.
  - Output: Return the modified sequence.
```


## Natural Language Program

1.  Initialize the output sequence as a copy of the input sequence.
2.  Iterate through the input sequence to identify all contiguous groups of identical non-zero numbers. For each group found, record its starting index, ending index, and length.
3.  For each identified group:
    a.  Check if the length of the group is greater than 2.
    b.  If the length is greater than 2, then iterate through the indices of the output sequence starting from the index *after* the group's start index up to the index *before* the group's end index. Set the value at each of these indices in the output sequence to 0.
4.  Return the final output sequence.
```python
import copy

def find_groups(sequence):
    """
    Identifies contiguous groups of identical non-zero numbers in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'value', 'start_index', 'end_index', and 'length'.
    """
    groups = []
    i = 0
    n = len(sequence)
    while i < n:
        if sequence[i] != 0:
            value = sequence[i]
            start_index = i
            # Find the end of the group
            j = i + 1
            while j < n and sequence[j] == value:
                j += 1
            end_index = j - 1
            length = end_index - start_index + 1
            groups.append({
                'value': value,
                'start_index': start_index,
                'end_index': end_index,
                'length': length
            })
            # Move the main index past this group
            i = end_index + 1
        else:
            # Move to the next element if it's zero
            i += 1
    return groups

def transform(input_sequence):
    """
    Transforms the input sequence based on identified groups of non-zero numbers.
    If a contiguous group of the same non-zero number has a length greater than 2,
    only the first and last elements of the group are kept, and the elements
    in between are replaced with 0. Groups of length 2 or less remain unchanged.
    Zeros outside of these groups also remain unchanged.
    """
    
    # Initialize the output sequence as a copy of the input sequence.
    # Using list() creates a shallow copy, which is sufficient here as elements are integers.
    output_sequence = list(input_sequence) 
    
    # Iterate through the input sequence to identify all contiguous groups 
    # of identical non-zero numbers.
    groups = find_groups(input_sequence)
    
    # For each identified group:
    for group in groups:
        # Check if the length of the group is greater than 2.
        if group['length'] > 2:
            # If the length is greater than 2, then iterate through the indices 
            # of the output sequence starting from the index *after* the group's 
            # start index up to the index *before* the group's end index.
            # Set the value at each of these indices in the output sequence to 0.
            # range(start, stop) goes up to stop-1, so range(start+1, end) is correct.
            for i in range(group['start_index'] + 1, group['end_index']):
                output_sequence[i] = 0
                
    # Return the final output sequence.
    return output_sequence

```
```python
"""
Transforms a 1D NumPy array of integers. It identifies contiguous groups of 
identical non-zero numbers. If a group's length is greater than 2, only the 
first and last elements of the group are kept in their original positions in 
the output array, and the elements between them are replaced with 0. Groups 
of length 2 or less, and zeros outside of these groups, remain unchanged.
"""

import numpy as np

def find_groups_np(sequence):
    """
    Identifies contiguous groups of identical non-zero numbers in a 1D NumPy array.

    Args:
        sequence: A 1D NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'value', 'start_index', 'end_index', and 'length'.
    """
    groups = []
    i = 0
    n = len(sequence)
    while i < n:
        # Check if the current element is non-zero
        if sequence[i] != 0:
            value = sequence[i]
            start_index = i
            
            # Find the end of the contiguous group of the same value
            j = i + 1
            while j < n and sequence[j] == value:
                j += 1
            end_index = j - 1 # Inclusive index of the last element
            length = end_index - start_index + 1
            
            # Record the found group
            groups.append({
                'value': value,
                'start_index': start_index,
                'end_index': end_index,
                'length': length
            })
            
            # Move the main index past this group
            i = end_index + 1
        else:
            # Move to the next element if it's zero
            i += 1
    return groups

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array with the transformation applied.
    """
    # Create a copy of the input array to serve as the output array.
    output_grid = np.copy(input_grid)
    
    # Find all contiguous groups of identical non-zero numbers.
    groups = find_groups_np(input_grid)
    
    # Iterate through each identified group.
    for group in groups:
        # Check if the length of the group is greater than 2.
        if group['length'] > 2:
            # If the length is greater than 2, set the elements in the 
            # output array from index start_index + 1 up to 
            # (but not including) end_index to 0 using array slicing.
            # Note: Python slicing is exclusive of the end index, 
            # so group['end_index'] is the correct upper bound.
            start_modify = group['start_index'] + 1
            end_modify = group['end_index'] 
            if start_modify < end_modify: # Ensure there are elements to modify
                 output_grid[start_modify:end_modify] = 0
                 
    # Return the modified output array.
    return output_grid
```
