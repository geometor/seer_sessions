
## train_1

**input:**
```
0 0 0 0 0 3 9 3 9 8 2 4
```


**output:**
```
0 0 3 9 3 9 8 2 4 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 8 7 4 5 1 2 0
```


**output:**
```
0 0 8 7 4 5 1 2 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 2 6 8 0 0 0 0
```


**output:**
```
0 0 2 6 8 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 1 1 6 4 0 0
```


**output:**
```
0 0 0 1 1 6 4 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 3 7 9 1
```


**output:**
```
0 0 0 0 0 3 7 9 1 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 5 9 1 5 0 0
```


**output:**
```
0 0 0 5 9 1 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 7 9 4 0 0 0
```


**output:**
```
0 0 0 7 9 4 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are lists of 12 single digits (0-9).
2.  **Core Content:** Each input list contains a sequence of non-zero digits, possibly preceded and followed by zeros. There might also be zeros interspersed within or immediately following the non-zero digits that seem to be part of a "block".
3.  **Transformation:** The core transformation appears to be a positional shift of a specific part of the input sequence.
4.  **Identifying the "Block":** The significant part of the sequence seems to start from the *first* non-zero digit encountered when reading from left to right. This block extends from that first non-zero digit all the way to the end of the input sequence.
5.  **The Shift:** This identified block is moved 3 positions to the left in the output sequence.
6.  **Padding:** Zeros are used to fill the space. The number of leading zeros in the output corresponds to the new starting position of the block. Trailing zeros are added to ensure the output sequence also has a length of 12.
7.  **Edge Case:** If the input sequence consists entirely of zeros, the output is identical (all zeros). This fits the general rule if we consider that no block is identified to be shifted.

**YAML Facts:**


```yaml
task_description: "Shift a trailing sub-sequence (starting from the first non-zero digit) left by 3 positions within a fixed-length digit list."
elements:
  - object: digit_sequence
    properties:
      - type: list
      - item_type: integer (0-9)
      - length: 12
      - role: container for digits (input or output)
  - object: zero_digit
    properties:
      - value: 0
      - role: padding (leading/trailing), potential part of the active_block
  - object: non_zero_digit
    properties:
      - value: integer (1-9)
      - role: marker, content
  - object: active_block
    properties:
      - type: sub-sequence
      - definition: The portion of the input sequence starting from the index of the first non-zero digit found, extending to the end of the sequence.
      - contains: The first non-zero digit and all subsequent digits (including zeros) from the input.
    relationships:
      - determined_by: position of the first non-zero digit
  - object: position
    properties:
      - type: index (0-based)
      - role: location identifier within the sequence
actions:
  - action: identify_first_non_zero_index
    description: Find the index of the first digit greater than 0 in the input sequence.
    inputs: input_sequence
    outputs: start_index (or indication of none found)
  - action: extract_active_block
    description: Get the sub-sequence from the identified start_index to the end of the input sequence.
    inputs: input_sequence, start_index
    outputs: active_block (sub-sequence)
  - action: shift_block_position
    description: Calculate the new starting index for the active_block in the output.
    inputs: start_index
    calculation: new_start_index = start_index - 3
    outputs: new_start_index
  - action: construct_output_sequence
    description: Assemble the final 12-digit output sequence.
    steps:
      - If no non-zero digit was found in the input, return the input sequence directly.
      - Otherwise, create a new list.
      - Add 'new_start_index' number of zeros to the list.
      - Append the 'active_block' to the list.
      - Append trailing zeros until the list length is 12.
    inputs: new_start_index, active_block, original_input (for edge case)
    outputs: output_sequence
relationships:
  - type: positional_shift
    subject: active_block
    direction: left
    magnitude: 3 indices
    reference_point: start_index of the block in the input vs. output
