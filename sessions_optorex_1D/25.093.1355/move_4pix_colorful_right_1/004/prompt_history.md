
## train_1

**input:**
```
0 0 0 0 4 6 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 6 7 0
```


## train_2

**input:**
```
4 5 6 4 5 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 5 6 4 5 0 0 0
```


## train_3

**input:**
```
0 0 0 4 7 1 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 7 1 7 0
```


## train_4

**input:**
```
1 3 3 2 8 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 3 3 2 8 8 0 0
```


## train_5

**input:**
```
0 2 2 5 4 4 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 2 5 4 4 5 0
```


## train_6

**input:**
```
0 0 0 2 9 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 9 8 0 0
```


## train_7

**input:**
```
0 3 2 7 8 7 7 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 2 7 8 7 7 4
```

Okay, let's analyze the task based on the provided examples.

**Perception of Task Elements:**

*   **Input/Output Format:** Both input and output are lists (or sequences) of integers. All examples show lists of length 12.
*   **Core Transformation:** The primary operation seems to be a spatial shift or relocation of a specific segment of the input list.
*   **Identifying the Segment:** The segment being moved consists of the non-zero numbers and any zeros located between the first and last non-zero number.
*   **Shift Characteristics:** The identified segment is moved to the right. The relative order of the numbers within the segment remains unchanged. The magnitude of the shift appears constant across all examples.
*   **Padding:** The positions in the output list not occupied by the shifted segment are filled with zeros.

**Analysis of the Shift:**

Let's determine the exact shift amount.
*   In `train_1`, the segment `[4, 6, 7]` starts at index 4 in the input and index 8 in the output. Shift = 8 - 4 = +4.
*   In `train_2`, the segment `[4, 5, 6, 4, 5]` starts at index 0 in the input and index 4 in the output. Shift = 4 - 0 = +4.
*   In `train_3`, the segment `[4, 7, 1, 7]` starts at index 3 in the input and index 7 in the output. Shift = 7 - 3 = +4.
*   In `train_4`, the segment `[1, 3, 3, 2, 8, 8]` starts at index 0 in the input and index 4 in the output. Shift = 4 - 0 = +4.

The pattern holds: the segment containing all non-zero numbers (from the first non-zero to the last non-zero) is shifted exactly 4 positions to the right.

**YAML Facts:**


```yaml
task_description: "Shift a contiguous block of numbers within a fixed-length list."
elements:
  - object: list
    type: integer_sequence
    properties:
      length: 12
      role: input/output
  - object: segment
    type: sublist
    definition: "The contiguous part of the input list starting from the first non-zero element and ending at the last non-zero element."
    properties:
      content: integers (non-zero and potentially intervening zeros)
      relative_order: preserved
relationships:
  - type: derivation
    from: input_list
    to: output_list
  - type: transformation
    action: identify_segment
    input: input_list
    output: segment, start_index
  - type: transformation
    action: calculate_new_position
    input: start_index
    parameter: shift_amount (constant +4)
    output: new_start_index
  - type: transformation
    action: construct_output
    inputs: list_length, segment, new_start_index
    process: "Create a list of zeros of the specified length, then place the segment at the new_start_index."
constants:
  list_length: 12
  shift_amount: 4
```


**Natural Language Program:**

