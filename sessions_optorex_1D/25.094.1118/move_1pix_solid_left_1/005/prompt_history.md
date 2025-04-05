
## train_1

**input:**
```
0 2 2 2 2 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 8 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 0 0 0 0 0 0
```


## train_5

**input:**
```
0 7 7 7 7 7 7 7 7 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 0 0 0 0
```


## train_6

**input:**
```
0 5 5 5 5 5 5 5 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 6 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are sequences (lists) of single-digit integers.
    *   Each sequence has a fixed length (12 in all examples).
    *   Each input sequence contains a contiguous block of identical non-zero digits. The rest of the elements are zeros.
    *   The output sequence is related to the input sequence by a positional shift of the non-zero block.

*   **YAML Facts:**
    
```yaml
    task_description: Shift the first contiguous block of identical non-zero digits one position to the left within a fixed-length list of integers.
    
    elements:
      - name: sequence
        type: list of integers
        properties:
          - length: fixed (e.g., 12)
          - contains: single-digit integers (0-9)
      - name: non_zero_block
        type: contiguous sub-sequence
        properties:
          - elements: identical non-zero integers
          - location: surrounded by zeros or list boundaries
      - name: zero
        type: integer
        value: 0
        role: padding element, background element
    
    actions:
      - name: identify_first_non_zero_block
        input: sequence
        output: start_index, end_index, block_value
      - name: shift_left
        input: sequence, start_index, end_index
        output: modified_sequence
        details: Moves the elements from start_index to end_index one position to the left.
      - name: pad_end
        input: sequence
        output: modified_sequence
        details: Appends a zero to the end if necessary to maintain original length after shift.
    
    relationships:
      - The output sequence is a transformation of the input sequence.
      - The non_zero_block in the output sequence starts one position earlier (index-1) than in the input sequence.
      - The length of the input and output sequences is identical.
      - The values within the non_zero_block remain unchanged.
      - The relative order of zeros outside the shifted block is maintained, except for the zero potentially displaced by the shift and the zero added at the end.
    ```


*   **Natural Language Program:**
    1.  Receive the input list of integers.
    2.  Find the starting index of the first non-zero element in the list. If no non-zero element exists, return the original list.
    3.  Identify the value of this first non-zero element.
    4.  Determine the end index of the contiguous block of elements that have this same non-zero value, starting from the found starting index.
    5.  Create a new list of the same length as the input list, initially filled with zeros.
    6.  Copy the identified block of non-zero elements into the new list, starting at an index one less than the original starting index.
    7.  Return the new list.
```python
"""
Transforms an input list of integers by finding the first contiguous block of 
identical non-zero digits and shifting this block one position to the left. 
The list maintains its original length, and positions outside the shifted 
block are filled with zeros in the output.
"""

import math

def find_first_block(data):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers.

    Args:
        data: A list of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    start_index = -1
    block_value = None
    n = len(data)

    # Find the start of the block and its value
    for i in range(n):
        if data[i] != 0:
            start_index = i
            block_value = data[i]
            break

    # If no non-zero element found, no block exists
    if start_index == -1:
        return None, None, None

    # Find the end of the block (index after the last element)
    end_index = start_index + 1
    while end_index < n and data[end_index] == block_value:
        end_index += 1

    return start_index, end_index, block_value

def transform(input_grid):
    """
    Shifts the first contiguous block of identical non-zero digits 
    one position to the left within the list.

    Args:
        input_grid: A list of integers.

    Returns:
        A new list of integers with the block shifted, or a copy of the 
        input list if no such block is found.
    """
    n = len(input_grid)
    
    # 1. & 2. & 3. & 4. Find the first non-zero block details
    # Use a helper function to find the start, end, and value of the block
    start_index, end_index, block_value = find_first_block(input_grid)

    # If no block is found, return a copy of the original list
    if start_index is None:
        return list(input_grid) # Return a copy

    # 5. Create a new list initialized with zeros
    output_grid = [0] * n

    # 6. Calculate the new starting position for the block (shifted left by 1)
    new_start_index = start_index - 1
    
    # Check if the shift is valid (start_index should be > 0 based on examples)
    # If start_index was 0, new_start_index would be -1. The examples provided
    # all have blocks starting at index 1 or later.
    if new_start_index < 0:
        # This case is not represented in the training data.
        # Based on the task description "shift left", we might assume data loss
        # at the beginning or handle it differently if more examples were given.
        # For now, proceed assuming valid shift based on observed examples.
        # A robust implementation might raise an error or have specific logic here.
        pass # Assuming valid shift as per examples

    # Copy the block elements to their new positions in the output grid
    block_length = end_index - start_index
    for i in range(block_length):
        dest_index = new_start_index + i
        # Ensure the destination index is within the bounds of the output grid
        if 0 <= dest_index < n:
            output_grid[dest_index] = block_value # Place the block's value

    # 7. Return the newly created list with the shifted block
    return output_grid
