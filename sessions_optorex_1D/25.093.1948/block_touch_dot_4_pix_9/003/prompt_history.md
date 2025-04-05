
## train_1

**input:**
```
2 0 0 0 1 1 0 0 0 0 0 0
```


**output:**
```
2 1 1 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 5 5 5 2
```


**output:**
```
0 0 0 0 0 0 0 0 5 5 5 2
```


## train_3

**input:**
```
0 2 8 8 8 0 0 0 0 0 0 0
```


**output:**
```
0 2 8 8 8 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 2 0 0 0 5 5 5 5 5
```


**output:**
```
0 0 0 2 5 5 5 5 5 0 0 0
```


## train_5

**input:**
```
9 9 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 9 2 0 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
6 0 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 2 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 4 4 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 4 2 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of 12 integers.
    *   The integers involved seem to primarily be 0, 2, and other non-zero digits (1, 4, 5, 6, 8, 9 in the examples).
    *   The transformation involves rearranging elements within the sequence based on specific patterns involving the numbers 0 and 2.
    *   The number 0 acts as empty space or a placeholder that can be swapped or filled.
    *   The number 2 appears to act as a special boundary or condition marker.
    *   Other non-zero numbers (not 2) seem to be movable elements or blocks of elements.
    *   The core transformation appears to be either a local swap of a non-zero number (not 2) with an adjacent 0 when followed by a 2, or a leftward shift of a block of non-zero numbers (not 2) over adjacent zeros when preceded by a 2.
    *   If neither of these specific patterns is present, the sequence remains unchanged.

*   **Facts:**
    
```yaml
    Task: Rearrange elements in a sequence based on local patterns involving 0 and 2.

    Objects:
      - Sequence: A list of 12 integers.
      - Element: An integer within the sequence.
      - Number_Zero: The integer 0, acting as space.
      - Number_Two: The integer 2, acting as a boundary/condition.
      - Non_Zero_Element: Any integer X != 0 and X != 2.
      - Non_Zero_Block: A contiguous sub-sequence Y containing only Non_Zero_Elements.

    Properties:
      - Position: The index of an element in the sequence.
      - Value: The integer value of an element.
      - Adjacency: Elements immediately next to each other.
      - Precedence: An element or block coming before another in the sequence.

    Relationships/Patterns:
      - Pattern_Swap: A Non_Zero_Element X followed immediately by 0, followed immediately by 2 (X, 0, 2).
      - Pattern_Shift: A 2 followed immediately by one or more 0s, followed immediately by a Non_Zero_Element or a Non_Zero_Block Y (2, 0..., 0, Y).

    Actions:
      - Scan: Iterate through the sequence to find patterns.
      - Identify: Recognize specific patterns (Pattern_Swap, Pattern_Shift).
      - Swap: Exchange the positions of two adjacent elements (X and 0 in Pattern_Swap).
      - Move_Block: Relocate a Non_Zero_Block Y to a new position (immediately after 2 in Pattern_Shift).
      - Fill_Zeros: Place zeros in the positions previously occupied by the moved block.
      - Halt: Stop processing after the first applicable transformation.
      - No_Change: Output the sequence unmodified if no patterns are found.
    ```


*   **Natural Language Program:**
    1.  Examine the input sequence from left to right.
    2.  Search for the first occurrence of the pattern: a non-zero integer `X` (where `X` is not 2) immediately followed by a 0, which is immediately followed by a 2 (i.e., the sub-sequence `X, 0, 2`).
    3.  If this pattern (`X, 0, 2`) is found, modify the sequence by swapping the positions of `X` and 0 to create the sub-sequence `0, X, 2`. Leave the rest of the sequence unchanged relative to this triplet. Stop processing and output the modified sequence.
    4.  If the pattern `X, 0, 2` is *not* found anywhere in the sequence, then search for the first occurrence of the pattern: the integer 2 followed by one or more consecutive 0s, followed immediately by a non-zero integer or a contiguous block `Y` of non-zero integers (where none of the integers in `Y` are 2).
    5.  If this pattern (`2, 0..., 0, Y`) is found, modify the sequence by moving the entire block `Y` to the position immediately following the 2. Fill the original positions of the zeros (that were between 2 and `Y`) and the original positions of block `Y` with zeros, placing them after the moved block `Y`. Stop processing and output the modified sequence.
    6.  If neither the `X, 0, 2` pattern nor the `2, 0..., 0, Y` pattern is found in the sequence, output the original input sequence without any modifications.
```python
import math # Not used in this specific logic, but common practice