1.  Identify the input list of 12 integers.
2.  Locate the index of the first non-zero integer (`first_nz_idx`) and the index of the last non-zero integer (`last_nz_idx`).
3.  If no non-zero integers are found (the list is all zeros), the output is identical to the input.
4.  Otherwise, extract the contiguous sublist (the "segment") from the input list, starting at `first_nz_idx` and ending at `last_nz_idx` (inclusive).
5.  Determine the target starting index for this segment in the output list by adding 4 to the `first_nz_idx`.
6.  Create a new output list of 12 zeros.
7.  Place the extracted segment into the output list, starting at the calculated target starting index.
8.  Return the resulting output list.
```python
import math
import collections

"""
Identify the contiguous segment of the input list starting from the first non-zero 
integer and ending at the last non-zero integer. Shift this entire segment exactly 
4 positions to the right within a list of the same total length (12), filling 
the remaining positions with zeros. If the input list contains only zeros, the 
output is identical to the input.
"""

def find_first_last_non_zero_indices(data_list):
  """
  Finds the indices of the first and last non-zero elements in a list.

  Args:
    data_list: The list of numbers to search.

  Returns:
    A tuple (first_idx, last_idx). Returns (None, None) if no non-zero 
    elements are found.
  """
  first_idx = None
  last_idx = None
  for i, val in enumerate(data_list):
    if val != 0:
      if first_idx is None:
        first_idx = i
      last_idx = i
  return first_idx, last_idx

def transform(input_list):
  """
  Transforms the input list by shifting the core non-zero segment 
  4 positions to the right.

  Args:
    input_list: A list of 12 integers.

  Returns:
    A new list of 12 integers with the segment shifted.
  """
  # Define constants based on observed patterns
  list_length = 12
  shift_amount = 4

  # Find the boundaries of the non-zero segment
  first_nz_idx, last_nz_idx = find_first_last_non_zero_indices(input_list)

  # Handle the case where the list is all zeros
  if first_nz_idx is None:
    return list(input_list) # Return a copy if no non-zeros found

  # Extract the segment
  # The segment includes all elements from the first non-zero to the last non-zero
  segment = input_list[first_nz_idx : last_nz_idx + 1]

  # Calculate the new starting position for the segment
  new_start_idx = first_nz_idx + shift_amount

  # Initialize the output list with zeros
  output_list = [0] * list_length

  # Place the segment into the output list at the new position
  # Ensure the segment fits within the bounds (though examples suggest it always does)
  segment_len = len(segment)
  if new_start_idx + segment_len <= list_length:
      output_list[new_start_idx : new_start_idx + segment_len] = segment
  else:
      # This case shouldn't happen based on examples, but include basic handling
      # Place as much of the segment as fits starting from new_start_idx
      fit_len = list_length - new_start_idx
      output_list[new_start_idx : list_length] = segment[:fit_len]


  return output_list
```
```python
import numpy as np
import math
import collections # Not strictly needed now but good practice

"""
Identify the contiguous segment of the input NumPy array (length 12) starting from 
the index of the first non-zero integer and ending at the index of the last 
non-zero integer. Shift this entire segment exactly 4 positions to the right 
within a new NumPy array of the same shape and dtype, filling the remaining 
positions with zeros. If the input array contains only zeros, the output is 
identical to the input.
"""

def find_non_zero_bounds(data_array):
  """
  Finds the indices of the first and last non-zero elements in a NumPy array.

  Args:
    data_array: The 1D NumPy array to search.

  Returns:
    A tuple (first_idx, last_idx). Returns (None, None) if no non-zero 
    elements are found.
  """
  non_zero_indices = np.nonzero(data_array)[0] # Get indices for the first (only) dimension
  if non_zero_indices.size == 0:
    return None, None
  first_idx = non_zero_indices[0]
  last_idx = non_zero_indices[-1]
  return first_idx, last_idx

def transform(input_array):
  """
  Transforms the input array by shifting the core non-zero segment 
  4 positions to the right.

  Args:
    input_array: A 1D NumPy array of 12 integers.

  Returns:
    A new 1D NumPy array of 12 integers with the segment shifted.
  """
  # Define constants based on observed patterns
  array_length = 12 # Expected length from examples
  shift_amount = 4

  # Ensure input is a numpy array (useful if the framework doesn't guarantee it)
  # input_array = np.array(input_array) 

  # Find the boundaries of the non-zero segment
  first_nz_idx, last_nz_idx = find_non_zero_bounds(input_array)

  # Handle the case where the array is all zeros
  if first_nz_idx is None:
    # If no non-zeros, return a copy of the input array
    return np.copy(input_array) 

  # Extract the segment
  # The segment includes all elements from the first non-zero to the last non-zero
  segment = input_array[first_nz_idx : last_nz_idx + 1]

  # Calculate the new starting position for the segment
  new_start_idx = first_nz_idx + shift_amount

  # Initialize the output array with zeros, preserving the data type
  output_array = np.zeros(array_length, dtype=input_array.dtype)

  # Place the segment into the output array at the new position
  segment_len = segment.shape[0] # Length of the segment
  
  # Calculate the end index for slicing in the output array
  new_end_idx = new_start_idx + segment_len
  
  # Check bounds before placing (though examples suggest it always fits)
  if new_end_idx <= array_length:
      output_array[new_start_idx : new_end_idx] = segment
  else:
      # If the segment goes out of bounds, truncate it
      fit_len = array_length - new_start_idx
      output_array[new_start_idx : array_length] = segment[:fit_len] # Place the part that fits

  return output_array
```