```


**Natural Language Program:**

1.  Examine the input list of 12 digits to find the index of the first digit that is not zero. Let this index be `start_index`.
2.  If no non-zero digit exists in the input list (i.e., all digits are 0), the output list is identical to the input list.
3.  If a non-zero digit is found at `start_index`:
    a.  Define the `active_block` as the sub-list containing all digits from `start_index` to the end of the input list.
    b.  Calculate the target starting position for this block in the output list: `new_start_index = start_index - 3`.
    c.  Construct the output list:
        i.  Begin with `new_start_index` zeros.
        ii. Append the `active_block`.
        iii. Append additional zeros to the end until the total length of the output list reaches 12.
4.  Return the constructed output list.
```python
"""
Shift a trailing sub-sequence (starting from the first non-zero digit) left by 3 positions within a fixed-length digit list.

1. Examine the input list of 12 digits to find the index of the first digit that is not zero. Let this index be `start_index`.
2. If no non-zero digit exists in the input list (i.e., all digits are 0), the output list is identical to the input list.
3. If a non-zero digit is found at `start_index`:
    a. Define the `active_block` as the sub-list containing all digits from `start_index` to the end of the input list.
    b. Calculate the target starting position for this block in the output list: `new_start_index = start_index - 3`.
    c. Construct the output list:
        i. Begin with `new_start_index` zeros.
        ii. Append the `active_block`.
        iii. Append additional zeros to the end until the total length of the output list reaches 12.
4. Return the constructed output list.
"""

# No specific imports needed for basic list operations

def find_first_non_zero_index(digit_list):
    """Finds the index of the first non-zero digit in a list."""
    for index, digit in enumerate(digit_list):
        if digit != 0:
            return index
    return -1 # Return -1 if no non-zero digit is found

def transform(input_list):
    """
    Applies the transformation rule to the input list of digits.
    """
    # Define the fixed length of the sequence
    list_length = 12

    # 1. Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_list)

    # 2. Handle the case where all digits are zero.
    if start_index == -1:
        return list(input_list) # Return a copy of the input list

    # 3. If a non-zero digit is found:
    # a. Extract the active block (from the first non-zero digit to the end).
    active_block = input_list[start_index:]

    # b. Calculate the new starting position for the block.
    #    Ensure the new start index isn't negative, though based on examples
    #    it seems the first non-zero will always be at index >= 3 if present.
    #    If it could be less than 3, we might need clarification.
    #    For now, assume it's always >= 3 if a non-zero exists.
    new_start_index = start_index - 3
    # Ensure non-negative index, though likely unnecessary based on examples
    # new_start_index = max(0, new_start_index)

    # c. Construct the output list.
    # Initialize the output list
    output_list = []

    # i. Add leading zeros.
    output_list.extend([0] * new_start_index)

    # ii. Append the active block.
    output_list.extend(active_block)

    # iii. Append trailing zeros to reach the fixed length.
    trailing_zeros_count = list_length - len(output_list)
    if trailing_zeros_count > 0:
        output_list.extend([0] * trailing_zeros_count)
    # Handle potential overshoot if active_block makes list longer than 12
    # after shifting (unlikely given problem constraints but good practice)
    elif trailing_zeros_count < 0:
         output_list = output_list[:list_length]


    # 4. Return the constructed output list.
    return output_list

```
```python
"""
Transform a sequence of 12 digits based on the following rules:

1. Define the fixed sequence length as 12 and the shift amount as 3 positions to the left.
2. Iterate through the input sequence (list or array of 12 digits) from the beginning (index 0) to find the index of the first digit that is not 0. Let this be `start_index`.
3. Case 1: No non-zero digit found. If all digits in the input sequence are 0, the output sequence is identical to the input sequence.
4. Case 2: Non-zero digit found at `start_index`.
    a. Extract the `active_block`, which is the sub-sequence containing all digits from `start_index` to the end of the input sequence.
    b. Calculate the target starting position for this block in the output sequence: `new_start_index = start_index - 3`.
    c. Construct the output sequence (length 12):
        i. Start with `new_start_index` zeros.
        ii. Append the `active_block`.
        iii. Append trailing zeros until the total length of the output sequence reaches 12.
5. Return the constructed output sequence.
"""

import numpy as np

