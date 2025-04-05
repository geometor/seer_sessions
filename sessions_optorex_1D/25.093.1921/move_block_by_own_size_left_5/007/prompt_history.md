
## train_1

**input:**
```
0 0 0 0 0 0 9 9 9 0 0 0
```


**output:**
```
0 0 0 9 9 9 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 6 6 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 1 1 1 1
```


**output:**
```
0 0 0 0 1 1 1 1 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 6 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 5 5 5 0 0
```


**output:**
```
0 0 0 0 5 5 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 7 7 7 0 0 0
```


**output:**
```
0 0 0 7 7 7 0 0 0 0 0 0
```

*   **Perception of task elements:**
    *   The input and output are lists of integers, always of length 12.
    *   Each list consists predominantly of zeros (0).
    *   Within each input list, there is a single, contiguous sequence (block) of identical non-zero digits.
    *   The transformation involves relocating this block of non-zero digits within the list.
    *   The non-zero digits themselves and the length of the block remain unchanged.
    *   The block appears to be shifted to the left. The amount of the shift seems related to the properties of the block itself.

*   **YAML facts:**
    
```yaml
    task_type: list_transformation
    list_length: 12
    background_element: 0
    objects:
      - type: contiguous_block
        properties:
          - value: non-zero_integer (constant within block)
          - length: variable (integer > 0)
          - start_index: variable (integer >= 0)
          - end_index: variable (integer < 12)
    action:
      - type: shift_left
        target: contiguous_block
        parameters:
          - shift_amount: equal_to_block_length
    relationship:
      - The distance the block is shifted left is numerically equal to the length of the block.
    output_structure:
      - The output list has the same length (12).
      - The shifted block retains its original values and length.
      - All other positions in the output list are filled with the background element (0).
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of identical non-zero digits within the input list.
    2.  Determine the starting index (`start_index`) and the length (`block_length`) of this block.
    3.  Calculate the new starting index for the block in the output list as `new_start_index = start_index - block_length`.
    4.  Create a new list of length 12, initially filled with zeros.
    5.  Copy the identified block of non-zero digits from the input list into the new list, starting at the `new_start_index`.
```python
import math
import numpy as np # Assuming numpy might be useful for grid operations, though not strictly needed here.

"""
Identifies a contiguous block of identical non-zero digits in the input list.
Shifts this block to the left by a number of positions equal to the length of the block.
Fills the remaining positions with zeros.
"""

