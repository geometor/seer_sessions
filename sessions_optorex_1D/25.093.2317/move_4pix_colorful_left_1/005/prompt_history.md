
## train_1

**input:**
```
0 0 0 0 0 0 0 0 8 3 5 0
```


**output:**
```
0 0 0 0 8 3 5 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 9 2 7 2 3 3 4 0
```


**output:**
```
9 2 7 2 3 3 4 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 7 9 1 6 7 3 4
```


**output:**
```
0 7 9 1 6 7 3 4 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 7 6 0 0 0 0 0 0
```


**output:**
```
7 6 0 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 8 8 5 8 1 2
```


**output:**
```
0 0 8 8 5 8 1 2 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 3 3 0 0 0 0
```


**output:**
```
0 0 3 3 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 9 2 0 0 0 0 0
```


**output:**
```
0 9 2 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are strings representing sequences of single digits separated by spaces. They can be interpreted as lists or arrays of integers.
2.  **Sequence Length:** The length of the sequence remains constant between the input and the output in all examples.
3.  **Core Content:** The non-zero digits and the zeros situated between the first and last non-zero digits seem to form a "core segment" or "payload". This core segment appears unchanged in the output.
4.  **Positional Shift:** The primary transformation is a positional shift of this core segment within the sequence. The core segment consistently moves towards the beginning of the sequence (left shift).
5.  **Shift Magnitude:** The amount of the left shift appears deterministic. By comparing the number of leading zeros in the input versus the output, we can deduce the rule.
    *   train_1: 8 leading zeros in -> 4 leading zeros out (Shift of 4 positions left)
    *   train_2: 4 leading zeros in -> 0 leading zeros out (Shift of 4 positions left)
    *   train_3: 5 leading zeros in -> 1 leading zero out (Shift of 4 positions left)
    *   train_4: 4 leading zeros in -> 0 leading zeros out (Shift of 4 positions left)
    *   train_5: 6 leading zeros in -> 2 leading zeros out (Shift of 4 positions left)
    *   train_6: 6 leading zeros in -> 2 leading zeros out (Shift of 4 positions left)
    *   train_7: 5 leading zeros in -> 1 leading zero out (Shift of 4 positions left)
    The number of leading zeros in the output is consistently 4 less than the number of leading zeros in the input, with a minimum of 0 leading zeros.

**YAML Fact Document:**


```yaml
task_description: Rearrange a sequence of digits by shifting the core non-zero segment to the left.
elements:
  - object: sequence
    properties:
      - type: list of integers (derived from space-separated string)
      - length: constant between input and output
      - items: single digits (0-9)
  - object: core_segment
    description: The subsequence starting from the first non-zero digit and ending at the last non-zero digit, inclusive.
    properties:
      - content: digits (non-zero and potentially included zeros)
      - location_input: defined by the index of the first non-zero digit (number of leading zeros)
      - location_output: derived from the input location
relationships:
  - type: transformation
    action: identify_core_segment
    inputs: [input_sequence]
    outputs: [core_segment, first_nonzero_index, last_nonzero_index]
  - type: transformation
    action: calculate_output_position
    inputs: [first_nonzero_index]
    outputs: [output_leading_zeros]
    rule: output_leading_zeros = max(0, first_nonzero_index - 4)
  - type: transformation
    action: reconstruct_output
    inputs: [output_leading_zeros, core_segment, input_sequence_length]
    outputs: [output_sequence]
    rule: Concatenate 'output_leading_zeros' count of zeros, the 'core_segment', and trailing zeros to match 'input_sequence_length'.
