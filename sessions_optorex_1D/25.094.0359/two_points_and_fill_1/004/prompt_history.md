
## train_1

**input:**
```
0 0 0 0 0 0 0 5 0 5 0 0
```


**output:**
```
0 0 0 0 0 0 0 5 5 5 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 7 0 0 0 0 7
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 7 7
```


## train_3

**input:**
```
9 0 9 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 9 9 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
4 0 0 0 0 4 0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 4 0 0 0 0 0 0
```


## train_5

**input:**
```
0 6 0 0 0 0 0 0 6 0 0 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 1 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 1 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 7 0 7 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 0 0
```

## Perception

The input is a string representing a list of single-digit integers separated by spaces. The list primarily consists of zeros, with exactly two instances of a non-zero integer (let's call this the 'fill value'). The output is also a string representing a list of integers of the same length. The transformation fills the zeros located *between* the two occurrences of the fill value in the input list with that same fill value. The original positions of the fill value and any zeros outside this range remain unchanged.

## Facts


```yaml
task_elements:
  - object: input_list
    type: List[int]
    description: A list derived from the input string, containing mostly zeros and exactly two instances of a single non-zero integer.
  - object: output_list
    type: List[int]
    description: A list derived from the output string, representing the transformed state of the input list.
  - property: fill_value
    type: int
    description: The single non-zero integer present in the input_list.
    value_determination: Find the first non-zero element in the input_list.
  - property: first_occurrence_index
    type: int
    description: The index of the first appearance of the fill_value in the input_list.
  - property: second_occurrence_index
    type: int
    description: The index of the second appearance of the fill_value in the input_list.
  - relationship: containment
    description: The fill_value is contained within the input_list exactly twice.
  - action: fill_segment
    description: Replace elements in the list between the first_occurrence_index and the second_occurrence_index.
    target_object: output_list (initially a copy of input_list)
    condition: Affects only elements whose index `i` satisfies `first_occurrence_index < i < second_occurrence_index`.
    value_used: fill_value
```


## Natural Language Program

1.  Parse the input string into a list of integers.
2.  Identify the non-zero integer (`fill_value`) present in the list.
3.  Find the index of the first occurrence (`idx1`) of the `fill_value`.
4.  Find the index of the second occurrence (`idx2`) of the `fill_value`.
5.  Create a copy of the input list to serve as the initial output list.
6.  Iterate through the indices `i` from `idx1 + 1` up to (but not including) `idx2`.
7.  For each index `i` in this range, set the element at index `i` in the output list to the `fill_value`.
8.  Format the modified list back into a space-separated string for the final output.
```python
import math

"""
Identifies the single non-zero digit ('fill_value') present exactly twice in the input list. 
Fills the elements between the first and second occurrences of the 'fill_value' with the 'fill_value' itself. 
Elements outside this range remain unchanged.
"""

def find_first(lst, value):
    """Helper function to find the first index of a value in a list."""
    for i, x in enumerate(lst):
        if x == value:
            return i
    return -1 # Should not happen based on problem description

def find_last(lst, value):
    """Helper function to find the last index of a value in a list."""
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == value:
            return i
    return -1 # Should not happen based on problem description

def transform(input_str: str) -> str:
    """
    Transforms the input string list by filling zeros between two occurrences 
    of a non-zero digit with that digit.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Identify the non-zero integer (fill_value).
    fill_value = 0
    for x in input_list:
        if x != 0:
            fill_value = x
            break # Found the first non-zero, which is the fill value

    # Check if a fill_value was found (handles edge case of all zeros, though not expected)
    if fill_value == 0:
        return input_str # No non-zero value, return original string

    # 3. Find the index of the first occurrence (idx1).
    idx1 = find_first(input_list, fill_value)

    # 4. Find the index of the second occurrence (idx2).
    # We search from idx1 + 1 onwards to ensure we find the *second* occurrence.
    # A simpler way is to find the *last* occurrence, as there are only two.
    idx2 = find_last(input_list, fill_value)

    # 5. Create a copy of the input list to serve as the initial output list.
    output_list = list(input_list)

    # 6. Iterate through the indices i from idx1 + 1 up to (but not including) idx2.
    # 7. For each index i in this range, set the element at index i in the output list to the fill_value.
    if idx1 != -1 and idx2 != -1 and idx1 < idx2: # Ensure both found and in correct order
        for i in range(idx1 + 1, idx2):
            output_list[i] = fill_value

    # 8. Format the modified list back into a space-separated string for the final output.
    output_str = " ".join(map(str, output_list))

    return output_str

```
```python
import math # Although math isn't strictly needed here, it's included as per template instructions
import copy # Used for creating a mutable copy of the input

"""
Identifies the single non-zero digit ('fill_value') present exactly twice in the input list. 
Fills the elements between the first and second occurrences of the 'fill_value' with the 'fill_value' itself. 
Elements outside this range remain unchanged. The input is assumed to be a list or list-like structure (e.g., NumPy array) of integers.
"""

def find_first(lst, value):
    """Helper function to find the first index of a value in a list."""
    for i, x in enumerate(lst):
        if x == value:
            return i
    return -1 # Should not happen based on problem description

def find_last(lst, value):
    """Helper function to find the last index of a value in a list."""
    # Iterate backwards to find the last occurrence efficiently
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == value:
            return i
    return -1 # Should not happen based on problem description

def transform(input_list):
    """
    Transforms the input list by filling elements between the two occurrences 
    of a unique non-zero digit with that digit.

    Args:
        input_list: A list or list-like structure of integers.

    Returns:
        A new list with the transformation applied.
    """
    # Ensure we are working with a standard Python list if input is array-like
    # and create a mutable copy for the output.
    # Using deepcopy handles potential nested structures, although simple list() or copy.copy()
    # would work for a flat list of ints. Using copy.deepcopy for robustness.
    output_list = copy.deepcopy(list(input_list)) 

    # 1. Identify the non-zero integer (fill_value).
    # Based on the problem description, there's exactly one unique non-zero value.
    fill_value = 0
    for x in output_list: # Iterate through the list to find the first non-zero
        if x != 0:
            fill_value = x
            break # Found the fill value, no need to continue search

    # Handle edge case: if no non-zero value found (not expected from examples)
    if fill_value == 0:
        return output_list # Return the original list copy

    # 2. Find the index of the first occurrence (idx1).
    idx1 = find_first(output_list, fill_value)

    # 3. Find the index of the last occurrence (idx2).
    idx2 = find_last(output_list, fill_value)

    # 4. Iterate through the indices i from idx1 + 1 up to (but not including) idx2.
    # 5. For each index i in this range, set the element at index i in the output list to the fill_value.
    # Check if both indices were found and idx1 is before idx2 (as expected)
    if idx1 != -1 and idx2 != -1 and idx1 < idx2:
        for i in range(idx1 + 1, idx2):
            output_list[i] = fill_value

    # 6. Return the modified output list.
    return output_list
```