def find_non_zero_block(input_list):
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block.
        - block_length (int): The length of the block.
        - block_value (int): The value of the elements in the block.
        Returns (-1, 0, 0) if no non-zero block is found.
    """
    start_index = -1
    block_length = 0
    block_value = 0

    for i, val in enumerate(input_list):
        if val != 0:
            # Found the start of a potential block
            if start_index == -1:
                start_index = i
                block_value = val
                block_length = 1
            # Continue the current block
            elif val == block_value:
                block_length += 1
            # Found a different non-zero value, meaning the block ended just before
            elif val != block_value:
                 break # Stop searching once the first block is fully identified
        elif start_index != -1:
            # Found a zero after the block started, so the block ends here
            break # Stop searching once the first block is fully identified

    # Handle case where block goes to the end of the list (loop finishes)
    if start_index != -1:
        return start_index, block_length, block_value
    else:
        # No non-zero block found
        return -1, 0, 0


def transform(input_grid: list[int]) -> list[int]:
    """
    Transforms the input list based on the described rule.

    Args:
        input_grid: A list of integers.

    Returns:
        A new list of integers with the non-zero block shifted.
    """
    # Find the non-zero block details
    start_index, block_length, block_value = find_non_zero_block(input_grid)

    # Initialize the output grid with zeros
    list_length = len(input_grid)
    output_grid = [0] * list_length

    # If no block was found, return the list of zeros (or original, depending on spec - returning zeros seems consistent)
    if start_index == -1:
        return output_grid

    # Calculate the new starting position for the block
    # The shift amount is equal to the block length
    new_start_index = start_index - block_length

    # Ensure the new start index is not out of bounds (although examples suggest it won't be negative)
    # new_start_index = max(0, new_start_index) # Let's stick strictly to the observed rule first

    # Place the block in the new position in the output grid
    # Ensure we don't write past the start or end of the list if the calculation results in out-of-bounds indices
    for i in range(block_length):
        target_index = new_start_index + i
        # Check bounds before writing (important if shift calculation could go out of bounds)
        if 0 <= target_index < list_length:
             output_grid[target_index] = block_value
        # If the target index is out of bounds, the element is effectively lost (or placed off-grid)
        # which is consistent with the output being filled with zeros otherwise.

    return output_grid

```
```python
import math
import numpy as np # Although not strictly needed by the logic, might be present in the execution environment

"""
Transforms the input list by identifying a contiguous block of identical non-zero digits 
and shifting this block to the left by a number of positions equal to its length. 
The remaining positions in the output list are filled with zeros.
"""

def find_non_zero_block(input_list: list[int]) -> tuple[int, int, int]:
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if no block found).
        - block_length (int): The length of the block (0 if no block found).
        - block_value (int): The value of the elements in the block (0 if no block found).
    """
    start_index = -1
    block_length = 0
    block_value = 0

    for i, val in enumerate(input_list):
        # Look for the start of a potential block (first non-zero)
        if val != 0 and start_index == -1:
            start_index = i
            block_value = val
            block_length = 1
        # If we are already in a block, check if the current element continues it
        elif start_index != -1:
            if val == block_value:
                block_length += 1
            # If the element is different (zero or another non-zero), the block ends
            else:
                break 
        # If we haven't started a block and the element is zero, continue
        # If we have finished a block (by encountering a different value), the break above handles it.
        
    # Handle case where block goes to the end of the list (loop finishes while block is active)
    if start_index != -1:
        return start_index, block_length, block_value
    else:
        # No non-zero block found
        return -1, 0, 0

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the described transformation rule to the input list.

    Args:
        input_grid: The input list of integers.

    Returns:
        A new list with the non-zero block shifted according to the rule.
    """
    list_length = len(input_grid)
    # 1. Initialize output_grid: Create a new list filled with zeros.
    output_grid = [0] * list_length

    # 2. Identify Block & 3. Record Properties: Find the non-zero block details.
    start_index, block_length, block_value = find_non_zero_block(input_grid)

    # Proceed only if a block was found. If not, the all-zero grid is returned.
    if start_index != -1:
        # 4. Calculate New Position: Determine the target start index.
        new_start_index = start_index - block_length

        # 5. Place Block: Copy the block to the new position in the output grid.
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure writing stays within list bounds [0, list_length - 1].
            if 0 <= target_index < list_length:
                output_grid[target_index] = block_value
            # Elements shifted outside bounds are implicitly handled as they are not written.

    # 6. Finalize: Return the resulting grid.
    return output_grid
```
```python
import math
import numpy as np # Import numpy as the environment might pass arrays

"""
Transforms an input list (or NumPy array) of integers by identifying the first 
contiguous block of identical non-zero digits. This block is then shifted to the 
left by a number of positions equal to its own length. The resulting list is 
filled with zeros except for the shifted block.
"""

def find_non_zero_block(input_list: list[int]) -> tuple[int, int, int]:
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if no block found).
        - block_length (int): The length of the block (0 if no block found).
        - block_value (int): The value of the elements in the block (0 if no block found).
    """
    start_index = -1
    block_length = 0
    block_value = 0

    # Iterate through the list to find the block
    for i, val in enumerate(input_list):
        # Look for the start of a potential block (first non-zero)
        if val != 0 and start_index == -1:
            start_index = i
            block_value = val
            block_length = 1
        # If we are already in a block, check if the current element continues it
        elif start_index != -1:
            if val == block_value:
                block_length += 1
            # If the element is different (zero or another non-zero), the block ends
            else:
                break # Found the end of the block, stop searching

    # Return details, handling the case where no block was found
    if start_index != -1:
        return start_index, block_length, block_value
    else:
        return -1, 0, 0

def transform(input_grid) -> list[int]:
    """
    Applies the block-shifting transformation to the input grid.

    Args:
        input_grid: A list or NumPy array of integers.

    Returns:
        A new list of integers with the non-zero block shifted.
    """
    # Ensure input is a standard Python list for consistent processing
    # This addresses the potential issue of receiving a NumPy array
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assuming it's already list-like (e.g., a list)
        input_list = list(input_grid) 

    list_length = len(input_list)
    
    # 1. Initialize output_grid: Create a new list filled with zeros.
    output_grid = [0] * list_length

    # 2. Identify Block & 3. Record Properties: Find the non-zero block details using the helper function.
    start_index, block_length, block_value = find_non_zero_block(input_list)

    # 4. Check if a block was found. If not, the all-zero grid is returned.
    if start_index != -1:
        # 5. Calculate New Position: Determine the target start index for the shifted block.
        new_start_index = start_index - block_length

        # 6. Place Block: Copy the block to the new position in the output grid.
        # Iterate through the length of the block to place each element.
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure the target index is within the valid bounds of the output list.
            if 0 <= target_index < list_length:
                output_grid[target_index] = block_value
            # Elements that would be shifted outside the list bounds are simply not placed.

    # 7. Finalize: Return the resulting grid.
    return output_grid