def parse_input(input_str):
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(grid):
    """Formats the list of integers back into a space-separated string."""
    return ' '.join(map(str, grid))

def transform(input_str):
    """
    Transforms the input sequence based on two primary patterns involving 0 and 2:
    1. If a pattern `X, 0, 2` (where X is non-zero and not 2) is found,
       swap X and 0 to `0, X, 2` and return. This action happens only for the
       first occurrence found scanning left-to-right.
    2. If Pattern 1 is not found, search for the first pattern `2, 0..., 0, Y`
       (where there's at least one 0, and Y is a non-empty block of non-zero,
       non-2 digits immediately following the zeros). Move block Y immediately
       after the 2, followed by the zeros that were originally between 2 and Y.
       Return the result. This action happens only for the first valid occurrence found.
    3. If neither pattern is found, return the original sequence.
    """
    grid = parse_input(input_str)
    n = len(grid)
    # Initialize output_grid as a copy of the input
    output_grid = list(grid) 

    # --- Check for Pattern 1: X, 0, 2 ---
    pattern1_found = False
    # Iterate up to n-3 because we need to check i, i+1, and i+2
    for i in range(n - 2):
        x = output_grid[i]
        zero = output_grid[i+1]
        two = output_grid[i+2]
        
        # Condition: X is non-zero and not 2, followed by 0, followed by 2
        if x != 0 and x != 2 and zero == 0 and two == 2:
            # Perform the swap: X and 0
            output_grid[i], output_grid[i+1] = output_grid[i+1], output_grid[i]
            pattern1_found = True
            # Stop processing after the first pattern match
            break 
            
    # If Pattern 1 was found and applied, return the result immediately
    if pattern1_found:
        return format_output(output_grid)

    # --- Check for Pattern 2: 2, 0..., 0, Y ---
    # This section only runs if Pattern 1 was NOT found
    pattern2_found = False
    # Iterate through the grid to find the first '2' that initiates the pattern
    for i in range(n):
        # Is the current element 2?
        if output_grid[i] == 2:
            idx_2 = i
            
            # Check if there are elements after the '2' to form the rest of the pattern
            if idx_2 + 1 < n:
                
                # --- Find the block of zeros immediately following the '2' ---
                idx_first_zero = idx_2 + 1
                idx_first_non_zero_after_zeros = -1
                num_zeros = 0
                # Scan from after '2' to find contiguous zeros
                for j in range(idx_first_zero, n):
                    if output_grid[j] == 0:
                        num_zeros += 1
                    else:
                        # Found the first non-zero element after the zero block
                        idx_first_non_zero_after_zeros = j
                        break
                
                # --- Check if the zero block is valid (at least one zero) ---
                # Also need a non-zero element following the zeros to form block Y
                if num_zeros > 0 and idx_first_non_zero_after_zeros != -1:
                    
                    # --- Find the block Y (non-zero, non-2 elements) ---
                    idx_block_start = idx_first_non_zero_after_zeros
                    idx_block_end = idx_block_start # Initialize end index (exclusive)
                    block_y = []
                    contains_2_in_block = False
                    
                    # Scan from the start of the potential block Y
                    for k in range(idx_block_start, n):
                        val = output_grid[k]
                        # Block continues if element is non-zero and not 2
                        if val != 0 and val != 2:
                            block_y.append(val)
                            idx_block_end = k + 1 # Update end index
                        else:
                            # Block ends if 0 or 2 is encountered
                            if val == 2:
                                # Mark if the block is invalid because it contains a 2
                                contains_2_in_block = True 
                            break # Stop scanning for this block

                    # --- Check if a valid block Y was found ---
                    # Block Y must be non-empty and must not contain any 2s
                    if len(block_y) > 0 and not contains_2_in_block:
                        len_y = len(block_y)
                        
                        # --- Perform the transformation ---
                        # Construct the new sequence segments
                        prefix = output_grid[:idx_2 + 1]          # Elements up to and including '2'
                        moved_part = block_y + ([0] * num_zeros) # The moved block Y followed by the zeros
                        suffix = output_grid[idx_block_end:]      # Elements after the original block Y
                        
                        # Combine segments to form the new grid
                        new_grid_list = prefix + moved_part + suffix
                        
                        # Basic sanity check for length preservation
                        if len(new_grid_list) == n:
                           output_grid = new_grid_list # Update the grid with the transformation
                           pattern2_found = True
                           # Stop searching for patterns after the first successful transformation
                           break 
                        # else: # If length changed, there's a logic error (should not happen here)
                           # print("Error: Length mismatch during Pattern 2 transformation") 
                           # pass

            # If Pattern 2 was successfully applied for this '2', stop the outer loop
            if pattern2_found:
                 break

    # Return the final state of the grid, formatted as a string
    # This will be the result of Pattern 2 if applied, or the original grid if no patterns matched
    return format_output(output_grid)