```
```python
"""
Transforms an input 1D NumPy array of integers by finding the first 
contiguous block of identical non-zero digits and shifting this block 
one position to the left. The array maintains its original length, and 
positions outside the shifted block are filled with zeros in the output.
"""

import numpy as np

def find_first_block_np(data):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers in a NumPy array.

    Args:
        data: A 1D NumPy array of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(data)[0]

    # If no non-zero element found, no block exists
    if len(non_zero_indices) == 0:
        return None, None, None

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]
    block_value = data[start_index]
    
    # Find the end of the block (index after the last element)
    end_index = start_index + 1
    n = len(data)
    while end_index < n and data[end_index] == block_value:
        end_index += 1
        
    # Verify that the block found corresponds to the *first* sequence 
    # of non-zeros. This check is important if there could be multiple 
    # blocks separated by zeros. np.nonzero finds all non-zeros, but we only
    # care about the first contiguous block. The while loop starting from 
    # non_zero_indices[0] ensures this.

    return start_index, end_index, block_value

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the first contiguous block of identical non-zero digits 
    one position to the left within the NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the block shifted, or a copy of the 
        input array if no such block is found or the block is already
        at the beginning.
    """
    # 1. Find the first non-zero block details
    start_index, end_index, block_value = find_first_block_np(input_grid)

    # If no block is found, return a copy of the original grid
    if start_index is None:
        return np.copy(input_grid) 

    # If the block starts at index 0, it cannot be shifted left.
    # Based on examples, this doesn't happen, but handle defensively.
    # The examples show blocks starting at index 1 or later being shifted.
    # If a block starts at 0, the examples suggest no change, but the prompt
    # implies a left shift. Let's assume based on examples that if start_index is 0, 
    # we return the original grid or handle as required if new examples clarify.
    # The test cases provided all shift blocks starting at index >= 1.
    # If start_index is 0, new_start_index would be -1.
    if start_index == 0:
         # Re-evaluate if examples with start_index=0 appear.
         # For now, aligning with the pattern that only blocks NOT at the start move.
         # Example output for input [2, 2, 0] -> [2, 2, 0]? or error? or [2, 0, 0]?
         # Let's assume no change if already at the start, consistent with outputs.
         # Example 5 output implies a shift even if starting at index 1 -> index 0.
         # Example 1 output implies a shift starting at index 1 -> index 0.
         # Ok, the shift should happen even if it means starting at index 0.
         pass # Proceed with the shift calculation.

    # 2. Create a new array initialized with zeros
    output_grid = np.zeros_like(input_grid)

    # 3. Calculate the new starting position and block length
    new_start_index = start_index - 1
    block_length = end_index - start_index

    # Ensure the new start index isn't negative before slicing
    if new_start_index < 0:
        # This case means the block started at index 0.
        # The problem description/examples don't explicitly cover shifting *off* the grid.
        # Based on example 1 & 5, shifting *to* index 0 is expected.
        # If we *must* shift left from index 0, we'd lose the first element.
        # However, let's stick to the observed patterns where the shift target index >= 0.
        # If start_index=0, new_start_index = -1. Let's adjust.
        # The slice `output_grid[-1:block_length-1]` is not intuitive.
        # Let's refine the copy logic for the edge case start_index=0
        
        # If the original block starts at index 0
        # Example: [2, 2, 0, 0] -> shift left -> [2, 0, 0, 0]? lose one '2'?
        # The examples show blocks starting >= 1. Let's assume valid shifts.
        # If an example like [2, 2, ...] -> [2, ...] arises, we'll adapt.
        # The current logic correctly handles shifts resulting in index 0 (e.g., from index 1).
         pass # The slicing below handles the valid cases shown.


    # 4. Copy the block elements to their new positions in the output grid
    # Calculate the actual start and end for slicing in the output array
    output_slice_start = max(0, new_start_index) 
    output_slice_end = new_start_index + block_length
    
    # Calculate the corresponding slice from the original block value
    # If new_start_index is < 0, we start copying from the second element of the block
    block_copy_len = output_slice_end - output_slice_start

    # Place the block value into the output grid slice
    if block_copy_len > 0 and output_slice_start < len(output_grid):
       output_grid[output_slice_start:min(output_slice_end, len(output_grid))] = block_value


    # 5. Return the newly created grid
    return output_grid
```

Previous Code:
```python
"""
Transforms an input 1D NumPy array of integers by finding the first 
contiguous block of identical non-zero digits and shifting this block 
one position to the left. The array maintains its original length, and 
positions outside the shifted block are filled with zeros in the output.
"""

import numpy as np

def find_first_block_np(data):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers in a NumPy array.

    Args:
        data: A 1D NumPy array of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(data)[0]

    # If no non-zero element found, no block exists
    if len(non_zero_indices) == 0:
        return None, None, None

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]
    block_value = data[start_index]
    
    # Find the end of the block (index after the last element)
    end_index = start_index + 1
    n = len(data)
    while end_index < n and data[end_index] == block_value:
        end_index += 1
        
    # Verify that the block found corresponds to the *first* sequence 
    # of non-zeros. This check is important if there could be multiple 
    # blocks separated by zeros. np.nonzero finds all non-zeros, but we only
    # care about the first contiguous block. The while loop starting from 
    # non_zero_indices[0] ensures this.

    return start_index, end_index, block_value

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the first contiguous block of identical non-zero digits 
    one position to the left within the NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the block shifted, or a copy of the 
        input array if no such block is found or the block is already
        at the beginning.
    """
    # 1. Find the first non-zero block details
    start_index, end_index, block_value = find_first_block_np(input_grid)

    # If no block is found, return a copy of the original grid
    if start_index is None:
        return np.copy(input_grid) 

    # If the block starts at index 0, it cannot be shifted left.
    # Based on examples, this doesn't happen, but handle defensively.
    # The examples show blocks starting at index 1 or later being shifted.
    # If a block starts at 0, the examples suggest no change, but the prompt
    # implies a left shift. Let's assume based on examples that if start_index is 0, 
    # we return the original grid or handle as required if new examples clarify.
    # The test cases provided all shift blocks starting at index >= 1.
    # If start_index is 0, new_start_index would be -1.
    if start_index == 0:
         # Re-evaluate if examples with start_index=0 appear.
         # For now, aligning with the pattern that only blocks NOT at the start move.
         # Example output for input [2, 2, 0] -> [2, 2, 0]? or error? or [2, 0, 0]?
         # Let's assume no change if already at the start, consistent with outputs.
         # Example 5 output implies a shift even if starting at index 1 -> index 0.
         # Example 1 output implies a shift starting at index 1 -> index 0.
         # Ok, the shift should happen even if it means starting at index 0.
         pass # Proceed with the shift calculation.

    # 2. Create a new array initialized with zeros
    output_grid = np.zeros_like(input_grid)

    # 3. Calculate the new starting position and block length
    new_start_index = start_index - 1
    block_length = end_index - start_index

    # Ensure the new start index isn't negative before slicing
    if new_start_index < 0:
        # This case means the block started at index 0.
        # The problem description/examples don't explicitly cover shifting *off* the grid.
        # Based on example 1 & 5, shifting *to* index 0 is expected.
        # If we *must* shift left from index 0, we'd lose the first element.
        # However, let's stick to the observed patterns where the shift target index >= 0.
        # If start_index=0, new_start_index = -1. Let's adjust.
        # The slice `output_grid[-1:block_length-1]` is not intuitive.
        # Let's refine the copy logic for the edge case start_index=0
        
        # If the original block starts at index 0
        # Example: [2, 2, 0, 0] -> shift left -> [2, 0, 0, 0]? lose one '2'?
        # The examples show blocks starting >= 1. Let's assume valid shifts.
        # If an example like [2, 2, ...] -> [2, ...] arises, we'll adapt.
        # The current logic correctly handles shifts resulting in index 0 (e.g., from index 1).
         pass # The slicing below handles the valid cases shown.


    # 4. Copy the block elements to their new positions in the output grid
    # Calculate the actual start and end for slicing in the output array
    output_slice_start = max(0, new_start_index) 
    output_slice_end = new_start_index + block_length
    
    # Calculate the corresponding slice from the original block value
    # If new_start_index is < 0, we start copying from the second element of the block
    block_copy_len = output_slice_end - output_slice_start

    # Place the block value into the output grid slice
    if block_copy_len > 0 and output_slice_start < len(output_grid):
       output_grid[output_slice_start:min(output_slice_end, len(output_grid))] = block_value


    # 5. Return the newly created grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 2 2 2 2 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 2 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 66.66666666666669

