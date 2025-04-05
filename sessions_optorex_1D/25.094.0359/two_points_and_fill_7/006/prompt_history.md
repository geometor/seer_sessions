
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 2 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 2 2
```


## train_2

**input:**
```
0 2 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 2 2 2 2 2 2 2 0 0 0 0
```


## train_3

**input:**
```
2 0 0 0 0 2 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 0 0 0 0 0 0
```


## train_4

**input:**
```
4 0 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 1 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 0 0
```


## train_6

**input:**
```
0 7 0 0 0 0 0 7 0 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 7 0 0 0 0
```


## train_7

**input:**
```
0 0 3 0 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 0 0 0 0 0 0 0
```

## Perception of Elements:

The task involves processing a one-dimensional array (list) of single-digit integers. The core operation seems to be identifying specific patterns of non-zero numbers and modifying the zeros located between them. The key elements are:
1.  **Input/Output:** A list of integers.
2.  **Significant Values:** Non-zero integers. The value `0` acts as a placeholder or gap filler.
3.  **Pattern:** The presence of exactly two instances of the *same* non-zero integer within the list.
4.  **Action:** Filling the sequence of zeros (`0`) located *between* these two identical non-zero integers with the value of those integers.
5.  **Condition:** This filling action only occurs if there are precisely two instances of a specific non-zero digit. If the non-zero digits are adjacent (no zeros between them), or if there's only one instance, or more than two instances, or multiple different non-zero digits, the input remains unchanged.

## YAML Facts:


```yaml
objects:
  - name: input_array
    type: list
    contains: integers (0-9)
  - name: output_array
    type: list
    contains: integers (0-9)
  - name: non_zero_digit
    type: integer
    properties:
      - value > 0
      - count_in_array
      - indices_in_array
  - name: zero_digit
    type: integer
    properties:
      - value == 0
      - acts_as_gap

relationships:
  - type: spatial
    description: Zeros located between two instances of the same non_zero_digit.
  - type: conditional
    description: The transformation depends on the count of each unique non_zero_digit.

actions:
  - name: identify_non_zero_digits
    input: input_array
    output: list of unique non_zero_digits and their indices
  - name: count_occurrences
    input: unique non_zero_digit, input_array
    output: count
  - name: find_indices
    input: unique non_zero_digit, input_array
    output: list of indices
  - name: fill_gap
    input: array, start_index, end_index, fill_value
    output: modified_array
    condition: >
      A unique non_zero_digit occurs exactly twice.
      The start_index and end_index correspond to the positions of this digit.
      The fill_value is the value of this digit.

goal:
  - Transform input_array to output_array by conditionally filling gaps between pairs of identical non-zero digits.
```


## Natural Language Program:

1.  Examine the input array to identify all unique non-zero digits present.
2.  For each unique non-zero digit identified:
    a.  Count how many times this digit appears in the input array.
    b.  If the count is exactly two:
        i.  Find the first index (`idx1`) and the second index (`idx2`) where this digit appears.
        ii. Create a copy of the input array.
        iii. Change the value of all elements in the copied array from index `idx1 + 1` up to (but not including) index `idx2` to the value of the non-zero digit identified in step 2.
        iv. Return this modified array as the output.
3.  If, after checking all unique non-zero digits, none were found to occur exactly twice, return the original input array unchanged.
```python
import collections
import numpy as np # numpy might be useful for more complex array operations if needed later

"""
Transforms the input list by finding the first unique non-zero digit that appears exactly twice. 
If such a digit is found, it fills the elements between its two occurrences with the digit's value. 
If no such digit exists, the original list is returned unchanged.
"""

def find_indices(arr, value):
  """
  Helper function to find all indices of a specific value in a list.

  Args:
    arr: The list to search within.
    value: The value to find indices for.

  Returns:
    A list of indices where the value occurs.
  """
  return [i for i, x in enumerate(arr) if x == value]

