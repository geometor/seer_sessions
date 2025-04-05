
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
```python
import numpy as np
from typing import List, Union

"""
Transforms a sequence of 12 digits based on the following rule:
Identify the sub-sequence spanning from the first non-zero digit to the last non-zero digit in the input sequence.
Calculate a target start index by subtracting 3 (shift_amount) from the index of the first non-zero digit.
Construct the output sequence of length 12, initially filled with zeros.
Place the identified sub-sequence into the output sequence starting at the target start index.
Handle boundary conditions: If the target start index is negative, truncate the beginning of the sub-sequence before placing it (starting placement at index 0). If placing the sub-sequence exceeds the sequence length, truncate the end of the sub-sequence.
If the input sequence contains no non-zero digits, the output sequence is identical to the input sequence.
"""

def _find_first_nonzero_index(data_list: List[int]) -> int:
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(data_list):
    if val != 0:
      return i
  return -1 # Return -1 if no non-zero element is found

def _find_last_nonzero_index(data_list: List[int]) -> int:
  """Finds the index of the last non-zero element."""
  # Iterate backwards for efficiency is possible, but forwards works too
  for i in range(len(data_list) - 1, -1, -1):
      if data_list[i] != 0:
          return i
  return -1 # Should not happen if _find_first_nonzero_index found something, but good practice

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list representing the transformed sequence of 12 integers.
    """
    # Define constants
    sequence_length = 12
    shift_amount = 3
    padding_value = 0

    # Ensure input is a list (though type hint suggests it is)
    input_list = list(input_sequence)
    
    # --- Step 1 & 2: Find the index of the first non-zero digit ---
    start_index = _find_first_nonzero_index(input_list)

    # --- Step 3: Handle the case where the input is all zeros ---
    if start_index == -1:
        # If no non-zero elements, return the original sequence
        return input_list

    # --- Step 4 & 5: Find the last non-zero index ---
    # Only needed if a non-zero digit was found
    end_index = _find_last_nonzero_index(input_list)

    # --- Step 6: Extract the sub-sequence ---
    sub_sequence = input_list[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # --- Step 7: Calculate the target starting index for the output ---
    target_start_index = start_index - shift_amount

    # --- Step 8: Create a new output list initialized with zeros ---
    output_list = [padding_value] * sequence_length

    # --- Step 9 & 10: Determine placement boundaries and copy sub-sequence ---
    # Determine the slice of the sub_sequence to copy
    source_start = 0
    source_end = sub_len
    
    # Determine the slice of the output_list to place into
    dest_start = target_start_index
    dest_end = target_start_index + sub_len

    # Adjust source slice if destination starts before index 0
    if dest_start < 0:
        source_start = -dest_start # Skip initial elements of sub_sequence
        dest_start = 0          # Start placing at index 0 in output

    # Adjust source/destination slices if destination ends after the last index
    if dest_end > sequence_length:
        # Calculate how much it overflows
        overflow = dest_end - sequence_length
        # Reduce the portion copied from the source
        source_end = source_end - overflow 
        # Ensure the destination ends exactly at the sequence length
        dest_end = sequence_length                     

    # Only perform the assignment if there's a valid range to copy/paste
    # Check that start indices are less than end indices for both source and destination
    if dest_start < dest_end and source_start < source_end:
        output_list[dest_start:dest_end] = sub_sequence[source_start:source_end]

    # --- Step 11: Return the final output sequence ---
    return output_list
```