def find_first_non_zero_index(sequence):
    """
    Finds the index of the first non-zero element in a sequence.

    Args:
        sequence: A list or NumPy array of numbers.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    for index, element in enumerate(sequence):
        if element != 0:
            return index
    return -1

def transform(input_sequence):
    """
    Applies the described transformation to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 12 digits.

    Returns:
        A NumPy array representing the transformed sequence of 12 digits.
    """
    # Define constants
    sequence_length = 12
    shift_amount = 3

    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence)

    # 1. & 2. Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_array)

    # 3. Handle the case where all digits are zero.
    if start_index == -1:
        # Return a copy of the input array
        return input_array.copy()

    # 4. Handle the case where a non-zero digit is found.
    # a. Extract the active block (from the first non-zero digit to the end).
    active_block = input_array[start_index:]

    # b. Calculate the new starting position for the block.
    new_start_index = start_index - shift_amount
    # It's assumed based on examples that start_index >= shift_amount if non-zero exists.
    # Add a check just in case, though it might mask an unexpected input pattern.
    new_start_index = max(0, new_start_index)

    # c. Construct the output sequence.
    # i. Create the leading zeros part.
    leading_zeros = np.zeros(new_start_index, dtype=input_array.dtype)

    # ii. Concatenate leading zeros and the active block.
    # Note: active_block is already a NumPy array
    partial_output = np.concatenate((leading_zeros, active_block))

    # iii. Pad with trailing zeros or truncate to reach the fixed length.
    current_length = len(partial_output)
    if current_length < sequence_length:
        # Append trailing zeros
        trailing_zeros_count = sequence_length - current_length
        trailing_zeros = np.zeros(trailing_zeros_count, dtype=input_array.dtype)
        output_array = np.concatenate((partial_output, trailing_zeros))
    elif current_length > sequence_length:
        # Truncate if somehow the shifted block makes it too long
        output_array = partial_output[:sequence_length]
    else:
        # Already the correct length
        output_array = partial_output

    # 5. Return the constructed output sequence.
    return output_array

```

Previous Code:
```python
"""
Transform a sequence of 12 digits based on the following rules:

1. Define the fixed sequence length as 12 and the shift amount as 3 positions to the left.
2. Iterate through the input sequence (list or array of 12 digits) from the beginning (index 0) to find the index of the first digit that is not 0. Let this be `start_index`.
3. Case 1: No non-zero digit found. If all digits in the input sequence are 0, the output sequence is identical to the input sequence.
4. Case 2: Non-zero digit found at `start_index`.
    a. Extract the `active_block`, which is the sub-sequence containing all digits from `start_index` to the end of the input sequence.
    b. Calculate the target starting position for this block in the output sequence: `new_start_index = start_index - 3`.
    c. Construct the output sequence (length 12):
        i. Start with `new_start_index` zeros.
        ii. Append the `active_block`.
        iii. Append trailing zeros until the total length of the output sequence reaches 12.
5. Return the constructed output sequence.
"""

import numpy as np

def find_first_non_zero_index(sequence):
    """
    Finds the index of the first non-zero element in a sequence.

    Args:
        sequence: A list or NumPy array of numbers.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    for index, element in enumerate(sequence):
        if element != 0:
            return index
    return -1

def transform(input_sequence):
    """
    Applies the described transformation to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 12 digits.

    Returns:
        A NumPy array representing the transformed sequence of 12 digits.
    """
    # Define constants
    sequence_length = 12
    shift_amount = 3

    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence)

    # 1. & 2. Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_array)

    # 3. Handle the case where all digits are zero.
    if start_index == -1:
        # Return a copy of the input array
        return input_array.copy()

    # 4. Handle the case where a non-zero digit is found.
    # a. Extract the active block (from the first non-zero digit to the end).
    active_block = input_array[start_index:]

    # b. Calculate the new starting position for the block.
    new_start_index = start_index - shift_amount
    # It's assumed based on examples that start_index >= shift_amount if non-zero exists.
    # Add a check just in case, though it might mask an unexpected input pattern.
    new_start_index = max(0, new_start_index)

    # c. Construct the output sequence.
    # i. Create the leading zeros part.
    leading_zeros = np.zeros(new_start_index, dtype=input_array.dtype)

    # ii. Concatenate leading zeros and the active block.
    # Note: active_block is already a NumPy array
    partial_output = np.concatenate((leading_zeros, active_block))

    # iii. Pad with trailing zeros or truncate to reach the fixed length.
    current_length = len(partial_output)
    if current_length < sequence_length:
        # Append trailing zeros
        trailing_zeros_count = sequence_length - current_length
        trailing_zeros = np.zeros(trailing_zeros_count, dtype=input_array.dtype)
        output_array = np.concatenate((partial_output, trailing_zeros))
    elif current_length > sequence_length:
        # Truncate if somehow the shifted block makes it too long
        output_array = partial_output[:sequence_length]
    else:
        # Already the correct length
        output_array = partial_output

    # 5. Return the constructed output sequence.
    return output_array

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
## Assessment and Strategy

