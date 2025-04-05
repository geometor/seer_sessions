
## train_1

**input:**
```
0 0 0 0 0 1 9 5 9 6 3 8
```


**output:**
```
0 1 9 5 9 6 3 8 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 3 6 7 6 0 0 0 0
```


**output:**
```
3 6 7 6 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 3 3
```


**output:**
```
0 0 0 0 0 0 3 3 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 5 6 4 1 4 8 0 0
```


**output:**
```
5 6 4 1 4 8 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 4 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 3 4 9 9 2 6 5 0
```


**output:**
```
3 4 9 9 2 6 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 5 9 4 7 7 0 0
```


**output:**
```
0 5 9 4 7 7 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The inputs and outputs are sequences of single-digit integers, represented as space-separated strings.
    *   All sequences (input and output) have the same length (12 elements).
    *   The core content consists of a contiguous block of digits that starts with the first non-zero digit and ends with the last non-zero digit in the input sequence. This block may contain internal zeros.
    *   The remaining elements are zeros, appearing before (leading) and after (trailing) the core block.
    *   The transformation involves repositioning the core block within the sequence.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - item: sequence
        properties:
          - type: list of integers
          - length: 12
          - representation: space-separated string
      - item: core_block
        properties:
          - type: sub-sequence
          - definition: contiguous elements from the first non-zero digit to the last non-zero digit (inclusive)
          - contains: digits (can include internal zeros)
      - item: surrounding_zeros
        properties:
          - type: sequence elements
          - value: 0
          - position: before (leading) and after (trailing) the core_block
    transformation:
      action: shift_left
      target: core_block
      details:
        - identify the start index (first_nz) of the core_block in the input
        - calculate the new start index (new_start) for the core_block in the output: new_start = max(0, first_nz - 4)
        - place the core_block at the new_start index in an output sequence of the same length, initialized with zeros
        - the remaining positions in the output sequence are filled with zeros, effectively redistributing the original leading and trailing zeros.
    edge_case:
      - condition: input sequence contains only zeros
        output: return the input sequence unchanged
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of 12 digits.
    2.  Find the index of the first non-zero digit (`first_nz`).
    3.  If no non-zero digit is found (the sequence is all zeros), return the original sequence.
    4.  Find the index of the last non-zero digit (`last_nz`).
    5.  Extract the sub-sequence (the "core block") from `first_nz` to `last_nz` (inclusive).
    6.  Calculate the target starting index for the core block in the output sequence: `new_start = max(0, first_nz - 4)`.
    7.  Create a new sequence of 12 zeros.
    8.  Place the extracted core block into the new sequence, starting at the calculated `new_start` index.
    9.  Return the resulting sequence.
```python
import math

def find_first_nonzero_index(nums):
  """Finds the index of the first non-zero element."""
  for i, num in enumerate(nums):
    if num != 0:
      return i
  return -1 # Indicate not found

def find_last_nonzero_index(nums):
  """Finds the index of the last non-zero element."""
  last_nz = -1
  for i, num in enumerate(nums):
    if num != 0:
      last_nz = i
  return last_nz

def transform(input_str):
  """
  Transforms the input sequence by identifying the 'core block' (from the
  first non-zero digit to the last non-zero digit) and shifting it left
  by 4 positions, ensuring it doesn't go beyond the start of the sequence.
  The remaining positions are filled with zeros.
  """
  # 1. Read the input sequence of 12 digits.
  input_list = [int(x) for x in input_str.split()]
  n = len(input_list)

  # 2. Find the index of the first non-zero digit (`first_nz`).
  first_nz = find_first_nonzero_index(input_list)

  # 3. If no non-zero digit is found (the sequence is all zeros), return the original sequence.
  if first_nz == -1:
    return input_str

  # 4. Find the index of the last non-zero digit (`last_nz`).
  last_nz = find_last_nonzero_index(input_list)

  # 5. Extract the sub-sequence (the "core block") from `first_nz` to `last_nz` (inclusive).
  core_block = input_list[first_nz : last_nz + 1]
  core_len = len(core_block)

  # 6. Calculate the target starting index for the core block in the output sequence.
  new_start = max(0, first_nz - 4)

  # 7. Create a new sequence of 12 zeros.
  output_list = [0] * n

  # 8. Place the extracted core block into the new sequence, starting at the calculated `new_start` index.
  # Ensure the block doesn't exceed the bounds of the output list
  end_index = min(new_start + core_len, n)
  block_len_to_copy = end_index - new_start
  output_list[new_start : end_index] = core_block[:block_len_to_copy] # Slice core_block in case it's too long

  # 9. Return the resulting sequence as a space-separated string.
  return " ".join(map(str, output_list))

```
```python
import numpy as np # Use numpy for array handling as suggested by error messages

"""
Transforms an input sequence (list or array of 12 integers) by:
1. Identifying the 'core block' which starts at the first non-zero element 
   and ends at the last non-zero element (inclusive).
2. Calculating a new starting position for this block by shifting its original 
   start position left by 4 indices, but not going below index 0.
3. Creating a new sequence of 12 zeros.
4. Placing the extracted 'core block' into the new sequence at the calculated 
   starting position. Zeros fill the remaining positions.
5. If the input sequence contains only zeros, it is returned unchanged.
"""

