
## train_1

**input:**
```
0 0 0 2 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 0 0 0
```


## train_2

**input:**
```
0 0 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 6 0 0
```


## train_3

**input:**
```
5 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 5 0
```


## train_5

**input:**
```
0 0 9 9 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 9 9 0 0 0
```


## train_6

**input:**
```
0 0 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 4 4 4 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 1 0
```

*   **Perception of Elements:**
    *   The input and output are sequences (lists or arrays) of 12 integers.
    *   The sequences primarily contain the integer 0.
    *   Each input sequence contains a single contiguous block of identical non-zero integers.
    *   The transformation involves moving this non-zero block within the sequence.

*   **YAML Fact Document:**
    
```yaml
    task_elements:
      - name: sequence
        type: list_of_integers
        properties:
          - length: 12
          - contains_zeros: true
          - contains_non_zero_block: true
      - name: zero
        type: integer
        value: 0
        role: background_element
      - name: non_zero_block
        type: list_of_integers
        properties:
          - contiguity: true
          - uniformity: all elements are identical and non-zero
          - variable_length: true
          - variable_value: true (e.g., 2, 6, 5, 9, 4, 1)
          - variable_position: true
    actions:
      - name: identify_block
        input: sequence
        output: non_zero_block_details (value, start_index, end_index)
      - name: shift_block
        input: non_zero_block_details
        parameter: shift_amount (integer)
        output: new_start_index, new_end_index
      - name: construct_output
        input: original_sequence_length, non_zero_block_details, new_start_index, new_end_index
        output: output_sequence
    relationships:
      - type: positional_shift
        element_1: non_zero_block (in input)
        element_2: non_zero_block (in output)
        detail: The start index of the block in the output is exactly 4 greater than the start index of the block in the input.
      - type: replacement
        location: original position of non_zero_block
        new_value: zero
    constants:
      - name: sequence_length
        value: 12
      - name: shift_distance
        value: 4
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of identical non-zero integers within the 12-element input sequence. Note its starting index, ending index, and the value of the integers in the block.
    2.  Create a new output sequence of 12 zeros.
    3.  Calculate the new starting index for the block by adding 4 to the original starting index found in step 1.
    4.  Calculate the new ending index for the block by adding 4 to the original ending index found in step 1.
    5.  Place the identified non-zero block (using the value from step 1) into the output sequence starting at the new starting index and ending at the new ending index calculated in steps 3 and 4.
    6.  Return the modified output sequence.
```python
import math
import collections

"""
Identifies a contiguous block of identical non-zero integers in a 12-element list.
Shifts this block exactly 4 positions to the right.
The original position of the block is replaced with zeros.
The output is a new 12-element list reflecting this shift.
"""

def find_block(input_list):
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        input_list: A list of integers.

    Returns:
        A tuple (value, start_index, end_index) representing the block's
        value, starting index (inclusive), and ending index (exclusive).
        Returns (None, -1, -1) if no such block is found.
    """
    start_index = -1
    end_index = -1
    value = None
    n = len(input_list)

    for i in range(n):
        # If we find a non-zero element and haven't started a block yet
        if input_list[i] != 0 and start_index == -1:
            start_index = i
            value = input_list[i]
        # If we have started a block and find a zero or a different non-zero number
        elif start_index != -1 and (input_list[i] == 0 or input_list[i] != value):
            end_index = i
            break # Block ended

    # If a block was started but didn't end before the list finished
    if start_index != -1 and end_index == -1:
        end_index = n

    return value, start_index, end_index

def transform(input_list):
    """
    Transforms the input list by shifting the non-zero block 4 positions right.

    Args:
        input_list: A list of 12 integers containing one non-zero block.

    Returns:
        A new list of 12 integers with the block shifted.
    """
    # Define constants based on observed pattern
    sequence_length = 12
    shift_distance = 4

    # Initialize the output list with zeros
    output_list = [0] * sequence_length

    # 1. Identify the contiguous block of identical non-zero integers
    block_value, start_index, end_index = find_block(input_list)

    # Check if a valid block was found
    if block_value is None or start_index == -1:
        # Should not happen based on problem description, but good practice
        return output_list # Return the list of zeros

    # 2. Calculate the new position for the block
    new_start_index = start_index + shift_distance
    new_end_index = end_index + shift_distance

    # 3. Place the block into the output list at the new position
    # Ensure the new indices are within the bounds of the list
    # (Assumed valid based on examples, but checking prevents errors)
    actual_start = max(0, new_start_index)
    actual_end = min(sequence_length, new_end_index)

    for i in range(actual_start, actual_end):
         # Calculate the corresponding index within the original block length
         # This isn't strictly needed here since we know the value,
         # but useful if block contents varied within the block.
         # original_block_index = i - new_start_index
         # output_list[i] = input_list[start_index + original_block_index]
         # Simpler: just use the constant block value
         output_list[i] = block_value


    # 4. Return the modified output sequence
    return output_list

```