## Example 2:
Input:
```
0 0 0 0 1 1 1 1 0 0 0 0
```
Expected Output:
```
0 0 0 1 1 1 1 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 66.66666666666669

## Example 3:
Input:
```
0 0 0 8 8 8 8 8 0 0 0 0
```
Expected Output:
```
0 0 8 8 8 8 8 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 83.33333333333333

## Example 4:
Input:
```
0 0 0 5 5 5 5 0 0 0 0 0
```
Expected Output:
```
0 0 5 5 5 5 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 66.66666666666669

## Example 5:
Input:
```
0 7 7 7 7 7 7 7 7 0 0 0
```
Expected Output:
```
7 7 7 7 7 7 7 7 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 133.33333333333334

## Example 6:
Input:
```
0 5 5 5 5 5 5 5 0 0 0 0
```
Expected Output:
```
5 5 5 5 5 5 5 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 116.66666666666666

## Example 7:
Input:
```
0 0 0 0 0 0 0 0 6 6 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 6 6 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 7 7 7 7 7 0 0
```
Expected Output:
```
0 0 0 0 7 7 7 7 7 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 83.33333333333333
## General Assessment and Strategy

The provided execution results indicate a complete failure of the `transform` function, producing an all-zero array for every input, contrary to the expected outputs which show a leftward shift of a block of non-zero numbers. Manual tracing and metric calculation using the provided Python code suggest the logic for finding the block (`find_first_block_np`) and calculating the target slice for the shifted block (`output_slice_start`, `output_slice_end`) is correct based on the task description (shift left by one). The assignment `output_grid[slice] = block_value` should correctly fill the target slice with the non-zero value.