```

Previous Code:
```python
import math
import numpy as np # Import numpy as the environment might pass arrays

"""
Transforms an input list (or NumPy array) of integers by identifying the first 
contiguous block of identical non-zero digits. This block is then shifted to the 
left by a number of positions equal to its own length. The resulting list is 
filled with zeros except for the shifted block.
"""

def find_non_zero_block(input_list: list[int]) -> tuple[int, int, int]:
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if no block found).
        - block_length (int): The length of the block (0 if no block found).
        - block_value (int): The value of the elements in the block (0 if no block found).
    """
    start_index = -1
    block_length = 0
    block_value = 0

    # Iterate through the list to find the block
    for i, val in enumerate(input_list):
        # Look for the start of a potential block (first non-zero)
        if val != 0 and start_index == -1:
            start_index = i
            block_value = val
            block_length = 1
        # If we are already in a block, check if the current element continues it
        elif start_index != -1:
            if val == block_value:
                block_length += 1
            # If the element is different (zero or another non-zero), the block ends
            else:
                break # Found the end of the block, stop searching

    # Return details, handling the case where no block was found
    if start_index != -1:
        return start_index, block_length, block_value
    else:
        return -1, 0, 0

def transform(input_grid) -> list[int]:
    """
    Applies the block-shifting transformation to the input grid.

    Args:
        input_grid: A list or NumPy array of integers.

    Returns:
        A new list of integers with the non-zero block shifted.
    """
    # Ensure input is a standard Python list for consistent processing
    # This addresses the potential issue of receiving a NumPy array
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assuming it's already list-like (e.g., a list)
        input_list = list(input_grid) 

    list_length = len(input_list)
    
    # 1. Initialize output_grid: Create a new list filled with zeros.
    output_grid = [0] * list_length

    # 2. Identify Block & 3. Record Properties: Find the non-zero block details using the helper function.
    start_index, block_length, block_value = find_non_zero_block(input_list)

    # 4. Check if a block was found. If not, the all-zero grid is returned.
    if start_index != -1:
        # 5. Calculate New Position: Determine the target start index for the shifted block.
        new_start_index = start_index - block_length

        # 6. Place Block: Copy the block to the new position in the output grid.
        # Iterate through the length of the block to place each element.
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure the target index is within the valid bounds of the output list.
            if 0 <= target_index < list_length:
                output_grid[target_index] = block_value
            # Elements that would be shifted outside the list bounds are simply not placed.

    # 7. Finalize: Return the resulting grid.
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 9 9 9 0 0 0
```
Expected Output:
```
0 0 0 9 9 9 0 0 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 2:
Input:
```
0 0 0 6 6 0 0 0 0 0 0 0
```
Expected Output:
```
0 6 6 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 0 0 0 0 0 0 4 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 4 0 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 1 1 1 1
```
Expected Output:
```
0 0 0 0 1 1 1 1 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 5:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 6
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 6 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 6:
Input:
```
0 0 0 0 0 0 0 5 5 5 0 0
```
Expected Output:
```
0 0 0 0 5 5 5 0 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 7:
Input:
```
0 0 0 0 0 0 7 7 7 0 0 0
```
Expected Output:
```
0 0 0 7 7 7 0 0 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 5 5 0 0 0
```
Expected Output:
```
0 0 0 0 0 5 5 0 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None
*   **General Assessment:**
    *   The execution results show a consistent failure across all examples, where the transformed output is reported as `0` instead of the expected list of 12 integers.
    *   Comparing the expected outputs with the inputs confirms that the initially derived transformation rule (identify the contiguous block of identical non-zero digits, determine its start index `S` and length `L`, and shift it left to start at index `S - L`) holds true for all provided training examples.
    *   The failure is therefore not in the logical understanding of the transformation rule but likely lies in the implementation details within the `transform` function or its interaction with the execution/testing environment. Specifically, returning a single `0` suggests a potential type mismatch, incorrect handling of the input data format (e.g., expecting a list but receiving something else), or an issue in how the testing framework interprets the function's return value.
*   **Strategy:**
    1.  Verify the transformation logic's correctness against all examples using conceptual execution or calculation.
    2.  Gather metrics (block value, length, start index, new start index) for each example to confirm the pattern.
    3.  Assume the core logic (find block, calculate shift) is correct.
    4.  Refine the implementation focusing on robust input handling (e.g., ensuring the input is treated as a list of integers, regardless of whether it's passed as a list, numpy array, or potentially even a string needing parsing) and ensuring the output is explicitly a list of integers.
    5.  Re-state the YAML facts and Natural Language program, as the underlying transformation rule appears correctly identified.

*   **Metrics Gathering:**
    Executing the conceptual test and metrics gathering code:
    

*code_execution:*
```python
    import json

    def test_logic(input_str, output_str):
        try:
            input_list = [int(x) for x in input_str.split()]
            expected_output_list = [int(x) for x in output_str.split()]
        except ValueError:
            print(f"Error parsing input/output strings: '{input_str}', '{output_str}'")
            return False # Cannot parse, logic cannot be tested

        if not input_list: # Handle empty input if split results in empty list
             return not expected_output_list # True if both are empty

        list_length = len(input_list)
        output_grid = [0] * list_length

        start_index = -1
        block_length = 0
        block_value = 0
        # Find the block
        for i, val in enumerate(input_list):
            if val != 0 and start_index == -1: # Found start of block
                start_index = i
                block_value = val
                block_length = 1
            elif start_index != -1: # Already in a block
                if val == block_value: # Continue block
                    block_length += 1
                else: # End of block (different value or zero)
                    break
            # Else (val is 0, not in block): continue searching

        # Apply the shift if block found
        if start_index != -1:
            new_start_index = start_index - block_length
            for i in range(block_length):
                target_index = new_start_index + i
                # Place element if within bounds
                if 0 <= target_index < list_length:
                    output_grid[target_index] = block_value

        return output_grid == expected_output_list

    examples = [
        ("0 0 0 0 0 0 9 9 9 0 0 0", "0 0 0 9 9 9 0 0 0 0 0 0"),
        ("0 0 0 6 6 0 0 0 0 0 0 0", "0 6 6 0 0 0 0 0 0 0 0 0"),
        ("0 0 0 0 0 0 0 4 0 0 0 0", "0 0 0 0 0 0 4 0 0 0 0 0"),
        ("0 0 0 0 0 0 0 0 1 1 1 1", "0 0 0 0 1 1 1 1 0 0 0 0"),
        ("0 0 0 0 0 0 0 0 0 0 0 6", "0 0 0 0 0 0 0 0 0 0 6 0"),
        ("0 0 0 0 0 0 0 5 5 5 0 0", "0 0 0 0 5 5 5 0 0 0 0 0"),
        ("0 0 0 0 0 0 7 7 7 0 0 0", "0 0 0 7 7 7 0 0 0 0 0 0"),
    ]

    logic_results = [test_logic(inp, outp) for inp, outp in examples]
    print(f"Logic Correctness Check: {logic_results}")

    # Calculate metrics
    metrics = []
    for idx, (inp_str, outp_str) in enumerate(examples):
        try:
            input_list = [int(x) for x in inp_str.split()]
        except ValueError:
             metrics.append({
                 "example": idx + 1,
                 "input": inp_str,
                 "output": outp_str,
                 "error": "Cannot parse input"
             })
             continue

        if not input_list:
             metrics.append({
                 "example": idx + 1,
                 "input": inp_str,
                 "output": outp_str,
                 "error": "Empty input list after parsing"
             })
             continue

        start_index = -1
        block_length = 0
        block_value = 0
        for i, val in enumerate(input_list):
            if val != 0 and start_index == -1:
                start_index = i
                block_value = val
                block_length = 1
            elif start_index != -1:
                if val == block_value:
                    block_length += 1
                else:
                    break
        new_start_index = start_index - block_length if start_index != -1 else -1
        metrics.append({
            "example": idx + 1,
            "input": inp_str,
            "output": outp_str,
            "block_value": block_value,
            "block_length": block_length,
            "start_index": start_index,
            "new_start_index": new_start_index,
            "logic_correct": test_logic(inp_str, outp_str)
        })

    print("\nMetrics per Example:")
    print(json.dumps(metrics, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Logic Correctness Check: [True, True, True, True, True, True, True]

Metrics per Example:
[
  {
    "example": 1,
    "input": "0 0 0 0 0 0 9 9 9 0 0 0",
    "output": "0 0 0 9 9 9 0 0 0 0 0 0",
    "block_value": 9,
    "block_length": 3,
    "start_index": 6,
    "new_start_index": 3,
    "logic_correct": true
  },
  {
    "example": 2,
    "input": "0 0 0 6 6 0 0 0 0 0 0 0",
    "output": "0 6 6 0 0 0 0 0 0 0 0 0",
    "block_value": 6,
    "block_length": 2,
    "start_index": 3,
    "new_start_index": 1,
    "logic_correct": true
  },
  {
    "example": 3,
    "input": "0 0 0 0 0 0 0 4 0 0 0 0",
    "output": "0 0 0 0 0 0 4 0 0 0 0 0",
    "block_value": 4,
    "block_length": 1,
    "start_index": 7,
    "new_start_index": 6,
    "logic_correct": true
  },
  {
    "example": 4,
    "input": "0 0 0 0 0 0 0 0 1 1 1 1",
    "output": "0 0 0 0 1 1 1 1 0 0 0 0",
    "block_value": 1,
    "block_length": 4,
    "start_index": 8,
    "new_start_index": 4,
    "logic_correct": true
  },
  {
    "example": 5,
    "input": "0 0 0 0 0 0 0 0 0 0 0 6",
    "output": "0 0 0 0 0 0 0 0 0 0 6 0",
    "block_value": 6,
    "block_length": 1,
    "start_index": 11,
    "new_start_index": 10,
    "logic_correct": true
  },
  {
    "example": 6,
    "input": "0 0 0 0 0 0 0 5 5 5 0 0",
    "output": "0 0 0 0 5 5 5 0 0 0 0 0",
    "block_value": 5,
    "block_length": 3,
    "start_index": 7,
    "new_start_index": 4,
    "logic_correct": true
  },
  {
    "example": 7,
    "input": "0 0 0 0 0 0 7 7 7 0 0 0",
    "output": "0 0 0 7 7 7 0 0 0 0 0 0",
    "block_value": 7,
    "block_length": 3,
    "start_index": 6,
    "new_start_index": 3,
    "logic_correct": true
  }
]

```
*   **YAML Facts:**
    
```yaml
    task_type: list_transformation
    input_type: list_of_integers # Can be represented as string initially
    output_type: list_of_integers
    list_length: 12
    background_element: 0
    objects:
      - type: contiguous_block
        description: The first sequence of identical, non-zero integers found when scanning the list from left to right.
        properties:
          - value: non_zero_integer (constant within the block)
          - length: integer > 0 (number of elements in the block)
          - start_index: integer >= 0 (index of the first element of the block in the input list)
    action:
      - type: shift_left
        target: contiguous_block
        parameter:
          shift_amount: The amount to shift the block left is numerically equal to the block's length.
    output_composition:
      - Create a new list of the same length (12), initialized with the background element (0).
      - Place the identified 'contiguous_block' into this new list.
      - The starting index of the block in the new list is calculated as `new_start_index = original_start_index - block_length`.
      - Elements of the block that would be shifted to an index less than 0 are discarded.
      - All positions in the new list not occupied by the shifted block remain as the background element (0).
    invariants:
      - List length remains 12.
      - The value of the non-zero digits within the block remains unchanged.
      - The length of the block remains unchanged.
      - Only one such non-zero block exists in the input based on examples.
    constraints:
       - Input list always contains exactly one contiguous block of identical non-zero digits.
       - The rest of the elements are zeros.
    ```


*   **Natural Language Program:**
    1.  Receive the input, which represents a list of 12 integers. Ensure it is parsed into a list format if necessary (e.g., if provided as a space-separated string).
    2.  Initialize an output list of 12 zeros.
    3.  Iterate through the input list from left to right to find the first non-zero integer. This marks the potential start of the contiguous block.
    4.  Once the first non-zero integer is found at `start_index` with value `block_value`:
        *   Record `start_index` and `block_value`.
        *   Continue iterating from `start_index + 1` to count how many consecutive elements also have the value `block_value`. This count determines the `block_length`. Stop counting when an element differs from `block_value` or the end of the list is reached.
    5.  If no non-zero block is found (i.e., the input list contains only zeros), return the initialized output list of 12 zeros.
    6.  If a block is found:
        *   Calculate the target starting index for the block in the output list: `new_start_index = start_index - block_length`.
        *   Iterate from `i = 0` up to `block_length - 1`:
            *   Calculate the target index in the output list: `target_index = new_start_index + i`.
            *   If `target_index` is within the valid range of indices for the output list (i.e., `0 <= target_index < 12`), set the element at `output_list[target_index]` to `block_value`.
    7.  Return the final output list.