**General Assessment:**

The initial analysis correctly identified the core transformation pattern: finding the first non-zero digit, extracting the subsequent block, shifting it left by 3 positions, and padding with zeros to maintain a fixed length of 12. The error reported ("The truth value of an array with more than one element is ambiguous") arose because the test harness likely passed the raw input *string* to the `transform` function, which expected a list or array of *integers*. The provided Python code attempted to use NumPy operations, which failed when applied directly to a string or when comparisons were made between string characters and integers.

**Strategy:**

1.  **Input Parsing:** Modify the `transform` function to explicitly handle the input string format. This involves splitting the string by spaces and converting the resulting digit strings into integers.
2.  **Core Logic:** Keep the fundamental logic identified: find the index of the first non-zero integer, extract the block from that index onwards, calculate the new starting index (`start_index - 3`), and construct the new sequence.
3.  **Output Formatting:** Convert the resulting list of integers back into a space-separated string format for the final output.
4.  **Refinement:** Use standard Python list operations, as NumPy is not strictly necessary for this task and adds complexity if not handled correctly with input types.
5.  **Verification:** Mentally re-run the refined logic against each training example to ensure consistency.

## Metrics Gathering

We will analyze each training example to confirm the pattern.



*code_execution:*
```python
import numpy as np

def analyze_example(input_str, output_str):
    input_list = [int(d) for d in input_str.split()]
    output_list = [int(d) for d in output_str.split()]
    sequence_length = 12
    shift_amount = 3

    start_index = -1
    for index, digit in enumerate(input_list):
        if digit != 0:
            start_index = index
            break

    if start_index == -1:
        active_block = []
        new_start_index = -1 # Or irrelevant
        block_length = 0
    else:
        active_block = input_list[start_index:]
        new_start_index = start_index - shift_amount
        block_length = len(active_block)

    # Reconstruct expected output based on logic
    expected_output = []
    if start_index == -1:
        expected_output = list(input_list)
    else:
        # Leading zeros
        expected_output.extend([0] * new_start_index)
        # Active block
        expected_output.extend(active_block)
        # Trailing zeros
        trailing_zeros_count = sequence_length - len(expected_output)
        if trailing_zeros_count > 0:
            expected_output.extend([0] * trailing_zeros_count)
        elif trailing_zeros_count < 0:
            expected_output = expected_output[:sequence_length]


    match = (expected_output == output_list)

    return {
        "input": input_str,
        "output": output_str,
        "input_list": input_list,
        "output_list": output_list,
        "start_index": start_index,
        "active_block": active_block,
        "block_length": block_length,
        "new_start_index": new_start_index,
        "reconstructed_output": expected_output,
        "match": match
    }

examples = [
    {"input": "0 0 0 0 0 3 9 3 9 8 2 4", "output": "0 0 3 9 3 9 8 2 4 0 0 0"},
    {"input": "0 0 0 0 0 8 7 4 5 1 2 0", "output": "0 0 8 7 4 5 1 2 0 0 0 0"},
    {"input": "0 0 0 0 0 2 6 8 0 0 0 0", "output": "0 0 2 6 8 0 0 0 0 0 0 0"},
    {"input": "0 0 0 0 0 0 1 1 6 4 0 0", "output": "0 0 0 1 1 6 4 0 0 0 0 0"},
    {"input": "0 0 0 0 0 0 0 0 3 7 9 1", "output": "0 0 0 0 0 3 7 9 1 0 0 0"},
    {"input": "0 0 0 0 0 0 5 9 1 5 0 0", "output": "0 0 0 5 9 1 5 0 0 0 0 0"},
    {"input": "0 0 0 0 0 0 7 9 4 0 0 0", "output": "0 0 0 7 9 4 0 0 0 0 0 0"},
    # Add a hypothetical all-zero case
    {"input": "0 0 0 0 0 0 0 0 0 0 0 0", "output": "0 0 0 0 0 0 0 0 0 0 0 0"},
]

results = [analyze_example(ex["input"], ex["output"]) for ex in examples]

for i, res in enumerate(results):
    print(f"--- Example {i+1} ---")
    print(f"Input: {res['input']}")
    print(f"Output: {res['output']}")
    print(f"First non-zero index (start_index): {res['start_index']}")
    print(f"Active block: {res['active_block']}")
    print(f"Active block length: {res['block_length']}")
    print(f"New start index (start_index - 3): {res['new_start_index']}")
    print(f"Reconstructed Output: {res['reconstructed_output']}")
    print(f"Logic Matches Output: {res['match']}")
    print("-" * 15)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 ---
Input: 0 0 0 0 0 3 9 3 9 8 2 4
Output: 0 0 3 9 3 9 8 2 4 0 0 0
First non-zero index (start_index): 5
Active block: [3, 9, 3, 9, 8, 2, 4]
Active block length: 7
New start index (start_index - 3): 2
Reconstructed Output: [0, 0, 3, 9, 3, 9, 8, 2, 4, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 2 ---
Input: 0 0 0 0 0 8 7 4 5 1 2 0
Output: 0 0 8 7 4 5 1 2 0 0 0 0
First non-zero index (start_index): 5
Active block: [8, 7, 4, 5, 1, 2, 0]
Active block length: 7
New start index (start_index - 3): 2
Reconstructed Output: [0, 0, 8, 7, 4, 5, 1, 2, 0, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 3 ---
Input: 0 0 0 0 0 2 6 8 0 0 0 0
Output: 0 0 2 6 8 0 0 0 0 0 0 0
First non-zero index (start_index): 5
Active block: [2, 6, 8, 0, 0, 0, 0]
Active block length: 7
New start index (start_index - 3): 2
Reconstructed Output: [0, 0, 2, 6, 8, 0, 0, 0, 0, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 4 ---
Input: 0 0 0 0 0 0 1 1 6 4 0 0
Output: 0 0 0 1 1 6 4 0 0 0 0 0
First non-zero index (start_index): 6
Active block: [1, 1, 6, 4, 0, 0]
Active block length: 6
New start index (start_index - 3): 3
Reconstructed Output: [0, 0, 0, 1, 1, 6, 4, 0, 0, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 5 ---
Input: 0 0 0 0 0 0 0 0 3 7 9 1
Output: 0 0 0 0 0 3 7 9 1 0 0 0
First non-zero index (start_index): 8
Active block: [3, 7, 9, 1]
Active block length: 4
New start index (start_index - 3): 5
Reconstructed Output: [0, 0, 0, 0, 0, 3, 7, 9, 1, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 6 ---
Input: 0 0 0 0 0 0 5 9 1 5 0 0
Output: 0 0 0 5 9 1 5 0 0 0 0 0
First non-zero index (start_index): 6
Active block: [5, 9, 1, 5, 0, 0]
Active block length: 6
New start index (start_index - 3): 3
Reconstructed Output: [0, 0, 0, 5, 9, 1, 5, 0, 0, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 7 ---
Input: 0 0 0 0 0 0 7 9 4 0 0 0
Output: 0 0 0 7 9 4 0 0 0 0 0 0
First non-zero index (start_index): 6
Active block: [7, 9, 4, 0, 0, 0]
Active block length: 6
New start index (start_index - 3): 3
Reconstructed Output: [0, 0, 0, 7, 9, 4, 0, 0, 0, 0, 0, 0]
Logic Matches Output: True
---------------
--- Example 8 ---
Input: 0 0 0 0 0 0 0 0 0 0 0 0
Output: 0 0 0 0 0 0 0 0 0 0 0 0
First non-zero index (start_index): -1
Active block: []
Active block length: 0
New start index (start_index - 3): -1
Reconstructed Output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Logic Matches Output: True
---------------

```
**Metrics Summary:** The code execution confirms that the logic (find first non-zero, extract block, shift left by 3, pad) correctly reproduces the output for all provided training examples, including the inferred all-zero case. The `start_index` ranges from 5 to 8 in the non-zero examples, resulting in `new_start_index` values from 2 to 5. The `active_block` length varies. The fixed total length of 12 is maintained.