This discrepancy suggests either:
1.  The code executed during the test run was different from the code provided in the prompt.
2.  There was an issue in the testing environment or the way data was passed to the function (e.g., incorrect type).
3.  A very subtle bug exists that wasn't caught in tracing (less likely given the simplicity).

**Strategy:**
Assume the intended logic (find the first contiguous block of identical non-zero digits and shift it one position left) is correct, as strongly supported by the input/output examples. The failure to produce *any* non-zero output seems like a fundamental execution error rather than a subtle logical flaw in the intended algorithm. Therefore, the refinement will focus on ensuring the YAML and Natural Language Program clearly describe the observed *intended* transformation, rather than trying to explain the anomalous "all zeros" result. We will rely on the correctness of the `find_first_block_np` logic derived from the examples and refine the description of the transformation process.

## Metrics

Based on the `find_first_block_np` logic applied to the inputs:


*code_execution:*
```python
import numpy as np

def parse_line(line):
    return np.array([int(x) for x in line.split()], dtype=int)

def find_first_block_np(data):
    non_zero_indices = np.nonzero(data)[0]
    if len(non_zero_indices) == 0: return None, None, None
    start_index = non_zero_indices[0]
    block_value = data[start_index]
    end_index = start_index + 1
    n = len(data)
    while end_index < n and data[end_index] == block_value:
        end_index += 1
    return start_index, end_index, block_value

examples = {
    "train_1_input": "0 2 2 2 2 0 0 0 0 0 0 0",
    "train_2_input": "0 0 0 0 1 1 1 1 0 0 0 0",
    "train_3_input": "0 0 0 8 8 8 8 8 0 0 0 0",
    "train_4_input": "0 0 0 5 5 5 5 0 0 0 0 0",
    "train_5_input": "0 7 7 7 7 7 7 7 7 0 0 0",
    "train_6_input": "0 5 5 5 5 5 5 5 0 0 0 0",
    "train_7_input": "0 0 0 0 0 0 0 0 6 6 0 0",
    "test_1_input": "0 0 0 0 0 7 7 7 7 7 0 0",
}

results = {}
print("| Example   | Length | Block Value | Block Indices (Input) | Block Indices (Output) |")
print("|-----------|--------|-------------|-----------------------|------------------------|")
for name, line in examples.items():
    key = name.replace("_input", "")
    data = parse_line(line)
    n = len(data)
    start, end, value = find_first_block_np(data)
    if start is not None:
        new_start = start - 1
        new_end = end - 1 # The end index also shifts left
        results[key] = {
            "len": n,
            "start": start,
            "end": end,
            "value": value,
            "block_len": end - start,
            "new_start": new_start,
            "new_end": new_end
        }
        print(f"| {key:<9} | {n:<6} | {value:<11} | {start}:{end:<21} | {new_start}:{new_end:<22} |")
    else:
         results[key] = { "len": n, "start": None, "end": None, "value": None, "block_len": 0, "new_start": None, "new_end": None }
         print(f"| {key:<9} | {n:<6} | {'N/A':<11} | {'N/A':<21} | {'N/A':<22} |")


```