special_cases:
  - condition: Input sequence contains only zeros.
    result: Output sequence is identical to the input sequence. (The core segment is empty, leading zeros calculation still applies but doesn't change the sequence visually).
```


**Natural Language Program:**

1.  Parse the input string into a list of integers. Record the total length of this list.
2.  Locate the index of the first non-zero integer in the list (`first_nz_idx`). If no non-zero integer exists, return the original input string.
3.  Locate the index of the last non-zero integer in the list (`last_nz_idx`).
4.  Extract the sub-list from `first_nz_idx` to `last_nz_idx` (inclusive). This is the "core segment".
5.  Calculate the number of leading zeros for the output list: `num_output_zeros = max(0, first_nz_idx - 4)`.
6.  Construct the output list:
    a.  Start with `num_output_zeros` zeros.
    b.  Append the extracted "core segment" to the list.
    c.  Append additional zeros until the total length of the output list matches the recorded length of the input list.
7.  Convert the output list back into a space-separated string of digits.
```python
import math

"""
Parses an input string of space-separated digits into a list of integers.
Identifies the 'core segment' (from the first non-zero digit to the last non-zero digit).
Calculates the target starting position for this core segment by subtracting 4 from its original starting position (number of leading zeros), ensuring the result is not negative.
Reconstructs the output list by placing the core segment at the calculated starting position, padding with leading and trailing zeros as needed to maintain the original sequence length.
Finally, converts the resulting list back into a space-separated string.
"""

def _find_first_nonzero_index(int_list):
    """Finds the index of the first non-zero element."""
    for i, num in enumerate(int_list):
        if num != 0:
            return i
    return -1 # Indicate no non-zero element found

def _find_last_nonzero_index(int_list):
    """Finds the index of the last non-zero element."""
    last_idx = -1
    for i, num in enumerate(int_list):
        if num != 0:
            last_idx = i
    return last_idx

def transform(input_str: str) -> str:
    """
    Shifts the core non-zero segment of a sequence of digits 4 positions to the left.

    Args:
        input_str: A string of space-separated single digits.

    Returns:
        A string representing the transformed sequence of digits, also space-separated.
    """

    # 1. Parse the input string into a list of integers and record length
    input_list = [int(x) for x in input_str.split()]
    original_length = len(input_list)

    # 2. Locate the index of the first non-zero integer
    first_nz_idx = _find_first_nonzero_index(input_list)

    # Handle case where all digits are zero
    if first_nz_idx == -1:
        return input_str # Return original string if no non-zeros

    # 3. Locate the index of the last non-zero integer
    last_nz_idx = _find_last_nonzero_index(input_list)

    # 4. Extract the "core segment"
    # Ensure indices are valid before slicing
    if first_nz_idx <= last_nz_idx:
        core_segment = input_list[first_nz_idx : last_nz_idx + 1]
    else:
        # This case should ideally not happen if first_nz_idx != -1,
        # but handle defensively
        core_segment = []


    # 5. Calculate the number of leading zeros for the output list
    # The number of input leading zeros is simply first_nz_idx
    num_output_zeros = max(0, first_nz_idx - 4)

    # 6. Construct the output list
    output_list = []
    # a. Start with calculated leading zeros
    output_list.extend([0] * num_output_zeros)
    # b. Append the core segment
    output_list.extend(core_segment)
    # c. Append trailing zeros to match original length
    num_trailing_zeros = original_length - len(output_list)
    output_list.extend([0] * num_trailing_zeros)

    # 7. Convert the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
```
```python
import math
import numpy as np

"""
Rearranges a sequence of digits (represented as a list or NumPy array of integers) 
by identifying the 'core segment' (from the first non-zero digit to the 
last non-zero digit, inclusive). This core segment is then shifted 4 positions 
to the left within the sequence. If shifting 4 positions left would move the 
start of the segment past the beginning of the sequence (index 0), it is placed 
at index 0 instead. The remaining positions are filled with zeros (leading and 
trailing) to maintain the original sequence length. If the input sequence 
contains only zeros, it is returned unchanged.
"""

def _find_first_nonzero_index(int_list):
    """Finds the index of the first non-zero element in a list."""
    for i, num in enumerate(int_list):
        if num != 0:
            return i
    return -1 # Indicate no non-zero element found

def _find_last_nonzero_index(int_list):
    """Finds the index of the last non-zero element in a list."""
    last_idx = -1
    # Iterate backwards for potential minor efficiency, but forward is fine too.
    for i in range(len(int_list) - 1, -1, -1):
        if int_list[i] != 0:
            return i
    return -1 # Should not happen if first_nonzero found one, but defensive.


def transform(input_grid) -> list:
    """
    Shifts the core non-zero segment of a sequence of digits 4 positions to the left.

    Args:
        input_grid: A list or NumPy array of single-digit integers.

    Returns:
        A list representing the transformed sequence of digits.
    """

    # Ensure input is a standard Python list for consistent operations
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assume it's already list-like (e.g., a standard list)
        input_list = list(input_grid) 
        
    original_length = len(input_list)

    # Find the start index of the core segment (first non-zero)
    first_nz_idx = _find_first_nonzero_index(input_list)

    # Handle the case where the input is all zeros
    if first_nz_idx == -1:
        # Return a copy to avoid modifying the original if it was mutable
        return list(input_list) 

    # Find the end index of the core segment (last non-zero)
    last_nz_idx = _find_last_nonzero_index(input_list)

    # Extract the core segment using list slicing
    # Note: Slicing input_list[first_nz_idx : last_nz_idx + 1] is correct
    core_segment = input_list[first_nz_idx : last_nz_idx + 1]
    core_length = len(core_segment)

    # Calculate the number of leading zeros for the output list
    # This is the target start index for the core segment
    num_output_zeros = max(0, first_nz_idx - 4)

    # Construct the output list
    # Start with the calculated number of leading zeros
    output_list = [0] * num_output_zeros
    
    # Append the core segment
    output_list.extend(core_segment)
    
    # Calculate the number of trailing zeros needed to maintain original length
    current_length = len(output_list)
    num_trailing_zeros = original_length - current_length
    
    # Append the trailing zeros
    output_list.extend([0] * num_trailing_zeros)

    # The problem description implies the output should match the input type.
    # Since the error mentioned numpy.ndarray, let's try returning that.
    # If the input was originally a list, this still works.
    # return np.array(output_list, dtype=type(input_grid[0]) if original_length > 0 else int) 
    # Let's return a list first as per the function signature `-> list`
    return output_list
```

Previous Code:
```python
import math
import numpy as np

"""
Rearranges a sequence of digits (represented as a list or NumPy array of integers) 
by identifying the 'core segment' (from the first non-zero digit to the 
last non-zero digit, inclusive). This core segment is then shifted 4 positions 
to the left within the sequence. If shifting 4 positions left would move the 
start of the segment past the beginning of the sequence (index 0), it is placed 
at index 0 instead. The remaining positions are filled with zeros (leading and 
trailing) to maintain the original sequence length. If the input sequence 
contains only zeros, it is returned unchanged.
"""

def _find_first_nonzero_index(int_list):
    """Finds the index of the first non-zero element in a list."""
    for i, num in enumerate(int_list):
        if num != 0:
            return i
    return -1 # Indicate no non-zero element found

def _find_last_nonzero_index(int_list):
    """Finds the index of the last non-zero element in a list."""
    last_idx = -1
    # Iterate backwards for potential minor efficiency, but forward is fine too.
    for i in range(len(int_list) - 1, -1, -1):
        if int_list[i] != 0:
            return i
    return -1 # Should not happen if first_nonzero found one, but defensive.


def transform(input_grid) -> list:
    """
    Shifts the core non-zero segment of a sequence of digits 4 positions to the left.

    Args:
        input_grid: A list or NumPy array of single-digit integers.

    Returns:
        A list representing the transformed sequence of digits.
    """

    # Ensure input is a standard Python list for consistent operations
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assume it's already list-like (e.g., a standard list)
        input_list = list(input_grid) 
        
    original_length = len(input_list)

    # Find the start index of the core segment (first non-zero)
    first_nz_idx = _find_first_nonzero_index(input_list)

    # Handle the case where the input is all zeros
    if first_nz_idx == -1:
        # Return a copy to avoid modifying the original if it was mutable
        return list(input_list) 

    # Find the end index of the core segment (last non-zero)
    last_nz_idx = _find_last_nonzero_index(input_list)

    # Extract the core segment using list slicing
    # Note: Slicing input_list[first_nz_idx : last_nz_idx + 1] is correct
    core_segment = input_list[first_nz_idx : last_nz_idx + 1]
    core_length = len(core_segment)

    # Calculate the number of leading zeros for the output list
    # This is the target start index for the core segment
    num_output_zeros = max(0, first_nz_idx - 4)

    # Construct the output list
    # Start with the calculated number of leading zeros
    output_list = [0] * num_output_zeros
    
    # Append the core segment
    output_list.extend(core_segment)
    
    # Calculate the number of trailing zeros needed to maintain original length
    current_length = len(output_list)
    num_trailing_zeros = original_length - current_length
    
    # Append the trailing zeros
    output_list.extend([0] * num_trailing_zeros)

    # The problem description implies the output should match the input type.
    # Since the error mentioned numpy.ndarray, let's try returning that.
    # If the input was originally a list, this still works.
    # return np.array(output_list, dtype=type(input_grid[0]) if original_length > 0 else int) 
    # Let's return a list first as per the function signature `-> list`
    return output_list
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 8 3 5 0
```
Expected Output:
```
0 0 0 0 8 3 5 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 8 3 5 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0

## Example 2:
Input:
```
0 0 0 0 9 2 7 2 3 3 4 0
```
Expected Output:
```
9 2 7 2 3 3 4 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 9 2 7 2 3 3 4 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 91.66666666666667

## Example 3:
Input:
```
0 0 0 0 0 7 9 1 6 7 3 4
```
Expected Output:
```
0 7 9 1 6 7 3 4 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 7 9 1 6 7 3 4
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 83.33333333333334

## Example 4:
Input:
```
0 0 0 0 7 6 0 0 0 0 0 0
```
Expected Output:
```
7 6 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 7 6 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 33.33333333333334

## Example 5:
Input:
```
0 0 0 0 0 0 8 8 5 8 1 2
```
Expected Output:
```
0 0 8 8 5 8 1 2 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 8 8 5 8 1 2
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 83.33333333333334

## Example 6:
Input:
```
0 0 0 0 0 0 3 3 0 0 0 0
```
Expected Output:
```
0 0 3 3 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 3 3 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 33.33333333333334

## Example 7:
Input:
```
0 0 0 0 0 9 2 0 0 0 0 0
```
Expected Output:
```
0 9 2 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 9 2 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 33.33333333333334

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 1 8 4 7 6 1 0
```
Expected Output:
```
0 1 8 4 7 6 1 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 1 8 4 7 6 1 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 83.33333333333334
**General Assessment and Strategy**

The execution results indicate that the provided Python code consistently failed to transform the input sequences, instead returning the original input. However, the initial analysis and the natural language program derived from the examples accurately describe the observed transformation: identifying a "core segment" of non-zero numbers (and the zeros between them) and shifting this segment 4 positions to the left, bounded by the start of the sequence.

The discrepancy suggests either:
1.  An error in the execution environment or test harness used to generate the results.
2.  A subtle flaw in the provided Python code that prevents the transformation logic from executing correctly (though a manual walkthrough suggests the code *should* work as intended).
3.  A misunderstanding of the input/output format expected by the `transform` function in the testing context (e.g., receiving a string instead of a list).

**Strategy:**

1.  Re-verify the core transformation rule using metrics derived directly from the input/output pairs.
2.  Assume the initial analysis of the transformation rule (identify core, shift left by 4, pad with zeros) is correct, as it fits all examples perfectly.
3.  Refine the YAML documentation and the natural language program to be crystal clear about this rule.
4.  The provided code's failure is noted, but since the logic seems to match the required transformation, the focus will be on precisely describing the *intended* transformation based on the examples, rather than debugging the specific erroneous execution.

**Metrics Gathering**


*code_execution:*
```python
import numpy as np

def analyze_transformation(input_str, output_str):
    input_list = [int(x) for x in input_str.split()]
    output_list = [int(x) for x in output_str.split()]
    
    original_length = len(input_list)
    
    # Find first and last non-zero indices in input
    first_nz_idx_in = -1
    last_nz_idx_in = -1
    for i, num in enumerate(input_list):
        if num != 0:
            if first_nz_idx_in == -1:
                first_nz_idx_in = i
            last_nz_idx_in = i
            
    # Find first and last non-zero indices in output
    first_nz_idx_out = -1
    last_nz_idx_out = -1
    for i, num in enumerate(output_list):
        if num != 0:
            if first_nz_idx_out == -1:
                first_nz_idx_out = i
            last_nz_idx_out = i

    if first_nz_idx_in == -1: # All zeros
        core_segment_in = []
        shift_amount = 0
        core_segment_out = []
    else:
        core_segment_in = input_list[first_nz_idx_in : last_nz_idx_in + 1]
        core_segment_out = output_list[first_nz_idx_out : last_nz_idx_out + 1]
        shift_amount = first_nz_idx_in - first_nz_idx_out
        
    return {
        "length": original_length,
        "input_leading_zeros": first_nz_idx_in if first_nz_idx_in != -1 else original_length,
        "output_leading_zeros": first_nz_idx_out if first_nz_idx_out != -1 else original_length,
        "core_segment_in": core_segment_in,
        "core_segment_out": core_segment_out,
        "core_segment_match": core_segment_in == core_segment_out,
        "calculated_shift": shift_amount,
        "expected_shift_rule": max(0, first_nz_idx_in - 4) == first_nz_idx_out if first_nz_idx_in != -1 else True
    }

examples = [
    ("0 0 0 0 0 0 0 0 8 3 5 0", "0 0 0 0 8 3 5 0 0 0 0 0"),
    ("0 0 0 0 9 2 7 2 3 3 4 0", "9 2 7 2 3 3 4 0 0 0 0 0"),
    ("0 0 0 0 0 7 9 1 6 7 3 4", "0 7 9 1 6 7 3 4 0 0 0 0"),
    ("0 0 0 0 7 6 0 0 0 0 0 0", "7 6 0 0 0 0 0 0 0 0 0 0"),
    ("0 0 0 0 0 0 8 8 5 8 1 2", "0 0 8 8 5 8 1 2 0 0 0 0"),
    ("0 0 0 0 0 0 3 3 0 0 0 0", "0 0 3 3 0 0 0 0 0 0 0 0"),
    ("0 0 0 0 0 9 2 0 0 0 0 0", "0 9 2 0 0 0 0 0 0 0 0 0"),
    ("0 0 0 0 0 1 8 4 7 6 1 0", "0 1 8 4 7 6 1 0 0 0 0 0"), # Test example 1
]

analysis_results = []
for i, (in_str, out_str) in enumerate(examples):
    analysis = analyze_transformation(in_str, out_str)
    print(f"Example {i+1}: {analysis}")
    analysis_results.append(analysis)

# Verify consistency
all_lengths_same = all(r['length'] == analysis_results[0]['length'] for r in analysis_results)
all_segments_match = all(r['core_segment_match'] for r in analysis_results)
all_shifts_rule_match = all(r['expected_shift_rule'] for r in analysis_results)

print(f"\nAll lengths consistent: {all_lengths_same}")
print(f"All core segments match between input/output: {all_segments_match}")
print(f"All shifts follow 'max(0, input_leading_zeros - 4)' rule: {all_shifts_rule_match}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1: {'length': 12, 'input_leading_zeros': 8, 'output_leading_zeros': 4, 'core_segment_in': [8, 3, 5], 'core_segment_out': [8, 3, 5], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 2: {'length': 12, 'input_leading_zeros': 4, 'output_leading_zeros': 0, 'core_segment_in': [9, 2, 7, 2, 3, 3, 4], 'core_segment_out': [9, 2, 7, 2, 3, 3, 4], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 3: {'length': 12, 'input_leading_zeros': 5, 'output_leading_zeros': 1, 'core_segment_in': [7, 9, 1, 6, 7, 3, 4], 'core_segment_out': [7, 9, 1, 6, 7, 3, 4], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 4: {'length': 12, 'input_leading_zeros': 4, 'output_leading_zeros': 0, 'core_segment_in': [7, 6], 'core_segment_out': [7, 6], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 5: {'length': 12, 'input_leading_zeros': 6, 'output_leading_zeros': 2, 'core_segment_in': [8, 8, 5, 8, 1, 2], 'core_segment_out': [8, 8, 5, 8, 1, 2], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 6: {'length': 12, 'input_leading_zeros': 6, 'output_leading_zeros': 2, 'core_segment_in': [3, 3], 'core_segment_out': [3, 3], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 7: {'length': 12, 'input_leading_zeros': 5, 'output_leading_zeros': 1, 'core_segment_in': [9, 2], 'core_segment_out': [9, 2], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}
Example 8: {'length': 12, 'input_leading_zeros': 5, 'output_leading_zeros': 1, 'core_segment_in': [1, 8, 4, 7, 6, 1], 'core_segment_out': [1, 8, 4, 7, 6, 1], 'core_segment_match': True, 'calculated_shift': 4, 'expected_shift_rule': True}

All lengths consistent: True
All core segments match between input/output: True
All shifts follow 'max(0, input_leading_zeros - 4)' rule: True

```
**YAML Fact Document**


```yaml
task_description: Rearrange a sequence of digits by shifting the core non-zero segment exactly 4 positions to the left, padding with zeros.
constants:
  - name: SHIFT_AMOUNT
    value: 4
elements:
  - object: sequence
    properties:
      - type: list of single-digit integers
      - length: constant between input and output (verified as 12 in examples)
      - items: integers 0-9
  - object: core_segment
    description: The contiguous subsequence starting from the first non-zero digit and ending at the last non-zero digit, inclusive. Contains original values and order.
    properties:
      - content: original digits (non-zero and included zeros)
      - input_start_index: index of the first non-zero digit in the input sequence (equivalent to the number of leading zeros).
      - input_end_index: index of the last non-zero digit in the input sequence.
      - output_start_index: target index for the start of the core segment in the output sequence.
relationships:
  - type: identification
    action: find_core_segment
    inputs: [input_sequence]
    outputs: [core_segment, input_start_index, input_end_index]
    condition: Returns empty segment and indices (-1 or length) if input contains only zeros.
  - type: calculation
    action: determine_output_start_index
    inputs: [input_start_index]
    outputs: [output_start_index]
    rule: output_start_index = max(0, input_start_index - SHIFT_AMOUNT) # SHIFT_AMOUNT is 4
  - type: construction
    action: build_output_sequence
    inputs: [output_start_index, core_segment, sequence_length]
    outputs: [output_sequence]
    rule: Create a new sequence of 'sequence_length' filled with zeros. Place the 'core_segment' into this sequence starting at 'output_start_index'.
special_cases:
  - condition: Input sequence contains only zeros.
    result: Output sequence is identical to the input sequence. (Core segment is empty, placement logic results in no change).
validation_notes:
  - The core segment's content and internal order remain unchanged.
  - The shift amount is consistently 4 positions to the left.
  - The target start index is capped at 0 (no negative indices).
  - Total sequence length is preserved by padding with zeros before and after the shifted core segment.
  - Execution results provided previously contradict this analysis, showing no transformation occurred. The logic described here is based purely on the input/output examples.
```


**Natural Language Program**

1.  Receive the input sequence of digits (represented as a list of integers). Let the total number of elements be `L`.
2.  Identify the "core segment":
    a.  Find the index of the first non-zero digit (`first_nz`). If no non-zero digits exist, return the original input sequence.
    b.  Find the index of the last non-zero digit (`last_nz`).
    c.  Extract the sub-sequence from `first_nz` to `last_nz` (inclusive). This is the `core_segment`.
3.  Determine the target starting position for the `core_segment` in the output sequence:
    a.  Calculate the desired start index: `target_start = first_nz - 4`.
    b.  Adjust the start index to ensure it's not negative: `output_start = max(0, target_start)`.
4.  Construct the output sequence:
    a.  Create a new list of length `L` initialized entirely with zeros.
    b.  Copy the elements of the `core_segment` into the new list, starting at index `output_start`. Ensure the copied elements do not exceed the bounds of the list (though based on the shift rule and segment extraction, this shouldn't occur if `L` is constant).
5.  Return the constructed output sequence.
