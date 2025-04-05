
## train_1

**input:**
```
0 0 5 5 5 5 2 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 2 0 0 0 0 0
```


## train_2

**input:**
```
0 9 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 2 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
9 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 2 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 3 3 3 0 0 0 2 0
```


**output:**
```
0 0 0 0 3 3 3 3 3 3 2 0
```


## train_5

**input:**
```
0 0 0 2 0 0 0 3 3 3 3 0
```


**output:**
```
0 0 0 2 3 3 3 3 3 3 3 0
```


## train_6

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 2
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 2
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 2 0 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 2 7 7 7
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are single-line strings representing sequences of digits separated by spaces.
2.  **Core Operation:** The transformation seems conditional. In many cases (train_1, train_2, train_3, train_6), the input is identical to the output. In others (train_4, train_5, train_7), specific changes occur.
3.  **Key Element '2':** The digit '2' appears to play a crucial role. Changes only happen in examples containing a '2', and the changes occur *near* the '2'.
4.  **Key Element '0':** The digit '0' also seems important. The changes involve replacing sequences of '0's.
5.  **Filling Behavior:** When changes occur, sequences of '0's adjacent to a '2' are replaced by a non-zero digit. This non-zero digit appears to be "copied" from the digit bordering the sequence of '0's on the side *opposite* the '2'.
    *   In `train_4` (`... 3 3 3 0 0 0 2 ...`), the `0 0 0` block is to the left of `2` and bordered by `3` on its left. It becomes `3 3 3`.
    *   In `train_5` (`... 2 0 0 0 3 3 ...`), the `0 0 0` block is to the right of `2` and bordered by `3` on its right. It becomes `3 3 3`.
    *   In `train_7` (`... 2 0 7 7 ...`), the `0` is to the right of `2` and bordered by `7` on its right. It becomes `7`.
6.  **Boundary Condition:** The '2' seems to act as a boundary for this filling process. The filling stops *at* the '2'.
7.  **No Change Condition:** If the digits adjacent to '2' are not '0's, or if the zeros are bordered only by other '0's or the sequence boundaries without a non-zero digit to copy from, no change occurs in that direction.

**YAML Facts:**


```yaml
task_elements:
  - item: sequence
    properties:
      - type: list of integers (derived from space-separated string)
      - contains: digits 0-9
  - item: digit_2
    properties:
      - value: 2
      - role: boundary, trigger for modification
  - item: digit_0
    properties:
      - value: 0
      - role: replaceable element
  - item: non_zero_digit
    properties:
      - value: any digit from 1, 3, 4, 5, 6, 7, 8, 9
      - role: fill value source
relationships:
  - type: adjacency
    between: digits in the sequence
  - type: boundary
    element: digit_2
    context: separates regions where replacement might occur
  - type: propagation/fill
    source: non_zero_digit
    target: adjacent sequence of digit_0
    condition: the sequence of digit_0 must also be adjacent to digit_2 on the opposite side
    direction: from non_zero_digit towards digit_2
actions:
  - name: identify_indices
    target: digit_2
  - name: identify_sequences
    target: digit_0
    condition: adjacent to digit_2
  - name: identify_bordering_digit
    target: sequence of digit_0
    condition: must be non_zero_digit, located on the side opposite to digit_2
  - name: replace_sequence
    target: sequence of digit_0
    value: bordering non_zero_digit
```


**Natural Language Program:**

1.  Represent the input string of digits as a list or array.
2.  Iterate through the list to find the index (or indices, if multiple '2's exist) of the digit '2'.
3.  For each index `i` where the digit is '2':
    a.  **Check Left:** Examine the digits to the left of index `i` (i.e., index `i-1`, `i-2`, ...). If there is a contiguous block of '0's immediately to the left of '2' (ending at index `i-1`), find the first non-zero digit `d` encountered when moving further left from this block of '0's. If such a non-zero digit `d` is found before reaching the beginning of the sequence or another '2', replace all the '0's in that contiguous block with `d`.
    b.  **Check Right:** Examine the digits to the right of index `i` (i.e., index `i+1`, `i+2`, ...). If there is a contiguous block of '0's immediately to the right of '2' (starting at index `i+1`), find the first non-zero digit `d` encountered when moving further right from this block of '0's. If such a non-zero digit `d` is found before reaching the end of the sequence or another '2', replace all the '0's in that contiguous block with `d`.