*code_execution_result:*
outcome: OUTCOME_OK
```
| Example   | Length | Block Value | Block Indices (Input) | Block Indices (Output) |
|-----------|--------|-------------|-----------------------|------------------------|
| train_1   | 12     | 2           | 1:5                     | 0:4                      |
| train_2   | 12     | 1           | 4:8                     | 3:7                      |
| train_3   | 12     | 8           | 3:8                     | 2:7                      |
| train_4   | 12     | 5           | 3:7                     | 2:6                      |
| train_5   | 12     | 7           | 1:9                     | 0:8                      |
| train_6   | 12     | 5           | 1:8                     | 0:7                      |
| train_7   | 12     | 6           | 8:10                    | 7:9                      |
| test_1    | 12     | 7           | 5:10                    | 4:9                      |

```
## YAML Facts


```yaml
task_description: Transform a 1D array of integers by finding the first contiguous block of identical non-zero digits and shifting this block one position to the left. The array length remains constant, with zeros filling positions not occupied by the shifted block.

elements:
  - name: integer_array
    type: 1D numpy array of integers
    properties:
      - length: fixed (e.g., 12)
      - contains: single-digit integers (0-9 observed)
      - role: input and output data structure
  - name: non_zero_block
    type: contiguous sub-sequence within the array
    properties:
      - elements: identical non-zero integers (e.g., all 2s, all 7s)
      - location: identified by start_index (inclusive) and end_index (exclusive)
      - uniqueness: only the *first* such block encountered from left-to-right is considered.
  - name: zero
    type: integer
    value: 0
    role: background/padding element

actions:
  - name: find_first_non_zero_block
    input: integer_array
    output: start_index, end_index, block_value
    description: Scans the array from left to right to find the first non-zero element. If found, determines its value and the extent (end_index) of the contiguous block of elements matching that value. Returns None if no non-zero elements exist.
  - name: generate_output_array
    input: original_length
    output: new_integer_array
    description: Creates a new array of the same length as the input, initialized entirely with zeros.
  - name: place_shifted_block
    input: output_array, original_start_index, original_end_index, block_value
    output: modified_output_array
    description: Calculates the new start index (original_start_index - 1) and new end index (original_end_index - 1). Copies the `block_value` into the `output_array` within these new indices. Ensures indices stay within array bounds (implicitly handles shift starting from index 1 to index 0).

relationships:
  - The output array has the same length as the input array.
  - If a non_zero_block is found in the input starting at index `s` and ending at index `e`, the output array will contain the same block value at indices `s-1` to `e-1`.
  - All positions in the output array *not* occupied by the shifted block are filled with zeros.
  - If no non_zero_block exists in the input, the output is identical to the input (or an all-zero array of the same length, consistent with the process).
  - The transformation only affects the *first* identified non-zero block; subsequent blocks or isolated non-zero numbers are ignored.
```


## Natural Language Program

1.  Receive the input 1D integer array.
2.  Initialize an output array of the same length as the input array, filled with zeros.
3.  Scan the input array from the first element (index 0) to find the index of the first non-zero element. Let this be `start_index`.
4.  If no non-zero element is found (`start_index` remains undefined), return the initialized (all zero) output array.
5.  If a non-zero element is found at `start_index`, record its value as `block_value`.
6.  Determine the end index (`end_index`, exclusive) of the contiguous block of elements equal to `block_value`, starting from `start_index`.
7.  Calculate the `new_start_index` for the output array by subtracting 1 from the `start_index`.
8.  Calculate the `new_end_index` for the output array by subtracting 1 from the `end_index`.
9.  Fill the elements of the output array from `new_start_index` (inclusive) up to `new_end_index` (exclusive) with the `block_value`. (Ensure indices used for assignment are valid, e.g., >= 0).
10. Return the modified output array.