```

Previous Code:
```python
import math # Not used in this specific logic, but common practice

def parse_input(input_str):
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(grid):
    """Formats the list of integers back into a space-separated string."""
    return ' '.join(map(str, grid))

def transform(input_str):
    """
    Transforms the input sequence based on two primary patterns involving 0 and 2:
    1. If a pattern `X, 0, 2` (where X is non-zero and not 2) is found,
       swap X and 0 to `0, X, 2` and return. This action happens only for the
       first occurrence found scanning left-to-right.
    2. If Pattern 1 is not found, search for the first pattern `2, 0..., 0, Y`
       (where there's at least one 0, and Y is a non-empty block of non-zero,
       non-2 digits immediately following the zeros). Move block Y immediately
       after the 2, followed by the zeros that were originally between 2 and Y.
       Return the result. This action happens only for the first valid occurrence found.
    3. If neither pattern is found, return the original sequence.
    """
    grid = parse_input(input_str)
    n = len(grid)
    # Initialize output_grid as a copy of the input
    output_grid = list(grid) 

    # --- Check for Pattern 1: X, 0, 2 ---
    pattern1_found = False
    # Iterate up to n-3 because we need to check i, i+1, and i+2
    for i in range(n - 2):
        x = output_grid[i]
        zero = output_grid[i+1]
        two = output_grid[i+2]
        
        # Condition: X is non-zero and not 2, followed by 0, followed by 2
        if x != 0 and x != 2 and zero == 0 and two == 2:
            # Perform the swap: X and 0
            output_grid[i], output_grid[i+1] = output_grid[i+1], output_grid[i]
            pattern1_found = True
            # Stop processing after the first pattern match
            break 
            
    # If Pattern 1 was found and applied, return the result immediately
    if pattern1_found:
        return format_output(output_grid)

    # --- Check for Pattern 2: 2, 0..., 0, Y ---
    # This section only runs if Pattern 1 was NOT found
    pattern2_found = False
    # Iterate through the grid to find the first '2' that initiates the pattern
    for i in range(n):
        # Is the current element 2?
        if output_grid[i] == 2:
            idx_2 = i
            
            # Check if there are elements after the '2' to form the rest of the pattern
            if idx_2 + 1 < n:
                
                # --- Find the block of zeros immediately following the '2' ---
                idx_first_zero = idx_2 + 1
                idx_first_non_zero_after_zeros = -1
                num_zeros = 0
                # Scan from after '2' to find contiguous zeros
                for j in range(idx_first_zero, n):
                    if output_grid[j] == 0:
                        num_zeros += 1
                    else:
                        # Found the first non-zero element after the zero block
                        idx_first_non_zero_after_zeros = j
                        break
                
                # --- Check if the zero block is valid (at least one zero) ---
                # Also need a non-zero element following the zeros to form block Y
                if num_zeros > 0 and idx_first_non_zero_after_zeros != -1:
                    
                    # --- Find the block Y (non-zero, non-2 elements) ---
                    idx_block_start = idx_first_non_zero_after_zeros
                    idx_block_end = idx_block_start # Initialize end index (exclusive)
                    block_y = []
                    contains_2_in_block = False
                    
                    # Scan from the start of the potential block Y
                    for k in range(idx_block_start, n):
                        val = output_grid[k]
                        # Block continues if element is non-zero and not 2
                        if val != 0 and val != 2:
                            block_y.append(val)
                            idx_block_end = k + 1 # Update end index
                        else:
                            # Block ends if 0 or 2 is encountered
                            if val == 2:
                                # Mark if the block is invalid because it contains a 2
                                contains_2_in_block = True 
                            break # Stop scanning for this block

                    # --- Check if a valid block Y was found ---
                    # Block Y must be non-empty and must not contain any 2s
                    if len(block_y) > 0 and not contains_2_in_block:
                        len_y = len(block_y)
                        
                        # --- Perform the transformation ---
                        # Construct the new sequence segments
                        prefix = output_grid[:idx_2 + 1]          # Elements up to and including '2'
                        moved_part = block_y + ([0] * num_zeros) # The moved block Y followed by the zeros
                        suffix = output_grid[idx_block_end:]      # Elements after the original block Y
                        
                        # Combine segments to form the new grid
                        new_grid_list = prefix + moved_part + suffix
                        
                        # Basic sanity check for length preservation
                        if len(new_grid_list) == n:
                           output_grid = new_grid_list # Update the grid with the transformation
                           pattern2_found = True
                           # Stop searching for patterns after the first successful transformation
                           break 
                        # else: # If length changed, there's a logic error (should not happen here)
                           # print("Error: Length mismatch during Pattern 2 transformation") 
                           # pass

            # If Pattern 2 was successfully applied for this '2', stop the outer loop
            if pattern2_found:
                 break

    # Return the final state of the grid, formatted as a string
    # This will be the result of Pattern 2 if applied, or the original grid if no patterns matched
    return format_output(output_grid)