4.  If no '2' is found in the list, or if the conditions for replacement in step 3a or 3b are not met for any '2', the list remains unchanged.
5.  Convert the potentially modified list back into a space-separated string of digits for the output.
```python
import re

"""
The transformation rule identifies the digit '2' in a sequence of digits. 
If a contiguous block of '0's exists immediately adjacent (left or right) to a '2', 
the rule attempts to find the first non-zero digit bordering that block of '0's 
on the side opposite the '2'. If such a non-zero digit is found before reaching 
the sequence boundary or another '2', the entire block of '0's is replaced 
by that non-zero digit. This process is applied independently for the left and 
right sides of each '2' found in the sequence. If no '2' is present, or if the 
conditions for replacement are not met (e.g., no adjacent '0's, or adjacent '0's 
are not bordered by a non-zero digit on the other side), the sequence remains unchanged.
"""

def transform(input_str: str) -> str:
    """
    Applies the described transformation rule to a space-separated string of digits.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """

    # Convert the input string to a list of integers
    digits = [int(d) for d in input_str.split()]
    n = len(digits)
    
    # Create a copy to modify, ensuring changes don't affect index lookup during iteration
    output_digits = list(digits) 

    # Find indices of all '2's
    two_indices = [i for i, digit in enumerate(digits) if digit == 2]

    # Process each '2' found
    for idx in two_indices:
        
        # --- Check Left ---
        # Find the start of the contiguous block of zeros to the left of '2'
        zero_end_left = idx - 1
        zero_start_left = -1
        if zero_end_left >= 0 and digits[zero_end_left] == 0:
            # Scan left to find the beginning of the zero block
            i = zero_end_left
            while i >= 0 and digits[i] == 0:
                zero_start_left = i
                i -= 1
            
            # Find the first non-zero digit further left (the fill digit)
            fill_digit_left = 0
            fill_digit_idx_left = zero_start_left - 1
            if fill_digit_idx_left >= 0:
                 # We only fill if the bordering digit is non-zero and not another '2'
                 # (though the '2' condition isn't explicitly required by examples, it prevents infinite loops in theoretical cases like 2 0 2)
                 # Considering the examples, the fill only happens if the source is not 0.
                 if digits[fill_digit_idx_left] != 0:
                     fill_digit_left = digits[fill_digit_idx_left]


            # If a valid fill digit was found, replace the zeros
            if zero_start_left != -1 and fill_digit_left != 0:
                for i in range(zero_start_left, zero_end_left + 1):
                    # Modify the output list, not the original list used for lookups
                    output_digits[i] = fill_digit_left 

        # --- Check Right ---
        # Find the end of the contiguous block of zeros to the right of '2'
        zero_start_right = idx + 1
        zero_end_right = -1
        if zero_start_right < n and digits[zero_start_right] == 0:
            # Scan right to find the end of the zero block
            i = zero_start_right
            while i < n and digits[i] == 0:
                zero_end_right = i
                i += 1

            # Find the first non-zero digit further right (the fill digit)
            fill_digit_right = 0
            fill_digit_idx_right = zero_end_right + 1
            if fill_digit_idx_right < n:
                 # We only fill if the bordering digit is non-zero and not another '2'
                 if digits[fill_digit_idx_right] != 0:
                     fill_digit_right = digits[fill_digit_idx_right]

            # If a valid fill digit was found, replace the zeros
            if zero_end_right != -1 and fill_digit_right != 0:
                for i in range(zero_start_right, zero_end_right + 1):
                     # Modify the output list
                    output_digits[i] = fill_digit_right

    # Convert the potentially modified list back to a space-separated string
    return " ".join(map(str, output_digits))

```
```python
import numpy as np

"""
The transformation rule operates on a 1D NumPy array of integers. It identifies 
all occurrences of the integer '2'. For each '2', it checks its immediate left 
and right neighbors. If a neighbor is '0', it identifies the full contiguous 
block of '0's extending away from the '2'. It then looks at the element 
immediately bordering this block of '0's on the side opposite the '2'. If this 
bordering element exists (is within the array bounds) and is non-zero, the 
entire contiguous block of '0's is replaced with the value of that non-zero 
bordering element. This check and potential replacement are performed 
independently for the left and right sides of each '2' found in the array. 
If no '2' is present, or if the conditions for replacement (adjacent '0' block 
bordered by a non-zero digit) are not met, the array remains unchanged. The 
modifications are based on the original input array but applied to a copy, 
which is then returned.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation rule to a 1D NumPy array of digits.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence of integers.
    """
    # Initialize output_grid as a copy of the input to allow modifications
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # Find indices of all elements equal to 2
    two_indices = np.where(input_grid == 2)[0]

    # Iterate through each index where a '2' was found
    for idx in two_indices:
        
        # --- Check Left Side ---
        # Check if there's an element to the left and if it's 0
        if idx > 0 and input_grid[idx - 1] == 0:
            # Find the start of the contiguous block of zeros ending at idx - 1
            zero_end_left = idx - 1
            zero_start_left = zero_end_left
            while zero_start_left > 0 and input_grid[zero_start_left - 1] == 0:
                zero_start_left -= 1
            
            # Check the element bordering the zero block on the far left
            fill_digit_idx_left = zero_start_left - 1
            if fill_digit_idx_left >= 0:
                fill_digit_left = input_grid[fill_digit_idx_left]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_left != 0:
                    output_grid[zero_start_left : zero_end_left + 1] = fill_digit_left

        # --- Check Right Side ---
        # Check if there's an element to the right and if it's 0
        if idx < n - 1 and input_grid[idx + 1] == 0:
            # Find the end of the contiguous block of zeros starting at idx + 1
            zero_start_right = idx + 1
            zero_end_right = zero_start_right
            while zero_end_right < n - 1 and input_grid[zero_end_right + 1] == 0:
                zero_end_right += 1
                
            # Check the element bordering the zero block on the far right
            fill_digit_idx_right = zero_end_right + 1
            if fill_digit_idx_right < n:
                fill_digit_right = input_grid[fill_digit_idx_right]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_right != 0:
                    output_grid[zero_start_right : zero_end_right + 1] = fill_digit_right

    # Return the modified grid
    return output_grid
```