## YAML Facts


```yaml
task_description: "Parse a string of 12 space-separated digits, identify the sub-sequence starting from the first non-zero digit, shift this sub-sequence left by 3 positions within a 12-element list, pad with zeros, and format the result as a space-separated string."
constants:
  - name: sequence_length
    value: 12
    type: integer
    description: The fixed total number of digits in the input and output sequences.
  - name: shift_amount
    value: 3
    type: integer
    description: The number of positions to shift the active block to the left.
elements:
  - object: input_string
    properties:
      - type: string
      - format: space-separated digits (e.g., "0 0 3 ...")
      - length_constraint: Represents 12 digits
      - role: raw input data
  - object: output_string
    properties:
      - type: string
      - format: space-separated digits
      - length_constraint: Represents 12 digits
      - role: final transformed data
  - object: digit_list
    properties:
      - type: list
      - item_type: integer (0-9)
      - length: 12
      - role: internal representation derived from input_string, basis for transformation, precursor to output_string
  - object: zero_digit
    properties:
      - value: 0
      - type: integer
      - role: padding (leading/trailing), part of active_block
  - object: non_zero_digit
    properties:
      - value: integer (1-9)
      - type: integer
      - role: marker for start of active_block, content
  - object: active_block
    properties:
      - type: sub-list (of digit_list)
      - definition: The portion of the digit_list starting from the index of the first non-zero digit, extending to the end of the list.
      - contains: The first non-zero digit and all subsequent digits (including zeros) from the original digit_list.
    relationships:
      - determined_by: position of the first non-zero digit in digit_list
  - object: position_index
    properties:
      - type: integer (0-based)
      - role: location identifier within digit_list
      - names: start_index (first non-zero), new_start_index (target position for active_block)
actions:
  - action: parse_input_string
    description: Convert the input string into a list of 12 integers.
    inputs: input_string
    outputs: digit_list
  - action: find_first_non_zero_index
    description: Find the index of the first digit greater than 0 in the digit_list.
    inputs: digit_list
    outputs: start_index (integer >= 0, or -1 if none found)
  - action: handle_all_zeros
    description: If no non-zero digit is found (start_index is -1), the original digit_list is the result.
    inputs: start_index
    condition: start_index == -1
    outputs: result_list (identical to original digit_list)
  - action: extract_active_block
    description: Get the sub-list from the identified start_index to the end of the digit_list.
    inputs: digit_list, start_index
    condition: start_index != -1
    outputs: active_block (sub-list)
  - action: calculate_new_start_index
    description: Determine the starting index for the active_block in the output list.
    inputs: start_index
    condition: start_index != -1
    calculation: new_start_index = start_index - shift_amount
    outputs: new_start_index (integer >= 0)
  - action: construct_output_list
    description: Assemble the final 12-digit list based on the calculated position and block.
    inputs: new_start_index, active_block, sequence_length
    condition: start_index != -1
    steps:
      - Create a list of 'new_start_index' zeros.
      - Append the 'active_block' to this list.
      - Append trailing zeros until the list length equals 'sequence_length'.
      - Handle potential truncation if the shifted block would exceed sequence_length (though not observed in examples).
    outputs: result_list (list of 12 integers)
  - action: format_output_string
    description: Convert the result list of integers back into a space-separated string.
    inputs: result_list
    outputs: output_string
```