Previous Code:
```python
import numpy as np
from typing import List, Union

"""
Transforms a sequence of 12 digits based on the following rule:
Identify the sub-sequence spanning from the first non-zero digit to the last non-zero digit in the input sequence.
Calculate a target start index by subtracting 3 (shift_amount) from the index of the first non-zero digit.
Construct the output sequence of length 12, initially filled with zeros.
Place the identified sub-sequence into the output sequence starting at the target start index.
Handle boundary conditions: If the target start index is negative, truncate the beginning of the sub-sequence before placing it (starting placement at index 0). If placing the sub-sequence exceeds the sequence length, truncate the end of the sub-sequence.
If the input sequence contains no non-zero digits, the output sequence is identical to the input sequence.
"""

def _find_first_nonzero_index(data_list: List[int]) -> int:
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(data_list):
    if val != 0:
      return i
  return -1 # Return -1 if no non-zero element is found

def _find_last_nonzero_index(data_list: List[int]) -> int:
  """Finds the index of the last non-zero element."""
  # Iterate backwards for efficiency is possible, but forwards works too
  for i in range(len(data_list) - 1, -1, -1):
      if data_list[i] != 0:
          return i
  return -1 # Should not happen if _find_first_nonzero_index found something, but good practice

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list representing the transformed sequence of 12 integers.
    """
    # Define constants
    sequence_length = 12
    shift_amount = 3
    padding_value = 0

    # Ensure input is a list (though type hint suggests it is)
    input_list = list(input_sequence)
    
    # --- Step 1 & 2: Find the index of the first non-zero digit ---
    start_index = _find_first_nonzero_index(input_list)

    # --- Step 3: Handle the case where the input is all zeros ---
    if start_index == -1:
        # If no non-zero elements, return the original sequence
        return input_list

    # --- Step 4 & 5: Find the last non-zero index ---
    # Only needed if a non-zero digit was found
    end_index = _find_last_nonzero_index(input_list)

    # --- Step 6: Extract the sub-sequence ---
    sub_sequence = input_list[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # --- Step 7: Calculate the target starting index for the output ---
    target_start_index = start_index - shift_amount

    # --- Step 8: Create a new output list initialized with zeros ---
    output_list = [padding_value] * sequence_length

    # --- Step 9 & 10: Determine placement boundaries and copy sub-sequence ---
    # Determine the slice of the sub_sequence to copy
    source_start = 0
    source_end = sub_len
    
    # Determine the slice of the output_list to place into
    dest_start = target_start_index
    dest_end = target_start_index + sub_len

    # Adjust source slice if destination starts before index 0
    if dest_start < 0:
        source_start = -dest_start # Skip initial elements of sub_sequence
        dest_start = 0          # Start placing at index 0 in output

    # Adjust source/destination slices if destination ends after the last index
    if dest_end > sequence_length:
        # Calculate how much it overflows
        overflow = dest_end - sequence_length
        # Reduce the portion copied from the source
        source_end = source_end - overflow 
        # Ensure the destination ends exactly at the sequence length
        dest_end = sequence_length                     

    # Only perform the assignment if there's a valid range to copy/paste
    # Check that start indices are less than end indices for both source and destination
    if dest_start < dest_end and source_start < source_end:
        output_list[dest_start:dest_end] = sub_sequence[source_start:source_end]

    # --- Step 11: Return the final output sequence ---
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
**General Assessment:**

The error message `The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()` consistently appears across all examples. This strongly indicates that the `transform` function, specifically the helper functions `_find_first_nonzero_index` and `_find_last_nonzero_index`, are receiving NumPy arrays as input, not standard Python lists as type-hinted. The comparison `val != 0` within these functions fails because comparing a NumPy array element (which might itself be considered array-like in some contexts or the comparison results in an array) in a context expecting a single boolean (like an `if` statement) causes this ambiguity error.

The core transformation logic identified previously (finding the block between the first and last non-zero elements, shifting it left by 3 positions, and padding with zeros) appears correct, as confirmed by manual checks and simulation. The failure is purely in the implementation's handling of the input data type.

**Strategy for Resolution:**

1.  Modify the helper functions (`_find_first_nonzero_index`, `_find_last_nonzero_index`) to explicitly handle potential NumPy array inputs. This could involve converting the input to a list at the beginning or using NumPy-native functions like `np.nonzero()` to find the indices directly, which is generally more efficient and idiomatic for NumPy arrays.
2.  Refine the main `transform` function to use these updated helper functions or integrate the NumPy-based index finding.
3.  Ensure the slicing and placement logic correctly handles boundary conditions (negative start index, exceeding sequence length) which seemed correctly implemented in the last version but should be double-checked, especially if using NumPy indexing/slicing.

**Metrics Gathering:**

The code execution below uses NumPy to verify the core logic (finding indices, extracting sub-sequence, calculating output position) for each training example.



*code_execution:*
```python
import numpy as np

def analyze_example(input_str):
    input_arr = np.array([int(x) for x in input_str.split()])
    n = len(input_arr)
    non_zero_indices = np.nonzero(input_arr)[0]

    if len(non_zero_indices) == 0:
        start_index = -1
        end_index = -1
        sub_sequence = np.array([], dtype=int)
        output_start_index = -1
    else:
        start_index = non_zero_indices[0]
        end_index = non_zero_indices[-1]
        sub_sequence = input_arr[start_index : end_index + 1]
        output_start_index = start_index - 3 # Shift left by 3

    # Calculate expected output based on logic
    output_arr = np.zeros(n, dtype=int)
    if start_index != -1:
        sub_len = len(sub_sequence)
        dest_start = max(0, output_start_index)
        dest_end = min(n, output_start_index + sub_len)
        source_start = max(0, -output_start_index)
        source_end = source_start + (dest_end - dest_start)

        if dest_start < dest_end: # Check if there is anything to copy/place
             output_arr[dest_start:dest_end] = sub_sequence[source_start:source_end]

    return {
        "input": input_arr.tolist(),
        "first_nz_idx": int(start_index) if start_index != -1 else None,
        "last_nz_idx": int(end_index) if end_index != -1 else None,
        "sub_sequence": sub_sequence.tolist(),
        "sub_sequence_len": len(sub_sequence),
        "calculated_output_start_idx": int(output_start_index) if start_index != -1 else None,
        "calculated_output": output_arr.tolist()
    }