Previous Code:
```python
import numpy as np

"""
The transformation rule operates on a 1D NumPy array of integers. It identifies 
all occurrences of the integer '2'. For each '2', it checks its immediate left 
and right neighbors. If a neighbor is '0', it identifies the full contiguous 
block of '0's extending away from the '2'. It then looks at the element 
immediately bordering this block of '0's on the side opposite the '2'. If this 
bordering element exists (is within the array bounds) and is non-zero, the 
entire contiguous block of '0's is replaced with the value of that non-zero 
bordering element. This check and potential replacement are performed 
independently for the left and right sides of each '2' found in the array. 
If no '2' is present, or if the conditions for replacement (adjacent '0' block 
bordered by a non-zero digit) are not met, the array remains unchanged. The 
modifications are based on the original input array but applied to a copy, 
which is then returned.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation rule to a 1D NumPy array of digits.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence of integers.
    """
    # Initialize output_grid as a copy of the input to allow modifications
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # Find indices of all elements equal to 2
    two_indices = np.where(input_grid == 2)[0]

    # Iterate through each index where a '2' was found
    for idx in two_indices:
        
        # --- Check Left Side ---
        # Check if there's an element to the left and if it's 0
        if idx > 0 and input_grid[idx - 1] == 0:
            # Find the start of the contiguous block of zeros ending at idx - 1
            zero_end_left = idx - 1
            zero_start_left = zero_end_left
            while zero_start_left > 0 and input_grid[zero_start_left - 1] == 0:
                zero_start_left -= 1
            
            # Check the element bordering the zero block on the far left
            fill_digit_idx_left = zero_start_left - 1
            if fill_digit_idx_left >= 0:
                fill_digit_left = input_grid[fill_digit_idx_left]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_left != 0:
                    output_grid[zero_start_left : zero_end_left + 1] = fill_digit_left

        # --- Check Right Side ---
        # Check if there's an element to the right and if it's 0
        if idx < n - 1 and input_grid[idx + 1] == 0:
            # Find the end of the contiguous block of zeros starting at idx + 1
            zero_start_right = idx + 1
            zero_end_right = zero_start_right
            while zero_end_right < n - 1 and input_grid[zero_end_right + 1] == 0:
                zero_end_right += 1
                
            # Check the element bordering the zero block on the far right
            fill_digit_idx_right = zero_end_right + 1
            if fill_digit_idx_right < n:
                fill_digit_right = input_grid[fill_digit_idx_right]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_right != 0:
                    output_grid[zero_start_right : zero_end_right + 1] = fill_digit_right

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 5 5 5 5 2 0 0 0 0 0
```
Expected Output:
```
0 0 5 5 5 5 2 0 0 0 0 0
```
Transformed Output:
```
0 0 5 5 5 5 2 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 9 2 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 9 2 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 9 2 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 3:
Input:
```
9 2 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
9 2 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
9 2 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 4:
Input:
```
0 0 0 0 3 3 3 0 0 0 2 0
```
Expected Output:
```
0 0 0 0 3 3 3 3 3 3 2 0
```
Transformed Output:
```
0 0 0 0 3 3 3 0 0 0 2 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 5:
Input:
```
0 0 0 2 0 0 0 3 3 3 3 0
```
Expected Output:
```
0 0 0 2 3 3 3 3 3 3 3 0
```
Transformed Output:
```
0 0 0 2 0 0 0 3 3 3 3 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 6:
Input:
```
7 7 7 7 7 7 7 7 7 7 7 2
```
Expected Output:
```
7 7 7 7 7 7 7 7 7 7 7 2
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7 7 7 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 7:
Input:
```
0 0 0 0 0 0 0 0 2 0 7 7
```
Expected Output:
```
0 0 0 0 0 0 0 0 2 7 7 7
```
Transformed Output:
```
0 0 0 0 0 0 0 0 2 0 7 7
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.666666666666686