## Natural Language Program

1.  **Receive Input:** Start with the input string containing 12 space-separated digits.
2.  **Parse Input:** Convert the input string into a list of 12 integer digits. Let this be `digit_list`.
3.  **Find Start:** Iterate through `digit_list` from the beginning (index 0) to find the index of the first digit that is not 0. Let this index be `start_index`.
4.  **Handle All Zeros:** If no non-zero digit is found (`start_index` remains undefined or is marked as -1), the final result list is identical to the initial `digit_list`. Proceed to Step 8.
5.  **Extract Block:** If a non-zero digit is found at `start_index`, extract the `active_block`, which is the sub-list containing all elements of `digit_list` from `start_index` to the end.
6.  **Calculate New Position:** Determine the target starting index for the `active_block` in the output: `new_start_index = start_index - 3`.
7.  **Construct Output List:** Create a new list (`result_list`) of 12 digits as follows:
    a.  Add `new_start_index` number of zeros to the beginning of `result_list`.
    b.  Append all digits from the `active_block` to `result_list`.
    c.  Append trailing zeros to `result_list` until its total length reaches 12.
8.  **Format Output:** Convert the `result_list` (either from Step 4 or Step 7) back into a string where each digit is separated by a space.
9.  **Return Output:** Return the final formatted string.