train_inputs = [
    "0 0 0 0 0 0 3 9 1 2 4 6",
    "0 0 0 0 5 8 1 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 6 1 0 0",
    "0 0 0 0 0 0 0 4 6 3 2 5",
    "0 0 0 0 0 0 0 0 0 2 5 2",
    "0 0 0 5 2 8 5 8 8 8 0 0",
    "0 0 0 0 0 0 0 1 1 6 9 0",
]

train_outputs = [
    "0 0 0 3 9 1 2 4 6 0 0 0",
    "0 5 8 1 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 6 1 0 0 0 0 0",
    "0 0 0 0 4 6 3 2 5 0 0 0",
    "0 0 0 0 0 0 2 5 2 0 0 0",
    "5 2 8 5 8 8 8 0 0 0 0 0",
    "0 0 0 0 1 1 6 9 0 0 0 0",
]

results = []
for i, input_str in enumerate(train_inputs):
    analysis = analyze_example(input_str)
    analysis["expected_output"] = [int(x) for x in train_outputs[i].split()]
    analysis["match"] = analysis["calculated_output"] == analysis["expected_output"]
    results.append(analysis)
    print(f"--- Example {i+1} ---")
    print(f"Input: {analysis['input']}")
    print(f"First NZ Idx: {analysis['first_nz_idx']}, Last NZ Idx: {analysis['last_nz_idx']}")
    print(f"Sub-sequence: {analysis['sub_sequence']} (len={analysis['sub_sequence_len']})")
    print(f"Target Start Idx: {analysis['calculated_output_start_idx']}")
    print(f"Calculated Output: {analysis['calculated_output']}")
    print(f"Expected Output:   {analysis['expected_output']}")
    print(f"Match: {analysis['match']}")
    print("-"*(len(f"--- Example {i+1} ---")))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 ---