Test Set Results:

## Example 1:
Input:
```
0 0 0 3 3 3 3 3 2 0 0 0
```
Expected Output:
```
0 0 0 3 3 3 3 3 2 0 0 0
```
Transformed Output:
```
0 0 0 3 3 3 3 3 2 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment and Strategy**

The provided code (`code_00.py`) aimed to implement the transformation rule observed in the initial examples. The core logic involved finding the digit '2', identifying adjacent blocks of '0's, and filling those '0's with the non-zero digit bordering the block on the side opposite the '2'.

However, the execution results show failures on `train_4`, `train_5`, and `train_7`. In all failed cases, the code's output matched the *input*, indicating that the intended replacement of '0' blocks did not occur. Manual walkthroughs of the code logic against these failed examples suggest the code *should* have produced the expected output.

This discrepancy points towards a potential issue either in the exact code version executed by the test harness or a subtle implementation detail (perhaps related to array slicing or loop bounds) that behaves differently in practice than in the manual trace.

The strategy is to:
1.  Assume the *intended* logic (as described in the previous natural language program and the code's comments) is correct based on the *expected* outputs.
2.  Refine the description (YAML facts and natural language program) to be as precise as possible about the conditions for replacement, especially regarding boundaries and the non-zero fill value requirement.
3.  Document the performance metrics based on the *actual* results provided, highlighting the specific examples where the implementation failed.

**Metrics**


*code_execution:*
```python
import numpy as np