```
Results for code_00.py:

Train Set Results:

## Example 1:
Error: 'numpy.ndarray' object has no attribute 'split'

## Example 2:
Error: 'numpy.ndarray' object has no attribute 'split'

## Example 3:
Error: 'numpy.ndarray' object has no attribute 'split'

## Example 4:
Error: 'numpy.ndarray' object has no attribute 'split'

## Example 5:
Error: 'numpy.ndarray' object has no attribute 'split'

## Example 6:
Error: 'numpy.ndarray' object has no attribute 'split'

## Example 7:
Error: 'numpy.ndarray' object has no attribute 'split'

Test Set Results:

## Example 1:
Error: 'numpy.ndarray' object has no attribute 'split'
## General Assessment and Strategy

The primary issue identified is an input type mismatch. The previous code assumed the input was a string requiring parsing (`input_str.split()`), while the testing environment provided a data structure (likely a NumPy array or list) which does not have a `.split()` method. This caused the code to fail before the core transformation logic could be executed.

The strategy is to:
1.  **Correct Input Handling:** Modify the approach to directly accept a list or array of integers as input, eliminating the need for string parsing and formatting functions (`parse_input`, `format_output`) within the core `transform` logic.
2.  **Validate Core Logic:** Re-examine the previously defined transformation rules against all provided training examples, assuming the input is correctly handled as a list of integers. The initial walkthrough suggests the two-pattern logic (`X, 0, 2` swap prioritized over `2, 0..., 0, Y` shift) holds for the examples.
3.  **Refine Documentation:** Update the YAML facts and the natural language program to reflect the correct input object type (list/array of integers) and confirm the details of the transformation rules based on the re-evaluation.

## Metrics and Rule Validation

Based on a manual walkthrough and simulation of the intended logic (ignoring the original parsing error), the two core rules appear to cover the training examples:

1.  **Rule 1 (Swap):** Find the first instance of `X, 0, 2` where `X` is not 0 and not 2. Swap `X` and `0` -> `0, X, 2`. Stop.
2.  **Rule 2 (Shift):** If Rule 1 doesn't apply, find the first instance of `2, 0..., 0, Y` where there's at least one 0, and `Y` is a non-empty contiguous block of digits that are not 0 or 2. Move block `Y` immediately after the `2`, followed by the original intervening zeros. Stop.
3.  **Default:** If neither rule applies, return the input unchanged.

**Example Analysis:**


*code_execution:*
```python
import sys
import io

# Suppress print statements from the function itself during simulation
original_stdout = sys.stdout
sys.stdout = io.StringIO()