def find_first_nonzero_index(sequence):
  """Finds the index of the first non-zero element in a sequence."""
  for i, element in enumerate(sequence):
    if element != 0:
      return i
  return -1 # Indicate not found

def find_last_nonzero_index(sequence):
  """Finds the index of the last non-zero element in a sequence."""
  last_nz = -1
  for i, element in enumerate(sequence):
    if element != 0:
      last_nz = i
  return last_nz

def transform(input_sequence):
    """
    Applies the described transformation rule to the input sequence.

    Args:
        input_sequence: A list or numpy array of 12 integers.

    Returns:
        A list or numpy array of 12 integers representing the transformed sequence.
    """
    # Convert input to list for consistent processing, handle potential numpy array input
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        input_list = list(input_sequence) # Ensure it's a mutable list

    n = len(input_list) # Should always be 12 based on examples

    # 1. Find the index of the first non-zero element (`first_nz`).
    first_nz = find_first_nonzero_index(input_list)

    # 2. If no non-zero element is found (the sequence is all zeros), return the original sequence.
    if first_nz == -1:
      # Return in the original format if possible (numpy array or list)
      return input_sequence

    # 3. Find the index of the last non-zero element (`last_nz`).
    last_nz = find_last_nonzero_index(input_list)

    # 4. Extract the sub-sequence (the "core block").
    core_block = input_list[first_nz : last_nz + 1]
    core_len = len(core_block)

    # 5. Calculate the target starting index for the core block.
    new_start = max(0, first_nz - 4)

    # 6. Create a new sequence of n zeros.
    output_sequence = [0] * n

    # 7. Place the extracted core block into the new sequence.
    # Calculate the actual end index in the output sequence, respecting bounds.
    end_index_output = min(new_start + core_len, n)
    # Calculate how many elements of the core block can actually be copied.
    num_elements_to_copy = end_index_output - new_start

    # Copy the appropriate part of the core block.
    if num_elements_to_copy > 0:
        output_sequence[new_start : end_index_output] = core_block[:num_elements_to_copy]

    # 8. Return the resulting sequence. Return as numpy array if input was numpy array.
    if isinstance(input_sequence, np.ndarray):
        return np.array(output_sequence)
    else:
        return output_sequence
```
```python
import math
import numpy as np # Use numpy for potential array operations, though list manipulation is sufficient here

"""
Transforms an input sequence of 12 digits (represented as a space-separated string) by:
1. Identifying the 'core block' which starts at the first non-zero element 
   and ends at the last non-zero element (inclusive).
2. Calculating a new starting position for this block by shifting its original 
   start position left by 4 indices, ensuring the new start index is not less than 0.
3. Creating a new sequence initialized with 12 zeros.
4. Placing the extracted 'core block' into the new sequence at the calculated 
   starting position. If the block would extend beyond the end of the 12-element sequence, 
   it is truncated. Zeros fill the remaining positions.
5. If the input sequence contains only zeros, it is returned unchanged.
"""

def find_first_nonzero_index(sequence):
  """Finds the index of the first non-zero element in a sequence."""
  for i, element in enumerate(sequence):
    if element != 0:
      return i
  return -1 # Indicate not found

def find_last_nonzero_index(sequence):
  """Finds the index of the last non-zero element in a sequence."""
  last_nz = -1
  for i, element in enumerate(sequence):
    if element != 0:
      last_nz = i
  return last_nz

def transform(input_str):
    # 1. Examine the input sequence of 12 integers. Convert string to list of ints.
    input_sequence = [int(x) for x in input_str.split()]
    n = len(input_sequence) # Should be 12

    # 2. Locate the index of the first non-zero integer (`first_nz`).
    first_nz = find_first_nonzero_index(input_sequence)

    # 3. If no non-zero integer is present, return the original sequence string.
    if first_nz == -1:
      return input_str

    # 4. If non-zero integers exist, locate the index of the last non-zero integer (`last_nz`).
    last_nz = find_last_nonzero_index(input_sequence)

    # 5. Identify the 'core block'.
    core_block = input_sequence[first_nz : last_nz + 1]
    core_len = len(core_block)

    # 6. Calculate the intended new starting index.
    # 7. Adjust this new starting index (clamp at 0).
    new_start = max(0, first_nz - 4)

    # 8. Create a new sequence of 12 zeros.
    output_sequence = [0] * n

    # 9. Copy the elements of the 'core block' into the new sequence, starting at `new_start`.
    #    Ensure that you do not attempt to write past the end of the 12-element new sequence.
    # Calculate how many elements can actually be placed.
    elements_to_copy = min(core_len, n - new_start)

    # Perform the copy using slicing.
    if elements_to_copy > 0:
        output_sequence[new_start : new_start + elements_to_copy] = core_block[0 : elements_to_copy]

    # 10. Return the newly constructed sequence as a space-separated string.
    return " ".join(map(str, output_sequence))
```
