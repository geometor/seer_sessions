
## train_1

**input:**
```
3 3 3 3 0 0 0 0 0 0 2 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 2 0
```


## train_2

**input:**
```
6 6 6 6 6 6 2 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 7 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 2 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 9 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 2 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 8 8 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 2
```


## train_6

**input:**
```
0 2 0 0 8 8 8 8 0 0 0 0
```


**output:**
```
0 2 8 8 8 8 8 8 0 0 0 0
```


## train_7

**input:**
```
0 0 2 0 0 0 1 1 1 1 1 1
```


**output:**
```
0 0 2 1 1 1 1 1 1 1 1 1
```

**Perception of Task Elements:**

The task operates on sequences of 12 integers. The core elements appear to be:
1.  **The Number 2:** This number acts as a central pivot or boundary marker within the sequence.
2.  **Other Non-Zero Numbers:** These numbers (e.g., 1, 3, 6, 7, 8, 9) serve as "fill" values.
3.  **Zeros (0):** These are the elements subject to modification (filling).
4.  **Position/Sequence:** The relative positions of the numbers, specifically their proximity to the number 2, are crucial.

The transformation involves propagating a non-zero "fill" value into adjacent zeros, bounded by the position of the number 2.

**Facts:**


```yaml
objects:
  - sequence: a list of 12 integers.
  - marker: the integer value 2.
  - fill_value: any non-zero integer in the sequence other than 2.
  - target_element: the integer value 0.
properties:
  - sequence_length: 12
  - marker_presence: the number 2 is always present exactly once.
  - fill_value_location: relative position to the marker (left or right).
  - target_element_location: relative position to the marker and the fill_value.
actions:
  - locate: find the index of the marker (2).
  - search_left: find the nearest non-zero fill_value to the left of the marker.
  - search_right: find the nearest non-zero fill_value to the right of the marker.
  - fill: replace target_elements (0) between a fill_value and the marker with that fill_value.
relationships:
  - adjacency: zeros located between a fill_value and the marker.
  - boundary: the marker (2) limits the fill operation.
```


**Natural Language Program:**