# --- Define the core logic function (modified to accept list, return list) ---
def simulate_transform(grid):
    n = len(grid)
    output_grid = list(grid) # Work on a copy

    # --- Check for Pattern 1: X, 0, 2 ---
    pattern1_found = False
    for i in range(n - 2):
        x = output_grid[i]
        zero = output_grid[i+1]
        two = output_grid[i+2]
        if x != 0 and x != 2 and zero == 0 and two == 2:
            output_grid[i], output_grid[i+1] = output_grid[i+1], output_grid[i]
            pattern1_found = True
            break
            
    if pattern1_found:
        return output_grid

    # --- Check for Pattern 2: 2, 0..., 0, Y ---
    pattern2_found = False
    for i in range(n):
        if output_grid[i] == 2:
            idx_2 = i
            if idx_2 + 1 < n:
                idx_first_zero = idx_2 + 1
                idx_first_non_zero_after_zeros = -1
                num_zeros = 0
                for j in range(idx_first_zero, n):
                    if output_grid[j] == 0:
                        num_zeros += 1
                    else:
                        idx_first_non_zero_after_zeros = j
                        break
                
                if num_zeros > 0 and idx_first_non_zero_after_zeros != -1:
                    idx_block_start = idx_first_non_zero_after_zeros
                    idx_block_end = idx_block_start
                    block_y = []
                    contains_2_in_block = False
                    for k in range(idx_block_start, n):
                        val = output_grid[k]
                        if val != 0 and val != 2:
                            block_y.append(val)
                            idx_block_end = k + 1
                        else:
                            if val == 2:
                                contains_2_in_block = True
                            break
                            
                    if len(block_y) > 0 and not contains_2_in_block:
                        prefix = output_grid[:idx_2 + 1]
                        moved_part = block_y + ([0] * num_zeros)
                        # Calculate where the zeros originally ended
                        original_zeros_end_idx = idx_first_zero + num_zeros
                        # Suffix starts after the original block Y OR after the zeros if Y extended to the end
                        suffix_start_idx = idx_block_end if idx_block_end > original_zeros_end_idx else original_zeros_end_idx
                        
                        # Ensure suffix calculation is robust even if Y reaches end of list
                        suffix = output_grid[idx_block_end:]

                        new_grid_list = prefix + moved_part + suffix
                        
                        # Pad with zeros if the move shortens the list (shouldn't happen with correct logic but safer)
                        if len(new_grid_list) < n:
                            new_grid_list.extend([0] * (n - len(new_grid_list)))
                        # Truncate if it somehow becomes too long
                        if len(new_grid_list) > n:
                             new_grid_list = new_grid_list[:n]

                        if len(new_grid_list) == n:
                           output_grid = new_grid_list
                           pattern2_found = True
                           break
            if pattern2_found:
                 break

    return output_grid