def transform(input_list):
  """
  Applies the transformation rule to the input list.

  Args:
    input_list: A list of integers.

  Returns:
    A new list representing the transformed output.
  """
  # Create a copy of the input list to potentially modify
  output_list = list(input_list)

  # Find unique non-zero digits present in the input list
  # Using an ordered dict preserves insertion order which might be important if multiple digits qualify
  # although the prompt implies returning after the first match.
  # A set is simpler if order doesn't matter: non_zero_digits = set(x for x in input_list if x != 0)
  unique_digits = collections.OrderedDict()
  for x in input_list:
      if x != 0:
          unique_digits[x] = None # Store unique non-zero digits in order of appearance

  # Iterate through each unique non-zero digit found
  for digit in unique_digits.keys():
    # Find all indices where this digit appears in the original input list
    indices = find_indices(input_list, digit)

    # Check if the digit occurs exactly twice
    if len(indices) == 2:
      # Get the first and second index
      idx1, idx2 = indices[0], indices[1]

      # Fill the gap in the output_list between the two indices
      # The range starts from the element *after* the first occurrence (idx1 + 1)
      # and goes up to (but does not include) the second occurrence (idx2).
      for i in range(idx1 + 1, idx2):
        output_list[i] = digit

      # According to the natural language program and examples,
      # we return immediately after finding and processing the first valid pair.
      return output_list

  # If the loop completes without finding any digit that occurred exactly twice,
  # it means no transformation should be applied.
  # Return the unmodified copy (which is identical to the input in this case).
  return output_list
```
```python
import collections

"""
Transforms an input list of integers based on the following rule:
1. Identify all unique non-zero digits and the indices where they appear.
2. Check if any non-zero digit appears exactly twice in the list.
3. If one or more digits appear exactly twice, select the digit whose *first* occurrence (smallest index) is earliest in the list. This is the "target digit".
4. If a target digit is found with indices idx1 and idx2 (idx1 < idx2), create a copy of the input list.
5. In the copied list, change the value of all elements at indices strictly between idx1 and idx2 (i.e., from index idx1 + 1 up to, but not including, index idx2) to the value of the target digit.
6. Return the modified list.
7. If no non-zero digit appears exactly twice, return the original input list unchanged.
"""