Input: [0, 0, 0, 0, 0, 0, 3, 9, 1, 2, 4, 6]
First NZ Idx: 6, Last NZ Idx: 11
Sub-sequence: [3, 9, 1, 2, 4, 6] (len=6)
Target Start Idx: 3
Calculated Output: [0, 0, 0, 3, 9, 1, 2, 4, 6, 0, 0, 0]
Expected Output:   [0, 0, 0, 3, 9, 1, 2, 4, 6, 0, 0, 0]
Match: True
-----------------
--- Example 2 ---
Input: [0, 0, 0, 0, 5, 8, 1, 0, 0, 0, 0, 0]
First NZ Idx: 4, Last NZ Idx: 6
Sub-sequence: [5, 8, 1] (len=3)
Target Start Idx: 1
Calculated Output: [0, 5, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
Expected Output:   [0, 5, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
Match: True
-----------------
--- Example 3 ---
Input: [0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0]
First NZ Idx: 8, Last NZ Idx: 9
Sub-sequence: [6, 1] (len=2)
Target Start Idx: 5
Calculated Output: [0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 0]
Expected Output:   [0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 0]
Match: True
-----------------
--- Example 4 ---
Input: [0, 0, 0, 0, 0, 0, 0, 4, 6, 3, 2, 5]
First NZ Idx: 7, Last NZ Idx: 11
Sub-sequence: [4, 6, 3, 2, 5] (len=5)
Target Start Idx: 4
Calculated Output: [0, 0, 0, 0, 4, 6, 3, 2, 5, 0, 0, 0]
Expected Output:   [0, 0, 0, 0, 4, 6, 3, 2, 5, 0, 0, 0]
Match: True
-----------------
--- Example 5 ---
Input: [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2]
First NZ Idx: 9, Last NZ Idx: 11
Sub-sequence: [2, 5, 2] (len=3)
Target Start Idx: 6
Calculated Output: [0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0]
Expected Output:   [0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0]
Match: True
-----------------
--- Example 6 ---
Input: [0, 0, 0, 5, 2, 8, 5, 8, 8, 8, 0, 0]
First NZ Idx: 3, Last NZ Idx: 9
Sub-sequence: [5, 2, 8, 5, 8, 8, 8] (len=7)
Target Start Idx: 0
Calculated Output: [5, 2, 8, 5, 8, 8, 8, 0, 0, 0, 0, 0]
Expected Output:   [5, 2, 8, 5, 8, 8, 8, 0, 0, 0, 0, 0]
Match: True
-----------------
--- Example 7 ---
Input: [0, 0, 0, 0, 0, 0, 0, 1, 1, 6, 9, 0]
First NZ Idx: 7, Last NZ Idx: 10
Sub-sequence: [1, 1, 6, 9] (len=4)
Target Start Idx: 4
Calculated Output: [0, 0, 0, 0, 1, 1, 6, 9, 0, 0, 0, 0]
Expected Output:   [0, 0, 0, 0, 1, 1, 6, 9, 0, 0, 0, 0]
Match: True
-----------------

```
**YAML Fact Document:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list or numpy array of integers
      - length: 12
      - contains: digits 0-9
    roles:
      - input_sequence
      - output_sequence
  - object: sub_sequence
    properties:
      - type: list or numpy array of integers
      - derived_from: input_sequence
      - boundaries: defined by the first and last non-zero digits (inclusive)
      - content: contiguous sequence of digits between the first and last non-zero elements of the input
    role:
      - core_data_block
  - object: zero_digit
    properties:
      - value: 0
    role:
      - padding_element
      - internal_element (within sub_sequence, e.g., [1, 0, 2])
  - object: non_zero_digit
    properties:
      - value: range 1-9
    role:
      - boundary_marker (first and last non-zero define the sub_sequence)
      - data_element (part of the sub_sequence)
  - object: index
    properties:
      - type: integer
    roles:
      - start_index (of first non-zero in input)
      - end_index (of last non-zero in input)
      - output_start_index (calculated target placement index in output)
constants:
  - name: sequence_length
    value: 12
  - name: shift_amount
    value: 3
    direction: left
  - name: padding_value
    value: 0
actions:
  - name: find_non_zero_indices
    inputs:
      - input_sequence
    outputs:
      - list_of_indices: indices where elements are not zero
    notes: Handle empty list if all zeros.
  - name: determine_sub_sequence_boundaries
    inputs:
      - list_of_indices
    outputs:
      - start_index: first index in list_of_indices (or indicator of none)
      - end_index: last index in list_of_indices (or indicator of none)
  - name: extract_sub_sequence
    inputs:
      - input_sequence
      - start_index
      - end_index
    outputs:
      - core_data_block: the sub-sequence from start_index to end_index (inclusive)
    condition: Only if start_index and end_index are valid.
  - name: calculate_output_position
    inputs:
      - start_index
    constants:
      - shift_amount
    outputs:
      - output_start_index: start_index - shift_amount
    condition: Only if start_index is valid.
  - name: construct_output_sequence
    inputs:
      - core_data_block
      - output_start_index
    constants:
      - sequence_length
      - padding_value
    outputs:
      - output_sequence
    process:
      - Initialize sequence of sequence_length with padding_value.
      - Calculate effective placement range in output (adjusting for boundaries 0 and sequence_length-1).
      - Calculate corresponding source range from core_data_block (adjusting for boundaries).
      - Place the adjusted portion of core_data_block into the adjusted output range.
    condition: Only if core_data_block exists. If input was all zeros, output is all zeros.
relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: >
      Identify the sub-sequence spanning from the first non-zero digit to the last non-zero digit.
      Shift this sub-sequence 3 positions to the left.
      Place the (potentially truncated due to boundary conditions) sub-sequence into an output sequence of length 12, padded with zeros.
      If the input has no non-zero digits, the output is identical to the input.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits (which may be represented as a list or a NumPy array).
2.  Identify the indices of all non-zero elements in the input sequence.
3.  If there are no non-zero elements, the output sequence is identical to the input sequence (12 zeros). Proceed to step 9.
4.  If non-zero elements exist, determine the index of the first non-zero element (`start_index`) and the index of the last non-zero element (`end_index`).
5.  Extract the contiguous sub-sequence from the input sequence starting at `start_index` and ending at `end_index` (inclusive).
6.  Calculate the target starting index (`output_start_index`) for the sub-sequence in the output by subtracting 3 from `start_index`.
7.  Create a new output sequence of length 12, initialized entirely with zeros.
8.  Place the extracted sub-sequence into the output sequence starting at the `output_start_index`.
    *   If `output_start_index` is less than 0, begin placing the sub-sequence at index 0 of the output sequence, omitting the initial elements of the sub-sequence that correspond to the negative indices.
    *   If placing the sub-sequence extends beyond index 11 of the output sequence, truncate the end of the sub-sequence so that it fits within the 12-element length.
9.  Return the final output sequence.
