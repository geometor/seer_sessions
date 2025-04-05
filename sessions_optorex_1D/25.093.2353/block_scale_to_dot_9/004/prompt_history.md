
## train_1

**input:**
```
0 0 0 0 2 0 7 7 7 7 7 7
```


**output:**
```
0 0 0 0 2 7 7 7 7 7 7 7
```


## train_2

**input:**
```
0 0 0 2 0 0 0 0 3 3 3 3
```


**output:**
```
0 0 0 2 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 2 0 0 0 0 0 0 0 0 0 8
```


**output:**
```
0 2 8 8 8 8 8 8 8 8 8 8
```


## train_4

**input:**
```
0 6 6 6 6 6 6 6 6 2 0 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 2 0 0
```


## train_5

**input:**
```
0 9 9 9 0 0 0 0 0 0 2 0
```


**output:**
```
0 9 9 9 9 9 9 9 9 9 2 0
```


## train_6

**input:**
```
7 7 7 7 7 7 7 2 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 2 0 0 0 0
```


## train_7

**input:**
```
0 0 5 5 5 5 5 0 0 2 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 2 0 0
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are sequences (lists or arrays) of 12 single-digit integers.
2.  **Key Digits:** The digits `0` and `2` appear to play special roles. Other non-zero digits (like `3`, `5`, `6`, `7`, `8`, `9` in the examples) act as "fill" values.
3.  **The Role of '2':** The digit `2` seems to function as a fixed boundary or marker within the sequence. Its position does not change.
4.  **The Role of '0':** The digit `0` represents an empty or fillable space. These are the only digits that get replaced.
5.  **The Role of Other Non-Zero Digits (N):** These digits seem to expand or "fill" adjacent `0`s under certain conditions. The expansion originates from an existing block or instance of the digit `N`.
6.  **Transformation Mechanism:** The transformation involves identifying sequences of `0`s that lie *between* the digit `2` and the nearest non-zero digit (`N`) on either side (left or right). These intervening `0`s are then replaced by the digit `N`. If `2` is already adjacent to a non-zero digit, or if there are no non-zero digits on one side, no filling occurs on that side.

**YAML Fact Document:**


```yaml
elements:
  - type: sequence
    properties:
      - length: 12
      - item_type: integer
      - item_range: 0-9
objects:
  - id: marker
    value: 2
    description: A fixed position digit that acts as a boundary. Its own value and position never change.
  - id: fillable_space
    value: 0
    description: Represents positions that can be potentially overwritten.
  - id: fill_value
    value: N (any digit from 1, 3, 4, 5, 6, 7, 8, 9)
    description: A non-zero, non-marker digit that can expand to replace adjacent 'fillable_space' digits.
relationships:
  - type: adjacency
    description: The relative positions of 'marker', 'fillable_space', and 'fill_value' determine the transformation.
  - type: spatial_gap
    description: A sequence of one or more 'fillable_space' digits located between a 'marker' and the nearest 'fill_value' on either side.
actions:
  - name: locate_marker
    actor: system
    target: input_sequence
    description: Find the index of the 'marker' (digit 2).
  - name: locate_nearest_fill_value
    actor: system
    target: input_sequence
    parameters:
      - direction: left_of_marker
      - direction: right_of_marker
    description: Find the index of the nearest non-zero, non-marker digit ('fill_value') to the left and right of the 'marker'.
  - name: fill_gap
    actor: system
    target: sequence (initially a copy of input)
    condition: A 'spatial_gap' exists between the 'marker' and a 'fill_value'.
    effect: Replace all 'fillable_space' (0) digits within the 'spatial_gap' with the corresponding 'fill_value'. This happens independently for the left and right sides of the 'marker'.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Create a mutable copy of the input sequence to serve as the potential output.
3.  Find the index (position) of the digit `2` in the sequence. Let this be `marker_index`.
4.  **Left-side Fill:**
    a.  Search the sequence from `marker_index - 1` down to index 0.
    b.  Find the index of the first non-zero digit encountered. Let this be `left_fill_index` and its value be `left_fill_value`.
    c.  If such a digit is found (i.e., `left_fill_index` exists):
        i.  Iterate through the indices from `left_fill_index + 1` up to `marker_index - 1`.
        ii. For each index in this range, if the digit in the sequence copy at that index is `0`, replace it with `left_fill_value`.
5.  **Right-side Fill:**
    a.  Search the sequence from `marker_index + 1` up to the end of the sequence (index 11).
    b.  Find the index of the first non-zero digit encountered. Let this be `right_fill_index` and its value be `right_fill_value`.
    c.  If such a digit is found (i.e., `right_fill_index` exists):
        i.  Iterate through the indices from `marker_index + 1` up to `right_fill_index - 1`.
        ii. For each index in this range, if the digit in the sequence copy at that index is `0`, replace it with `right_fill_value`.