def find_indices_and_first_occurrence(data_list):
    """
    Finds all indices for each non-zero number and tracks the first index seen.

    Args:
        data_list: The input list of integers.

    Returns:
        A tuple containing:
        - dict: A dictionary mapping each non-zero digit to a list of its indices.
        - dict: A dictionary mapping each non-zero digit to its first encountered index.
    """
    indices_map = collections.defaultdict(list)
    first_occurrence = {}
    for index, value in enumerate(data_list):
        if value != 0:
            indices_map[value].append(index)
            if value not in first_occurrence:
                first_occurrence[value] = index
    return indices_map, first_occurrence

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A new list representing the transformed output, or the original list if no transformation applies.
    """

    # Analyze the input to find indices and first occurrences of non-zero digits
    indices_map, first_occurrence = find_indices_and_first_occurrence(input_list)

    # Initialize variables to find the target digit (the one appearing twice with the earliest first occurrence)
    target_digit = None
    min_first_index = float('inf')
    target_indices = None

    # Iterate through the digits found to identify potential targets
    for digit, indices in indices_map.items():
        # Check if the digit occurs exactly twice
        if len(indices) == 2:
            # Get the first index of this digit
            current_first_index = first_occurrence[digit]
            # If this digit's first occurrence is earlier than the current best, update the target
            if current_first_index < min_first_index:
                min_first_index = current_first_index
                target_digit = digit
                target_indices = indices

    # If no target digit was found (no digit appeared exactly twice)
    if target_digit is None:
        # Return the original list unchanged
        return list(input_list) # Return a copy to be safe, matching pattern of returning new list on change
    else:
        # A target digit was found, perform the fill operation
        # Create a copy of the input list to modify
        output_list = list(input_list)
        idx1, idx2 = target_indices[0], target_indices[1]

        # Fill the gap between the two indices (exclusive) with the target digit
        # Range starts from the element *after* the first occurrence (idx1 + 1)
        # and goes up to (but does not include) the second occurrence (idx2).
        for i in range(idx1 + 1, idx2):
            output_list[i] = target_digit

        # Return the modified list
        return output_list
```
```python
import collections
from typing import List, Dict, Tuple, Optional

"""
Transforms an input list of integers based on the following rule:
1. Identify all unique non-zero digits and the indices where they appear.
2. Check if any non-zero digit appears exactly twice in the list.
3. If one or more digits appear exactly twice, select the digit whose *first* occurrence (smallest index) is earliest in the list. This is the "target digit".
4. If a target digit is found with indices idx1 and idx2 (idx1 < idx2), create a copy of the input list.
5. In the copied list, change the value of all elements at indices strictly between idx1 and idx2 (i.e., from index idx1 + 1 up to, but not including, index idx2) to the value of the target digit.
6. Return the modified list.
7. If no non-zero digit appears exactly twice, return the original input list unchanged (as a new list copy).
"""

def _find_non_zero_digit_indices(data_list: List[int]) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    """
    Finds all indices for each non-zero number and tracks the first index seen.

    Args:
        data_list: The input list of integers.

    Returns:
        A tuple containing:
        - dict: A dictionary mapping each non-zero digit to a list of its indices.
        - dict: A dictionary mapping each non-zero digit to its first encountered index.
    """
    # Use defaultdict to easily append indices for each digit
    indices_map = collections.defaultdict(list)
    # Keep track of the first time we see a digit
    first_occurrence = {}
    for index, value in enumerate(data_list):
        if value != 0:
            indices_map[value].append(index)
            # Record the first occurrence index if not already seen
            if value not in first_occurrence:
                first_occurrence[value] = index
    return indices_map, first_occurrence

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A new list representing the transformed output, or a copy of the original list if no transformation applies.
    """

    # Step 1 & 2 (partially): Find indices and first occurrences of non-zero digits
    indices_map, first_occurrence = _find_non_zero_digit_indices(input_list)

    # Step 3 & 5a: Identify potential target digits (those appearing exactly twice)
    # and select the one with the earliest first occurrence.
    target_digit: Optional[int] = None
    min_first_index = float('inf')
    target_indices: Optional[List[int]] = None

    # Iterate through the non-zero digits found
    for digit, indices in indices_map.items():
        # Check if the digit occurs exactly twice
        if len(indices) == 2:
            # Get the first occurrence index for this digit
            current_first_index = first_occurrence[digit]
            # If this digit's first occurrence is earlier than the current best,
            # update the target digit and its details.
            if current_first_index < min_first_index:
                min_first_index = current_first_index
                target_digit = digit
                target_indices = indices # Store the two indices [idx1, idx2]

    # Step 4 & 7: If no target digit was found, return a copy of the original list.
    if target_digit is None or target_indices is None:
        return list(input_list) # Return a copy

    # Step 5b-e: A target digit was found, perform the fill operation.
    # Create a copy of the input list to modify.
    output_list = list(input_list)
    # Retrieve the start and end indices for the fill.
    idx1, idx2 = target_indices[0], target_indices[1] # Indices are already sorted as they were found sequentially

    # Fill the gap between the two indices (exclusive) with the target digit.
    # The range starts from the element *after* the first occurrence (idx1 + 1)
    # and goes up to (but does not include) the second occurrence (idx2).
    for i in range(idx1 + 1, idx2):
        # Only modify if the element is currently 0 (implied by examples, though could fill any)
        # The examples only show 0s being filled, so let's stick to that for now.
        # Revisit if examples show non-zeros being overwritten.
        # On second thought, the prompt says "fill the gap", which implies replacing whatever is there.
        # Let's assume replacement.
        output_list[i] = target_digit

    # Step 6: Return the modified list.
    return output_list
```
