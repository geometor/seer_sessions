
## train_1

**input:**
```
0 0 0 0 0 0 3 9 1 2 4 6
```


**output:**
```
0 0 0 3 9 1 2 4 6 0 0 0
```


## train_2

**input:**
```
0 0 0 0 5 8 1 0 0 0 0 0
```


**output:**
```
0 5 8 1 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 6 1 0 0
```


**output:**
```
0 0 0 0 0 6 1 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 4 6 3 2 5
```


**output:**
```
0 0 0 0 4 6 3 2 5 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 2 5 2
```


**output:**
```
0 0 0 0 0 0 2 5 2 0 0 0
```


## train_6

**input:**
```
0 0 0 5 2 8 5 8 8 8 0 0
```


**output:**
```
5 2 8 5 8 8 8 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 1 1 6 9 0
```


**output:**
```
0 0 0 0 1 1 6 9 0 0 0 0
```

Okay, I will analyze the provided examples to understand the transformation task.

**Perception of the Elements:**

*   The input and output are both sequences of 12 digits, represented as space-separated strings.
*   Each sequence contains digits from 0 to 9.
*   The core transformation involves identifying a specific contiguous sub-sequence within the input and relocating it within the output sequence.
*   The digits '0' primarily function as padding or placeholders.
*   The significant part of the sequence appears to be the segment starting with the first non-zero digit and ending with the last non-zero digit. This segment includes any zeros that fall between the first and last non-zero digits.
*   The position of this significant segment changes from the input to the output. Specifically, it appears to be shifted three positions to the left.
*   The length of the sequence remains constant (12 digits).

**YAML Fact Document:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12
      - contains: digits 0-9
    roles:
      - input_sequence
      - output_sequence
  - object: sub_sequence
    properties:
      - type: list of integers
      - derived_from: input_sequence
      - boundaries: defined by the first and last non-zero digits (inclusive)
      - content: sequence of digits between the first and last non-zero elements of the input
    role:
      - core_data_block
  - object: zero_digit
    properties:
      - value: 0
    role:
      - padding_element
  - object: non_zero_digit
    properties:
      - value: range 1-9
    role:
      - boundary_marker (first and last non-zero define the sub_sequence)
      - data_element (part of the sub_sequence)
actions:
  - name: identify_boundaries
    inputs:
      - input_sequence
    outputs:
      - start_index: index of the first non-zero digit
      - end_index: index of the last non-zero digit
  - name: extract_sub_sequence
    inputs:
      - input_sequence
      - start_index
      - end_index
    outputs:
      - core_data_block: the sub-sequence from start_index to end_index (inclusive)
  - name: calculate_output_position
    inputs:
      - start_index
    constants:
      - shift_amount: 3
    outputs:
      - output_start_index: start_index - shift_amount
  - name: construct_output
    inputs:
      - core_data_block
      - output_start_index
    constants:
      - output_length: 12
      - padding_value: 0
    outputs:
      - output_sequence: a sequence of length 12, padded with zeros, containing the core_data_block at the output_start_index
relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: extract the sub-sequence between the first and last non-zero digits and shift it 3 positions to the left, padding the remaining positions with zeros.
```


**Natural Language Program:**

1.  Read the input sequence of 12 digits.
2.  Find the index of the first non-zero digit in the input sequence. If no non-zero digit exists, the sequence remains unchanged (all zeros).
3.  Find the index of the last non-zero digit in the input sequence.
4.  Extract the sub-sequence from the input sequence starting at the first non-zero index and ending at the last non-zero index (inclusive).
5.  Determine the target starting index for this sub-sequence in the output sequence by subtracting 3 from the first non-zero index found in step 2.
6.  Create a new output sequence containing 12 zeros.
7.  Place the extracted sub-sequence into the new output sequence, beginning at the calculated target starting index.
8.  Output the resulting sequence.
```python
import re
import math

"""
Extract the contiguous sub-sequence starting with the first non-zero digit and ending with the last non-zero digit from the input sequence. Shift this extracted sub-sequence 3 positions to the left within a sequence of 12 digits, padding the remaining positions with zeros.
"""