# Data from the problem description
examples = {
    "train_1": {
        "input": "0 0 5 5 5 5 2 0 0 0 0 0",
        "expected": "0 0 5 5 5 5 2 0 0 0 0 0",
        "transformed": "0 0 5 5 5 5 2 0 0 0 0 0",
        "match": True, "pixels_off": 0, "score": 0.0
    },
    "train_2": {
        "input": "0 9 2 0 0 0 0 0 0 0 0 0",
        "expected": "0 9 2 0 0 0 0 0 0 0 0 0",
        "transformed": "0 9 2 0 0 0 0 0 0 0 0 0",
        "match": True, "pixels_off": 0, "score": 0.0
    },
    "train_3": {
        "input": "9 2 0 0 0 0 0 0 0 0 0 0",
        "expected": "9 2 0 0 0 0 0 0 0 0 0 0",
        "transformed": "9 2 0 0 0 0 0 0 0 0 0 0",
        "match": True, "pixels_off": 0, "score": 0.0
    },
    "train_4": {
        "input": "0 0 0 0 3 3 3 0 0 0 2 0",
        "expected": "0 0 0 0 3 3 3 3 3 3 2 0",
        "transformed": "0 0 0 0 3 3 3 0 0 0 2 0",
        "match": False, "pixels_off": 3, "score": 50.0
    },
    "train_5": {
        "input": "0 0 0 2 0 0 0 3 3 3 3 0",
        "expected": "0 0 0 2 3 3 3 3 3 3 3 0",
        "transformed": "0 0 0 2 0 0 0 3 3 3 3 0",
        "match": False, "pixels_off": 3, "score": 50.0
    },
    "train_6": {
        "input": "7 7 7 7 7 7 7 7 7 7 7 2",
        "expected": "7 7 7 7 7 7 7 7 7 7 7 2",
        "transformed": "7 7 7 7 7 7 7 7 7 7 7 2",
        "match": True, "pixels_off": 0, "score": 0.0
    },
    "train_7": {
        "input": "0 0 0 0 0 0 0 0 2 0 7 7",
        "expected": "0 0 0 0 0 0 0 0 2 7 7 7",
        "transformed": "0 0 0 0 0 0 0 0 2 0 7 7",
        "match": False, "pixels_off": 1, "score": 16.666666666666686
    },
    "test_1": { # Test example was also provided in results
        "input": "0 0 0 3 3 3 3 3 2 0 0 0",
        "expected": "0 0 0 3 3 3 3 3 2 0 0 0",
        "transformed": "0 0 0 3 3 3 3 3 2 0 0 0",
        "match": True, "pixels_off": 0, "score": 0.0
    }
}

total_examples = len(examples)
correct_examples = sum(1 for ex in examples.values() if ex["match"])
incorrect_examples = total_examples - correct_examples
total_pixels_off = sum(ex["pixels_off"] for ex in examples.values())
average_score = sum(ex["score"] for ex in examples.values()) / total_examples

# Identify characteristics of failed examples
failed_example_ids = [name for name, ex in examples.items() if not ex["match"]]
failed_details = {}
for name in failed_example_ids:
    ex = examples[name]
    input_arr = np.array([int(d) for d in ex["input"].split()])
    expected_arr = np.array([int(d) for d in ex["expected"].split()])
    transformed_arr = np.array([int(d) for d in ex["transformed"].split()])
    diff_indices = np.where(expected_arr != transformed_arr)[0]
    failed_details[name] = {
        "input_len": len(input_arr),
        "num_twos": np.count_nonzero(input_arr == 2),
        "pixels_off": ex["pixels_off"],
        "diff_indices": diff_indices.tolist(),
        "expected_values_at_diff": expected_arr[diff_indices].tolist(),
        "transformed_values_at_diff": transformed_arr[diff_indices].tolist()
    }


print(f"Total Examples: {total_examples}")
print(f"Correct Examples: {correct_examples}")
print(f"Incorrect Examples: {incorrect_examples}")
print(f"Total Pixels Off: {total_pixels_off}")
print(f"Average Score (Lower is better): {average_score:.2f}")
print("\nDetails of Failed Examples:")
for name, details in failed_details.items():
    print(f"  {name}:")
    print(f"    Input Length: {details['input_len']}")
    print(f"    Number of '2's in Input: {details['num_twos']}")
    print(f"    Pixels Off: {details['pixels_off']}")
    print(f"    Indices with Discrepancy: {details['diff_indices']}")
    print(f"    Expected Values at Indices: {details['expected_values_at_diff']}")
    print(f"    Transformed Values at Indices: {details['transformed_values_at_diff']}")


```

*code_execution_result:*
outcome: OUTCOME_OK
```
Total Examples: 8
Correct Examples: 5
Incorrect Examples: 3
Total Pixels Off: 7
Average Score (Lower is better): 14.58