1.  Identify the index of the number `2` in the input sequence.
2.  Find the index of the rightmost non-zero number located *before* the index of `2`. Let this number be `left_fill_value`. If such a number exists, replace all zeros between its index and the index of `2` with `left_fill_value`.
3.  Find the index of the leftmost non-zero number located *after* the index of `2`. Let this number be `right_fill_value`. If such a number exists, replace all zeros between the index of `2` and its index with `right_fill_value`.
4.  Return the modified sequence.
```python
import math
import numpy as np # Although not strictly needed for this logic, it's often available

"""
1. Identify the index of the number `2` in the input sequence.
2. Find the index of the rightmost non-zero number located *before* the index of `2`. Let this number be `left_fill_value`. If such a number exists, replace all zeros between its index (exclusive) and the index of `2` (exclusive) with `left_fill_value`.
3. Find the index of the leftmost non-zero number located *after* the index of `2`. Let this number be `right_fill_value`. If such a number exists, replace all zeros between the index of `2` (exclusive) and its index (exclusive) with `right_fill_value`.
4. Return the modified sequence.
"""

def find_index(sequence, value):
    """Helper function to find the first index of a value in a sequence."""
    try:
        return sequence.index(value)
    except ValueError:
        return -1 # Indicate not found

def transform(input_str):
    """
    Applies a fill operation on a sequence of integers based on the position of the number 2.
    Zeros between the number 2 and the nearest non-zero numbers on either side are filled
    with those respective non-zero numbers.
    """
    # Convert input string to a list of integers
    input_list = [int(x) for x in input_str.split()]
    
    # Initialize output_list as a copy of the input to modify it
    output_list = list(input_list)
    n = len(output_list)

    # 1. Identify the index of the number 2
    marker_index = find_index(output_list, 2)

    # If 2 is not found (shouldn't happen based on examples, but good practice)
    if marker_index == -1:
        return " ".join(map(str, output_list)) # Return original if 2 is missing

    # 2. Find the rightmost non-zero number *before* 2 and fill leftwards
    left_fill_value = 0
    left_fill_index = -1
    for i in range(marker_index - 1, -1, -1):
        if output_list[i] != 0:
            left_fill_value = output_list[i]
            left_fill_index = i
            break # Found the closest non-zero to the left

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_index != -1:
        for i in range(left_fill_index + 1, marker_index):
            if output_list[i] == 0:
                output_list[i] = left_fill_value

    # 3. Find the leftmost non-zero number *after* 2 and fill rightwards
    right_fill_value = 0
    right_fill_index = -1
    for i in range(marker_index + 1, n):
        if output_list[i] != 0:
            right_fill_value = output_list[i]
            right_fill_index = i
            break # Found the closest non-zero to the right

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_index != -1:
        for i in range(marker_index + 1, right_fill_index):
             if output_list[i] == 0:
                output_list[i] = right_fill_value

    # 4. Return the modified sequence as a space-separated string
    return " ".join(map(str, output_list))

```
```python
import numpy as np

"""
Accept the input, which is a sequence (list or array) of 12 integers.
Create a modifiable copy of the input sequence.
Locate the index of the number `2` (the marker) within the sequence.
Left Fill Process:
  Search backwards from the index immediately preceding the marker towards the beginning of the sequence.
  Identify the first non-zero number encountered (this is the `left_fill_value`) and record its index (`left_fill_index`).
  If a `left_fill_value` is found, iterate through the indices strictly between `left_fill_index` and the marker's index. Replace any element at these indices that is `0` with the `left_fill_value`.
Right Fill Process:
  Search forwards from the index immediately following the marker towards the end of the sequence.
  Identify the first non-zero number encountered (this is the `right_fill_value`) and record its index (`right_fill_index`).
  If a `right_fill_value` is found, iterate through the indices strictly between the marker's index and `right_fill_index`. Replace any element at these indices that is `0` with the `right_fill_value`.
Return the modified sequence.
"""

def find_first_occurrence(sequence, value):
    """Helper function to find the first index of a value in a sequence."""
    try:
        # np.where returns a tuple of arrays, one for each dimension.
        # For a 1D array, we take the first element of the tuple,
        # and then the first element of that array.
        indices = np.where(sequence == value)[0]
        if len(indices) > 0:
            return indices[0]
        else:
            return -1 # Indicate not found
    except Exception: # Catch potential errors if input isn't array-like or value not present
        return -1

def transform(input_sequence):
    """
    Applies a fill operation on a sequence of integers based on the position of the number 2.
    Zeros between the number 2 and the nearest non-zero numbers on either side are filled
    with those respective non-zero numbers.
    
    Args:
        input_sequence (numpy.ndarray): A 1D numpy array of 12 integers.

    Returns:
        numpy.ndarray: The modified numpy array.
    """
    # Ensure input is a numpy array and create a modifiable copy
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence)
    output_sequence = np.copy(input_sequence)
    n = len(output_sequence)

    # 1. Locate the index of the number 2 (the marker)
    marker_index = find_first_occurrence(output_sequence, 2)

    # If 2 is not found (shouldn't happen based on examples, but good practice)
    if marker_index == -1:
        return output_sequence # Return original if 2 is missing

    # 2. Left Fill Process
    left_fill_value = 0
    left_fill_index = -1
    # Search backwards from marker_index - 1 to index 0
    for i in range(marker_index - 1, -1, -1):
        if output_sequence[i] != 0:
            left_fill_value = output_sequence[i]
            left_fill_index = i
            break # Found the closest non-zero to the left

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_index != -1:
        # Iterate from the index *after* the fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            if output_sequence[i] == 0:
                output_sequence[i] = left_fill_value

    # 3. Right Fill Process
    right_fill_value = 0
    right_fill_index = -1
    # Search forwards from marker_index + 1 to the end of the sequence
    for i in range(marker_index + 1, n):
        if output_sequence[i] != 0:
            right_fill_value = output_sequence[i]
            right_fill_index = i
            break # Found the closest non-zero to the right

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_index != -1:
        # Iterate from the index *after* the marker up to (not including) the fill value
        for i in range(marker_index + 1, right_fill_index):
             if output_sequence[i] == 0:
                output_sequence[i] = right_fill_value

    # 4. Return the modified sequence
    return output_sequence
```