6.  Return the modified sequence copy as the output.
```python
import copy

"""
Transforms a sequence of 12 digits based on the following rules:
1. Locate the digit '2', which acts as a fixed marker.
2. Find the nearest non-zero digit to the left of the marker ('left_fill_value').
3. Replace all zeros between the 'left_fill_value' and the marker with 'left_fill_value'.
4. Find the nearest non-zero digit to the right of the marker ('right_fill_value').
5. Replace all zeros between the marker and the 'right_fill_value' with 'right_fill_value'.
6. If no non-zero digit exists on a side, no filling occurs on that side.
7. The marker '2' and existing non-zero digits remain unchanged.
"""

def transform(input_sequence_str):
    """
    Applies the described transformation to an input sequence string.

    Args:
        input_sequence_str: A string of space-separated single digits (e.g., "0 0 0 0 2 0 7 7 7 7 7 7").

    Returns:
        A string of space-separated single digits representing the transformed sequence.
        Returns the original string if the marker '2' is not found.
    """
    # Convert string input to list of integers
    try:
        input_list = [int(d) for d in input_sequence_str.split()]
    except ValueError:
        # Handle cases where input might not be valid integers
        print(f"Error: Input string '{input_sequence_str}' contains non-integer values.")
        return input_sequence_str # Or raise an error

    if len(input_list) != 12:
         print(f"Warning: Input sequence length is not 12 ({len(input_list)}).")
         # Decide how to handle this - process anyway or return error? Processing for now.


    # Initialize output_grid as a copy of the input list
    output_list = copy.deepcopy(input_list)
    n = len(output_list)

    # Find the index of the marker '2'
    marker_index = -1
    try:
        marker_index = input_list.index(2)
    except ValueError:
        # Marker '2' not found, return the original list as a string
        print("Marker '2' not found in the input.")
        return input_sequence_str

    # --- Left-side Fill ---
    left_fill_value = None
    left_fill_index = -1
    # Search backwards from marker_index - 1
    for i in range(marker_index - 1, -1, -1):
        if input_list[i] != 0:
            left_fill_value = input_list[i]
            left_fill_index = i
            break # Found the nearest non-zero

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_value is not None:
        for i in range(left_fill_index + 1, marker_index):
            if output_list[i] == 0:
                output_list[i] = left_fill_value

    # --- Right-side Fill ---
    right_fill_value = None
    right_fill_index = -1
    # Search forwards from marker_index + 1
    for i in range(marker_index + 1, n):
        if input_list[i] != 0:
            right_fill_value = input_list[i]
            right_fill_index = i
            break # Found the nearest non-zero

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_value is not None:
        for i in range(marker_index + 1, right_fill_index):
             if output_list[i] == 0:
                output_list[i] = right_fill_value

    # Convert the result list back to a space-separated string
    output_sequence_str = " ".join(map(str, output_list))
    return output_sequence_str

```
```python
import copy
# numpy is implicitly available but not explicitly needed for this logic if input is list-like
# import numpy as np 

"""
Transforms a sequence of digits based on the following rules:
1. Locate the digit '2', which acts as a fixed marker.
2. Find the nearest non-zero digit to the left of the marker ('left_fill_value').
3. Replace all zeros strictly between the 'left_fill_value' and the marker with 'left_fill_value'.
4. Find the nearest non-zero digit to the right of the marker ('right_fill_value').
5. Replace all zeros strictly between the marker and the 'right_fill_value' with 'right_fill_value'.
6. If no non-zero digit exists on a side (left or right), no filling occurs on that side.
7. The marker '2' and existing non-zero digits in the input sequence remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list-like sequence (e.g., list, numpy array) of integers.

    Returns:
        A new list or array representing the transformed sequence. Returns a copy
        of the original if the marker '2' is not found.
    """
    
    # Initialize output_grid as a deep copy to avoid modifying the input object
    # This works for both lists and numpy arrays
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid) # Get the length of the sequence

    # Find the index of the marker '2'
    marker_index = -1
    try:
        # Convert to list temporarily to use the .index() method reliably
        # This handles cases where input_grid might be a numpy array
        input_list_for_index = list(input_grid) 
        marker_index = input_list_for_index.index(2)
    except ValueError:
        # Marker '2' not found, return the original grid copy unchanged
        return output_grid # No transformation needed if no marker

    # --- Left-side processing: Find nearest non-zero and fill ---
    left_fill_value = None
    left_fill_index = -1
    # Search backwards from the position immediately left of the marker
    for i in range(marker_index - 1, -1, -1):
        if input_grid[i] != 0:  # Found the nearest non-zero digit
            left_fill_value = input_grid[i]
            left_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the left, fill the zeros in between
    if left_fill_value is not None:
        # Iterate from the position right after the left fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            # Check if the position in the original grid was a zero before filling
            if input_grid[i] == 0: 
                 output_grid[i] = left_fill_value # Update the output grid

    # --- Right-side processing: Find nearest non-zero and fill ---
    right_fill_value = None
    right_fill_index = -1
    # Search forwards from the position immediately right of the marker
    for i in range(marker_index + 1, n):
        if input_grid[i] != 0: # Found the nearest non-zero digit
            right_fill_value = input_grid[i]
            right_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the right, fill the zeros in between
    if right_fill_value is not None:
        # Iterate from the position right after the marker up to (not including) the right fill value
        for i in range(marker_index + 1, right_fill_index):
            # Check if the position in the original grid was a zero before filling
             if input_grid[i] == 0: 
                 output_grid[i] = right_fill_value # Update the output grid

    # Return the modified grid
    return output_grid
```
