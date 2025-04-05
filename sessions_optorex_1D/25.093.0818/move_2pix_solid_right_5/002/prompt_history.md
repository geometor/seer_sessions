
## train_1

**input:**
```
0 0 0 0 0 0 0 6 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 6 6 0
```


## train_2

**input:**
```
0 0 0 0 0 0 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 0 0
```


## train_3

**input:**
```
9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 8 8 8 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 0 0 0 0 0
```


## train_5

**input:**
```
6 6 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 6 6 0 0 0 0
```


## train_6

**input:**
```
1 1 1 1 1 1 0 0 0 0 0 0
```


**output:**
```
0 0 1 1 1 1 1 1 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 6 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 6 6
```

*   **Perception:** The task involves manipulating a sequence of twelve integers. Each input sequence contains a single contiguous block of identical non-zero integers, padded with zeros on either side. The transformation consists of shifting this entire non-zero block exactly two positions to the right within the sequence. The positions originally occupied by the block, and any positions to its left that are not taken up by the shifted block, become zeros. The length of the sequence remains constant at twelve.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input_format: string of space-separated integers
    output_format: string of space-separated integers
    sequence_length: 12 (constant in examples)
    elements:
      - type: integer
        value: 0 (acts as background/padding)
      - type: integer
        value: non-zero (forms a contiguous block)
    objects:
      - name: input_sequence
        type: list_of_integers
        properties:
          - contains_single_contiguous_non_zero_block
      - name: non_zero_block
        type: sublist_of_integers
        properties:
          - all_elements_are_identical_non_zero
          - contiguous_within_input_sequence
          - has_start_index
          - has_end_index
      - name: output_sequence
        type: list_of_integers
        properties:
          - same_length_as_input_sequence
    actions:
      - name: identify_block
        description: Find the start and end indices of the non_zero_block in the input_sequence.
      - name: shift_block
        description: Move the identified non_zero_block two positions to the right.
      - name: construct_output
        description: Create the output_sequence by placing the shifted block at its new position and filling remaining positions with zeros.
    relationships:
      - The output_sequence is derived from the input_sequence by applying the shift_block action to the non_zero_block.
      - The new start index of the block in the output is the original start index + 2.
      - The new end index of the block in the output is the original end index + 2.
    constraints:
      - Input sequence always contains exactly one contiguous block of non-zero numbers.
      - The non-zero numbers within the block are identical in the provided examples.
      - The shift amount is always +2 positions to the right.
      - The sequence length is fixed.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of integers (the `input_sequence`).
    2.  Determine the length of the `input_sequence`.
    3.  Initialize an `output_sequence` as a list of zeros with the same length.
    4.  Find the starting index (`start_index`) of the first non-zero element in the `input_sequence`. If no non-zero element exists, the `output_sequence` remains all zeros.
    5.  Find the ending index (`end_index`) of the last non-zero element in the `input_sequence`.
    6.  Extract the sublist containing the non-zero block from the `input_sequence`, ranging from `start_index` to `end_index` (inclusive).
    7.  Calculate the new starting index for the block in the `output_sequence` as `new_start_index = start_index + 2`.
    8.  Iterate through the extracted non-zero block elements. For each element at index `i` within the block (where `i` ranges from 0 to `end_index - start_index`), place it into the `output_sequence` at index `new_start_index + i`. Ensure indices remain within the bounds of the `output_sequence`.
    9.  Convert the `output_sequence` (list of integers) back into a space-separated string for the final output.
```python
"""
Transforms an input sequence of 12 integers by identifying a single contiguous block of identical non-zero integers and shifting this block exactly two positions to the right. The remaining positions are filled with zeros.
"""

import re # Using re for potentially finding the block, although simpler list operations might suffice

def _find_non_zero_block_indices(sequence):
    """
    Finds the start and end indices of the first contiguous non-zero block.
    Returns (start_index, end_index) or (None, None) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    for i, val in enumerate(sequence):
        if val != 0:
            if start_index == -1:
                start_index = i
            end_index = i
        elif start_index != -1:
            # Found a zero after the block started, so the block ended at the previous index
            break
    if start_index == -1:
        return None, None # No non-zero elements found
    return start_index, end_index

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of space-separated integers.

    Returns:
        A string of space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers
    input_sequence = [int(x) for x in input_str.split()]
    sequence_length = len(input_sequence)

    # 2. Initialize an output_sequence as a list of zeros with the same length
    output_sequence = [0] * sequence_length

    # 3. Find the starting and ending indices of the non-zero block
    start_index, end_index = _find_non_zero_block_indices(input_sequence)

    # 4. If a non-zero block exists, proceed with the shift
    if start_index is not None and end_index is not None:
        # 5. Extract the non-zero block
        non_zero_block = input_sequence[start_index : end_index + 1]

        # 6. Calculate the new starting index for the block
        new_start_index = start_index + 2

        # 7. Place the extracted non-zero block into the output_sequence at the new position
        # Iterate through the block and place elements, ensuring we don't go out of bounds
        for i, value in enumerate(non_zero_block):
            target_index = new_start_index + i
            if target_index < sequence_length: # Check boundary condition
                output_sequence[target_index] = value
            # If target_index >= sequence_length, the block element shifts off the end

    # 8. Convert the output_sequence back into a space-separated string
    output_str = " ".join(map(str, output_sequence))

    return output_str

```