# --- Test Cases ---
test_cases = [
    {"id": "train_1", "input": [2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], "expected": [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    {"id": "train_2", "input": [0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 2], "expected": [0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 2]},
    {"id": "train_3", "input": [0, 2, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0], "expected": [0, 2, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0]},
    {"id": "train_4", "input": [0, 0, 0, 2, 0, 0, 0, 5, 5, 5, 5, 5], "expected": [0, 0, 0, 2, 5, 5, 5, 5, 5, 0, 0, 0]},
    {"id": "train_5", "input": [9, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], "expected": [9, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    {"id": "train_6", "input": [6, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], "expected": [0, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    {"id": "train_7", "input": [0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0], "expected": [0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0]},
]

results = []
for case in test_cases:
    output = simulate_transform(case["input"])
    match = output == case["expected"]
    results.append({
        "id": case["id"],
        "input": case["input"],
        "output": output,
        "expected": case["expected"],
        "match": match
    })

# Restore stdout
sys.stdout = original_stdout

# Print summarized results
print("Logic Simulation Results:")
for r in results:
    print(f"  {r['id']}: {'Correct' if r['match'] else 'Incorrect'} -> Output: {r['output']}")
    if not r['match']:
         print(f"     Input:    {r['input']}")
         print(f"     Expected: {r['expected']}")

# Check if all matched
all_correct = all(r['match'] for r in results)
print(f"\nOverall Logic Correct: {all_correct}")

```

*code_execution_result:*
outcome: OUTCOME_OK
```
Logic Simulation Results:
  train_1: Correct -> Output: [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  train_2: Correct -> Output: [0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 2]
  train_3: Correct -> Output: [0, 2, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0]
  train_4: Correct -> Output: [0, 0, 0, 2, 5, 5, 5, 5, 5, 0, 0, 0]
  train_5: Correct -> Output: [9, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  train_6: Correct -> Output: [0, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  train_7: Correct -> Output: [0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0]

Overall Logic Correct: True

```
The simulation confirms that the core transformation logic, when applied directly to list inputs, correctly reproduces the output for all training examples. The previous errors were solely due to the incorrect input handling assumption.

## Facts (YAML)


```yaml
Task: Conditionally rearrange elements in a sequence based on local patterns involving the numbers 0 and 2.

Input_Type: List of 12 integers.
Output_Type: List of 12 integers.

Objects:
  - Sequence: The input list of 12 integers.
  - Element: An integer within the sequence.
  - Number_Zero: The integer 0, acting as empty space or a swappable/fillable element.
  - Number_Two: The integer 2, acting as a boundary or trigger for specific transformations.
  - Non_Zero_Non_Two_Element (X): Any integer element that is not 0 and not 2.
  - Zero_Block: A contiguous sub-sequence containing only 0s.
  - Movable_Block (Y): A contiguous sub-sequence containing only Non_Zero_Non_Two_Elements.

Properties:
  - Position: The index (0-11) of an element in the sequence.
  - Value: The integer value of an element.
  - Adjacency: Elements at consecutive indices.
  - Contiguity: Elements forming an unbroken block.

Relationships/Patterns:
  - Pattern_Swap: A Non_Zero_Non_Two_Element `X` followed immediately by a 0, followed immediately by a 2 (sub-sequence `X, 0, 2`). Found by scanning left-to-right.
  - Pattern_Shift: The integer 2 followed immediately by a Zero_Block (of length >= 1), followed immediately by a Movable_Block `Y`. (sub-sequence `2, 0..., 0, Y`). Found by scanning left-to-right for the initial '2'.

Actions:
  - Scan: Iterate through the sequence (typically left-to-right) to find the first occurrence of a pattern.
  - Identify: Recognize occurrences of Pattern_Swap or Pattern_Shift.
  - Apply_Swap: If Pattern_Swap is found first, swap the positions of `X` and 0.
  - Apply_Shift: If Pattern_Shift is found first (and Pattern_Swap was not found), move the Movable_Block `Y` to the position immediately following the '2', and place the Zero_Block immediately after the moved `Y`.
  - Halt: Stop processing and return the modified sequence after the first applicable action (Swap or Shift) is performed.
  - No_Change: If neither pattern is found during the scan, return the original sequence unmodified.
```


## Natural Language Program

1.  Receive the input as a list of 12 integers. Create a mutable copy of this list to potentially modify.
2.  Scan the list from left to right (index `i` from 0 up to length-3). Check if the sub-sequence starting at index `i` matches the pattern `X, 0, 2`, where `X` is any integer other than 0 or 2.
3.  If the first occurrence of the `X, 0, 2` pattern is found at index `i`:
    a.  Swap the elements at index `i` (the value `X`) and index `i+1` (the value 0).
    b.  Stop scanning. The transformation is complete. Return the modified list.
4.  If the `X, 0, 2` pattern is *not* found anywhere in the list after scanning:
    a.  Scan the list again from left to right (index `i` from 0 up to length-1) to find the first occurrence of the integer 2.
    b.  If a 2 is found at index `idx_2`, check the elements immediately following it.
    c.  Identify the contiguous block of one or more zeros starting at `idx_2 + 1`. Let the number of zeros be `num_zeros`.
    d.  Immediately after this block of zeros, identify the contiguous block `Y` consisting only of non-zero, non-2 integers. Check that such a block `Y` exists and is not empty.
    e.  If such a pattern `2, (zeros), Y` is found (where `num_zeros >= 1` and `Y` is valid and non-empty):
        i.  Construct the new sequence: Take the elements up to and including the `2` (from index 0 to `idx_2`). Append the block `Y`. Append `num_zeros` zeros. Append any remaining elements from the original list that came *after* the original position of block `Y`.
        ii. Stop scanning. The transformation is complete. Return the newly constructed list.
5.  If neither the `X, 0, 2` pattern nor the `2, (zeros), Y` pattern is found and applied, return the original, unmodified input list.