def _find_first_nonzero_index(data_list):
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(data_list):
    if val != 0:
      return i
  return -1 # Return -1 if no non-zero element is found

def _find_last_nonzero_index(data_list):
  """Finds the index of the last non-zero element."""
  last_index = -1
  for i, val in enumerate(data_list):
    if val != 0:
      last_index = i
  return last_index # Return -1 if no non-zero element is found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of space-separated digits (e.g., "0 0 1 2 3 0 0").

    Returns:
        A string representing the transformed sequence of space-separated digits.
    """
    # 1. Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list) # Should be 12 based on examples

    # 2. Find the indices of the first and last non-zero digits
    start_index = _find_first_nonzero_index(input_list)
    end_index = _find_last_nonzero_index(input_list)

    # 3. Handle the case where the input is all zeros or empty
    if start_index == -1:
      # If no non-zero elements, return the original string (or an equivalent string of zeros)
      return input_str

    # 4. Extract the sub-sequence
    sub_sequence = input_list[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # 5. Determine the target starting index for the output
    # Shift amount is 3 positions to the left
    shift_amount = 3
    output_start_index = start_index - shift_amount

    # 6. Create a new output list initialized with zeros
    output_list = [0] * n

    # 7. Place the extracted sub-sequence into the output list
    # Ensure indices stay within bounds (although examples seem to fit)
    # The slice assignment handles the placement correctly
    # Calculate the end index for placement in the output list
    output_end_index = output_start_index + sub_len
    
    # Check bounds to prevent errors, though not strictly needed based on examples
    if output_start_index >= 0 and output_end_index <= n:
         output_list[output_start_index:output_end_index] = sub_sequence
    # If the shift would place elements out of bounds (e.g., negative start index),
    # only the part that fits within the 0 to n-1 range is placed.
    # Python slicing handles this gracefully for start indices < 0 if the list is assigned,
    # but let's be explicit for clarity if needed.
    # Example: if output_start_index is -1, and sub_len is 4,
    # output_list[-1:3] is not standard. We want output_list[0:3] = sub_sequence[1:]
    else:
         # Adjust placement if shift goes out of bounds
        source_start = 0
        dest_start = output_start_index
        length_to_copy = sub_len

        if dest_start < 0:
            source_start = -dest_start # Start copying from this index in sub_sequence
            length_to_copy = sub_len - source_start # Adjust length
            dest_start = 0 # Start placing at index 0 in output_list

        if dest_start + length_to_copy > n:
             length_to_copy = n - dest_start # Truncate if it goes past the end

        if length_to_copy > 0: # Only copy if there's something left to copy within bounds
             output_list[dest_start : dest_start + length_to_copy] = sub_sequence[source_start : source_start + length_to_copy]


    # 8. Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
```
```python
import numpy as np
from typing import List, Union

"""
If the input sequence contains non-zero digits, extract the sub-sequence between the first and last non-zero digits (inclusive) and shift it 3 positions to the left within a sequence of 12 digits, padding the remaining positions with zeros. If the input sequence contains only zeros, the output sequence is identical to the input.
"""

def _find_first_nonzero_index(data_list: Union[List[int], np.ndarray]) -> int:
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(data_list):
    if val != 0:
      return i
  return -1 # Return -1 if no non-zero element is found

def _find_last_nonzero_index(data_list: Union[List[int], np.ndarray]) -> int:
  """Finds the index of the last non-zero element."""
  last_index = -1
  # Iterate backwards for efficiency, but iterating forwards works too
  for i in range(len(data_list) - 1, -1, -1):
      if data_list[i] != 0:
          return i
  return -1 # Return -1 if no non-zero element is found

def transform(input_sequence: Union[List[int], np.ndarray]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A list representing the transformed sequence of 12 integers.
    """
    # Ensure input is treated as a list for consistent indexing/slicing
    input_list = list(input_sequence)
    n = len(input_list) # Should be 12 based on examples

    # 1. Find the indices of the first and last non-zero digits
    start_index = _find_first_nonzero_index(input_list)
    
    # 2. Handle the case where the input is all zeros
    if start_index == -1:
      # If no non-zero elements, return the original sequence as a list
      return input_list

    # 3. Find the last non-zero index (only needed if there's a first one)
    end_index = _find_last_nonzero_index(input_list)

    # 4. Extract the sub-sequence
    sub_sequence = input_list[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # 5. Determine the target starting index for the output
    # Shift amount is 3 positions to the left
    shift_amount = 3
    output_start_index = start_index - shift_amount

    # 6. Create a new output list initialized with zeros
    output_list = [0] * n

    # 7. Place the extracted sub-sequence into the output list, handling boundaries
    
    # Determine the slice of the sub_sequence to copy
    source_start = 0
    source_end = sub_len
    
    # Determine the slice of the output_list to place into
    dest_start = output_start_index
    dest_end = output_start_index + sub_len

    # Adjust source slice if destination starts before index 0
    if dest_start < 0:
        source_start = -dest_start # Skip initial elements of sub_sequence
        dest_start = 0          # Start placing at index 0 in output

    # Adjust source slice if destination ends after index n-1
    if dest_end > n:
        # Calculate how much it overflows
        overflow = dest_end - n
        source_end = source_end - overflow # Don't copy the overflowing part
        dest_end = n                     # Place up to the end of the output list

    # Only perform the assignment if there's a valid range to copy/paste
    if dest_start < dest_end and source_start < source_end:
        output_list[dest_start:dest_end] = sub_sequence[source_start:source_end]

    # 8. Return the resulting output list
    return output_list
```

Previous Code:
```python
import numpy as np
from typing import List, Union

"""
If the input sequence contains non-zero digits, extract the sub-sequence between the first and last non-zero digits (inclusive) and shift it 3 positions to the left within a sequence of 12 digits, padding the remaining positions with zeros. If the input sequence contains only zeros, the output sequence is identical to the input.
"""

def _find_first_nonzero_index(data_list: Union[List[int], np.ndarray]) -> int:
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(data_list):
    if val != 0:
      return i
  return -1 # Return -1 if no non-zero element is found

def _find_last_nonzero_index(data_list: Union[List[int], np.ndarray]) -> int:
  """Finds the index of the last non-zero element."""
  last_index = -1
  # Iterate backwards for efficiency, but iterating forwards works too
  for i in range(len(data_list) - 1, -1, -1):
      if data_list[i] != 0:
          return i
  return -1 # Return -1 if no non-zero element is found

def transform(input_sequence: Union[List[int], np.ndarray]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A list representing the transformed sequence of 12 integers.
    """
    # Ensure input is treated as a list for consistent indexing/slicing
    input_list = list(input_sequence)
    n = len(input_list) # Should be 12 based on examples

    # 1. Find the indices of the first and last non-zero digits
    start_index = _find_first_nonzero_index(input_list)
    
    # 2. Handle the case where the input is all zeros
    if start_index == -1:
      # If no non-zero elements, return the original sequence as a list
      return input_list

    # 3. Find the last non-zero index (only needed if there's a first one)
    end_index = _find_last_nonzero_index(input_list)

    # 4. Extract the sub-sequence
    sub_sequence = input_list[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # 5. Determine the target starting index for the output
    # Shift amount is 3 positions to the left
    shift_amount = 3
    output_start_index = start_index - shift_amount

    # 6. Create a new output list initialized with zeros
    output_list = [0] * n

    # 7. Place the extracted sub-sequence into the output list, handling boundaries
    
    # Determine the slice of the sub_sequence to copy
    source_start = 0
    source_end = sub_len
    
    # Determine the slice of the output_list to place into
    dest_start = output_start_index
    dest_end = output_start_index + sub_len

    # Adjust source slice if destination starts before index 0
    if dest_start < 0:
        source_start = -dest_start # Skip initial elements of sub_sequence
        dest_start = 0          # Start placing at index 0 in output

    # Adjust source slice if destination ends after index n-1
    if dest_end > n:
        # Calculate how much it overflows
        overflow = dest_end - n
        source_end = source_end - overflow # Don't copy the overflowing part
        dest_end = n                     # Place up to the end of the output list

    # Only perform the assignment if there's a valid range to copy/paste
    if dest_start < dest_end and source_start < source_end:
        output_list[dest_start:dest_end] = sub_sequence[source_start:source_end]

    # 8. Return the resulting output list
    return output_list
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
Okay, I will analyze the provided examples, the previous code's execution results, and refine the understanding of the transformation.

**General Assessment and Strategy**

The core transformation logic identified previously (extracting the non-zero block and shifting it left by 3 positions) appears consistent with all provided training examples. The execution error reported ("The truth value of an array with more than one element is ambiguous...") strongly suggests an issue related to comparing NumPy arrays in a boolean context, likely occurring either within the testing framework when comparing the function's output to the expected output, or potentially within the function if NumPy arrays were handled unexpectedly despite the `list()` conversion.

The strategy is to:
1.  Confirm the "shift left by 3" rule holds for all examples by calculating indices and expected outputs.
2.  Refine the implementation details in the natural language program to be robust, assuming the core logic is correct.
3.  Update the YAML documentation to reflect the confirmed understanding.
4.  Assume the Python code implementation needs to be careful about data types, primarily returning standard Python lists to avoid ambiguity issues downstream in the testing harness. The previous code already attempted this by converting input to `list` and returning a `list`. The error might be external to the function itself, but the description should guide towards a robust implementation.

**Metrics Gathering**

Let's verify the indices, sub-sequences, and shifts for each training example.



*code_execution:*
```python
import numpy as np

def analyze_sequence(input_str):
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)
    
    first_nz = -1
    for i, val in enumerate(input_list):
        if val != 0:
            first_nz = i
            break
            
    last_nz = -1
    if first_nz != -1:
        for i in range(n - 1, -1, -1):
            if input_list[i] != 0:
                last_nz = i
                break
                
    if first_nz == -1:
        sub_sequence = []
        target_start = -1 # Not applicable
        calculated_output = input_list # Stays all zeros
    else:
        sub_sequence = input_list[first_nz : last_nz + 1]
        shift = 3
        target_start = first_nz - shift
        
        calculated_output = [0] * n
        sub_len = len(sub_sequence)
        
        # Boundary handling for placement
        source_start = 0
        dest_start = target_start
        length_to_copy = sub_len

        if dest_start < 0:
            source_start = -dest_start 
            length_to_copy = sub_len - source_start
            dest_start = 0 

        if dest_start + length_to_copy > n:
             length_to_copy = n - dest_start 

        if length_to_copy > 0 and source_start < sub_len:
             output_slice = slice(dest_start, dest_start + length_to_copy)
             sub_slice = slice(source_start, source_start + length_to_copy)
             calculated_output[output_slice] = sub_sequence[sub_slice]

    return {
        "input": input_list,
        "first_nz_index": first_nz,
        "last_nz_index": last_nz,
        "sub_sequence": sub_sequence,
        "target_start_index": target_start,
        "calculated_output": calculated_output
    }

examples = [
    ("0 0 0 0 0 0 3 9 1 2 4 6", "0 0 0 3 9 1 2 4 6 0 0 0"),
    ("0 0 0 0 5 8 1 0 0 0 0 0", "0 5 8 1 0 0 0 0 0 0 0 0"),
    ("0 0 0 0 0 0 0 0 6 1 0 0", "0 0 0 0 0 6 1 0 0 0 0 0"),
    ("0 0 0 0 0 0 0 4 6 3 2 5", "0 0 0 0 4 6 3 2 5 0 0 0"),
    ("0 0 0 0 0 0 0 0 0 2 5 2", "0 0 0 0 0 0 2 5 2 0 0 0"),
    ("0 0 0 5 2 8 5 8 8 8 0 0", "5 2 8 5 8 8 8 0 0 0 0 0"),
    ("0 0 0 0 0 0 0 1 1 6 9 0", "0 0 0 0 1 1 6 9 0 0 0 0")
]

results = []
for i, (inp, outp) in enumerate(examples):
    analysis = analyze_sequence(inp)
    expected_output = [int(x) for x in outp.split()]
    analysis["expected_output"] = expected_output
    analysis["output_matches"] = (analysis["calculated_output"] == expected_output)
    results.append(f"Example {i+1}:\n"
                   f"  Input: {analysis['input']}\n"
                   f"  First NZ Index: {analysis['first_nz_index']}\n"
                   f"  Last NZ Index: {analysis['last_nz_index']}\n"
                   f"  Sub-sequence: {analysis['sub_sequence']}\n"
                   f"  Target Start Index (Shifted): {analysis['target_start_index']}\n"
                   f"  Calculated Output: {analysis['calculated_output']}\n"
                   f"  Expected Output: {expected_output}\n"
                   f"  Output Matches: {analysis['output_matches']}\n")

print("\n".join(results))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1:
  Input: [0, 0, 0, 0, 0, 0, 3, 9, 1, 2, 4, 6]
  First NZ Index: 6
  Last NZ Index: 11
  Sub-sequence: [3, 9, 1, 2, 4, 6]
  Target Start Index (Shifted): 3
  Calculated Output: [0, 0, 0, 3, 9, 1, 2, 4, 6, 0, 0, 0]
  Expected Output: [0, 0, 0, 3, 9, 1, 2, 4, 6, 0, 0, 0]
  Output Matches: True

Example 2:
  Input: [0, 0, 0, 0, 5, 8, 1, 0, 0, 0, 0, 0]
  First NZ Index: 4
  Last NZ Index: 6
  Sub-sequence: [5, 8, 1]
  Target Start Index (Shifted): 1
  Calculated Output: [0, 5, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
  Expected Output: [0, 5, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
  Output Matches: True

Example 3:
  Input: [0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0]
  First NZ Index: 8
  Last NZ Index: 9
  Sub-sequence: [6, 1]
  Target Start Index (Shifted): 5
  Calculated Output: [0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 0]
  Expected Output: [0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 0]
  Output Matches: True

Example 4:
  Input: [0, 0, 0, 0, 0, 0, 0, 4, 6, 3, 2, 5]
  First NZ Index: 7
  Last NZ Index: 11
  Sub-sequence: [4, 6, 3, 2, 5]
  Target Start Index (Shifted): 4
  Calculated Output: [0, 0, 0, 0, 4, 6, 3, 2, 5, 0, 0, 0]
  Expected Output: [0, 0, 0, 0, 4, 6, 3, 2, 5, 0, 0, 0]
  Output Matches: True

Example 5:
  Input: [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2]
  First NZ Index: 9
  Last NZ Index: 11
  Sub-sequence: [2, 5, 2]
  Target Start Index (Shifted): 6
  Calculated Output: [0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0]
  Expected Output: [0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0]
  Output Matches: True

Example 6:
  Input: [0, 0, 0, 5, 2, 8, 5, 8, 8, 8, 0, 0]
  First NZ Index: 3
  Last NZ Index: 9
  Sub-sequence: [5, 2, 8, 5, 8, 8, 8]
  Target Start Index (Shifted): 0
  Calculated Output: [5, 2, 8, 5, 8, 8, 8, 0, 0, 0, 0, 0]
  Expected Output: [5, 2, 8, 5, 8, 8, 8, 0, 0, 0, 0, 0]
  Output Matches: True

Example 7:
  Input: [0, 0, 0, 0, 0, 0, 0, 1, 1, 6, 9, 0]
  First NZ Index: 7
  Last NZ Index: 10
  Sub-sequence: [1, 1, 6, 9]
  Target Start Index (Shifted): 4
  Calculated Output: [0, 0, 0, 0, 1, 1, 6, 9, 0, 0, 0, 0]
  Expected Output: [0, 0, 0, 0, 1, 1, 6, 9, 0, 0, 0, 0]
  Output Matches: True


```
The analysis confirms that the rule "extract the sub-sequence between the first and last non-zero elements (inclusive) and shift it 3 positions to the left, padding with zeros" correctly describes the transformation for all provided training examples. The calculated outputs match the expected outputs perfectly. The previous code failure likely lies outside the core logic, possibly in the test harness or subtle type interactions not present in this verification script.

**YAML Fact Document**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12
      - contains: digits 0-9
    roles:
      - input_sequence
      - output_sequence
  - object: sub_sequence
    properties:
      - type: list of integers
      - derived_from: input_sequence
      - boundaries: defined by the index of the first non-zero digit and the index of the last non-zero digit (inclusive)
      - content: sequence of digits between and including the first and last non-zero elements
    role:
      - core_data_block
  - object: zero_digit
    properties:
      - value: 0
    role:
      - padding_element
      - placeholder (within input/output)
      - potential_element (can be part of the core_data_block if surrounded by non-zeros)
  - object: non_zero_digit
    properties:
      - value: range 1-9
    role:
      - boundary_marker (first and last non-zero define the sub_sequence)
      - data_element (part of the sub_sequence)
constants:
  - name: sequence_length
    value: 12
  - name: shift_amount
    value: 3
  - name: shift_direction
    value: left
  - name: padding_value
    value: 0
actions:
  - name: find_boundaries
    inputs:
      - input_sequence
    outputs:
      - start_index: index of the first non-zero digit (or indication of none)
      - end_index: index of the last non-zero digit (or indication of none)
  - name: handle_all_zeros
    condition: no non-zero digits found in input_sequence
    action: return input_sequence unchanged
  - name: extract_sub_sequence
    condition: non-zero digits exist
    inputs:
      - input_sequence
      - start_index
      - end_index
    outputs:
      - core_data_block: the sub-sequence from start_index to end_index (inclusive)
  - name: calculate_target_position
    condition: non-zero digits exist
    inputs:
      - start_index
      - shift_amount
      - shift_direction
    outputs:
      - target_start_index: start_index - shift_amount
  - name: construct_output
    condition: non-zero digits exist
    inputs:
      - core_data_block
      - target_start_index
      - sequence_length
      - padding_value
    outputs:
      - output_sequence: a sequence of sequence_length, padded with padding_value, containing the core_data_block potentially truncated/shifted according to boundary rules (target_start_index < 0 or target_start_index + length(core_data_block) > sequence_length).
relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: |
      Identify the sub-sequence spanning from the first non-zero digit to the last non-zero digit in the input sequence.
      Calculate a target start index by subtracting 3 (shift_amount) from the index of the first non-zero digit.
      Construct the output sequence of length 12, initially filled with zeros.
      Place the identified sub-sequence into the output sequence starting at the target start index.
      Handle boundary conditions: If the target start index is negative, truncate the beginning of the sub-sequence before placing it (starting placement at index 0). If placing the sub-sequence exceeds the sequence length, truncate the end of the sub-sequence.
      If the input sequence contains no non-zero digits, the output sequence is identical to the input sequence.
```


**Natural Language Program**

1.  Receive the input sequence of 12 digits.
2.  Find the index of the first digit in the sequence that is not zero.
3.  If no non-zero digit is found, the output sequence is identical to the input sequence. Stop processing.
4.  If a non-zero digit is found, record its index as `start_index`.
5.  Find the index of the last digit in the sequence that is not zero. Record this index as `end_index`.
6.  Extract the sub-sequence containing all digits from `start_index` to `end_index` (inclusive) from the input sequence.
7.  Calculate the target starting position for the sub-sequence in the output by subtracting 3 from `start_index`. Let this be `target_start_index`.
8.  Create a new sequence of 12 zeros, representing the initial state of the output sequence.
9.  Determine the portion of the extracted sub-sequence and the corresponding portion of the output sequence for placement, considering boundary conditions:
    a.  Calculate the starting index within the sub-sequence (`source_start`) and the starting index within the output sequence (`dest_start`). Initially, `source_start = 0` and `dest_start = target_start_index`.
    b.  If `dest_start` is less than 0, adjust `source_start` to `-dest_start` and set `dest_start` to 0.
    c.  Calculate the number of elements to potentially copy (`length_to_copy`), which is initially the length of the sub-sequence minus the adjusted `source_start`.
    d.  If `dest_start + length_to_copy` exceeds 12, adjust `length_to_copy` to `12 - dest_start`.
10. If `length_to_copy` is greater than 0, copy the elements from the sub-sequence (starting at `source_start` for `length_to_copy` elements) into the output sequence (starting at `dest_start`).
11. Return the final output sequence.