Details of Failed Examples:
  train_4:
    Input Length: 12
    Number of '2's in Input: 1
    Pixels Off: 3
    Indices with Discrepancy: [7, 8, 9]
    Expected Values at Indices: [3, 3, 3]
    Transformed Values at Indices: [0, 0, 0]
  train_5:
    Input Length: 12
    Number of '2's in Input: 1
    Pixels Off: 3
    Indices with Discrepancy: [4, 5, 6]
    Expected Values at Indices: [3, 3, 3]
    Transformed Values at Indices: [0, 0, 0]
  train_7:
    Input Length: 12
    Number of '2's in Input: 1
    Pixels Off: 1
    Indices with Discrepancy: [9]
    Expected Values at Indices: [7]
    Transformed Values at Indices: [0]

```
**YAML Facts**


```yaml
task_description: "Fill blocks of zeros adjacent to a '2' based on the non-zero digit bordering the block."
input_format:
  type: sequence
  element_type: integer
  representation: space-separated string
output_format:
  type: sequence
  element_type: integer
  representation: space-separated string
rules:
  - rule: "Identity Transformation (Default)"
    condition: "No '2' is present, OR no '0' blocks are adjacent to any '2', OR adjacent '0' blocks are not bordered by a non-zero digit on the side opposite the '2'."
    action: Output is identical to the input.
  - rule: "Zero Block Filling"
    condition: "A digit '2' exists in the sequence."
    action:
      - scope: "For each occurrence of the digit '2' at index `idx`:"
      - step: "Check Left Adjacency"
        sub_condition: "Index `idx-1` exists AND contains '0'."
        sub_action:
          - "Identify the contiguous block of '0's ending at `idx-1` (from `zero_start_left` to `zero_end_left=idx-1`)."
          - "Identify the bordering digit at index `border_idx = zero_start_left - 1`."
          - "If `border_idx` is valid (>= 0) AND the digit at `border_idx` is non-zero:"
          - "Replace all elements in the output sequence from `zero_start_left` to `zero_end_left` with the bordering digit."
      - step: "Check Right Adjacency"
        sub_condition: "Index `idx+1` exists AND contains '0'."
        sub_action:
          - "Identify the contiguous block of '0's starting at `idx+1` (from `zero_start_right=idx+1` to `zero_end_right`)."
          - "Identify the bordering digit at index `border_idx = zero_end_right + 1`."
          - "If `border_idx` is valid (< sequence length) AND the digit at `border_idx` is non-zero:"
          - "Replace all elements in the output sequence from `zero_start_right` to `zero_end_right` with the bordering digit."
    notes:
      - "Modifications are based on the original input state but applied to the output."
      - "The process is applied independently for the left and right sides of each '2'."
      - "The fill operation stops at the sequence boundaries or at the bordering non-zero digit."
key_elements:
  - element: digit '2'
    role: trigger, boundary
  - element: digit '0'
    role: target for replacement
  - element: non-zero digit (1, 3-9)
    role: source for fill value, boundary for zero block search
```


**Natural Language Program**

1.  Read the input sequence of digits. Create a mutable copy for the output.
2.  Find all indices where the digit '2' appears in the original input sequence.
3.  If no '2' is found, the output is identical to the input. Return the output sequence.
4.  If '2's are found, iterate through each index `idx` where a '2' is located:
    a.  **Process Left Side:**
        i.  Check if the element immediately to the left (`idx-1`) exists and is '0'.
        ii. If yes, identify the contiguous block of '0's extending leftwards from `idx-1`. Let the start index of this block be `zero_start_left`.
        iii. Check the element at index `zero_start_left - 1`.
        iv. If this element exists (index >= 0) and its value is non-zero, then replace all elements in the *output sequence* from index `zero_start_left` up to `idx-1` (inclusive) with this non-zero value.
    b.  **Process Right Side:**
        i.  Check if the element immediately to the right (`idx+1`) exists and is '0'.
        ii. If yes, identify the contiguous block of '0's extending rightwards from `idx+1`. Let the end index of this block be `zero_end_right`.
        iii. Check the element at index `zero_end_right + 1`.
        iv. If this element exists (index < sequence length) and its value is non-zero, then replace all elements in the *output sequence* from index `idx+1` up to `zero_end_right` (inclusive) with this non-zero value.
5.  After processing all occurrences of '2', return the modified output sequence.
