
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
```python
import numpy as np

"""
The transformation rule operates on a 1D NumPy array of integers. It identifies
all occurrences of the integer '2'. For each '2', it checks its immediate left
and right neighbors based on the *original* input array. If a neighbor is '0',
it identifies the full contiguous block of '0's extending away from the '2' in
that direction, again based on the original input. It then looks at the element
immediately bordering this block of '0's on the side opposite the '2' in the
original input. If this bordering element exists (is within the array bounds)
and is non-zero, the entire contiguous block of '0's in the *output* array is
replaced with the value of that non-zero bordering element. This check and
potential replacement are performed independently for the left and right sides
of each '2' found in the array. If no '2' is present, or if the conditions for
replacement (adjacent '0' block bordered by a non-zero digit) are not met for
a given side, the corresponding section of the output array remains unchanged
from the initial copy of the input.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the zero-filling rule adjacent to '2's based on bordering non-zero digits.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence of integers.
    """
    # Initialize output_grid as a copy of the input to allow modifications
    # All checks for conditions (locations of 2s, 0s, fill digits) will be done
    # on the original input_grid, but modifications will be applied to output_grid.
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # Find indices of all elements equal to 2 in the original input
    two_indices = np.where(input_grid == 2)[0]

    # Iterate through each index where a '2' was found in the input
    for idx in two_indices:

        # --- Check Left Side ---
        # Check if there's an element to the left and if it's 0 in the input_grid
        if idx > 0 and input_grid[idx - 1] == 0:
            # Find the start of the contiguous block of zeros ending at idx - 1
            # We scan leftwards from idx - 1
            zero_end_left = idx - 1
            zero_start_left = zero_end_left
            # Keep moving left as long as we are in bounds and see a 0 in the input
            while zero_start_left > 0 and input_grid[zero_start_left - 1] == 0:
                zero_start_left -= 1

            # Check the element bordering the zero block on the far left in the input_grid
            fill_digit_idx_left = zero_start_left - 1
            # Ensure the border index is valid
            if fill_digit_idx_left >= 0:
                fill_digit_left = input_grid[fill_digit_idx_left]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_left != 0:
                    # Modify the output_grid in the range of the zero block
                    output_grid[zero_start_left : zero_end_left + 1] = fill_digit_left

        # --- Check Right Side ---
        # Check if there's an element to the right and if it's 0 in the input_grid
        if idx < n - 1 and input_grid[idx + 1] == 0:
            # Find the end of the contiguous block of zeros starting at idx + 1
            # We scan rightwards from idx + 1
            zero_start_right = idx + 1
            zero_end_right = zero_start_right
            # Keep moving right as long as we are in bounds and see a 0 in the input
            while zero_end_right < n - 1 and input_grid[zero_end_right + 1] == 0:
                zero_end_right += 1

            # Check the element bordering the zero block on the far right in the input_grid
            fill_digit_idx_right = zero_end_right + 1
            # Ensure the border index is valid
            if fill_digit_idx_right < n:
                fill_digit_right = input_grid[fill_digit_idx_right]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_right != 0:
                     # Modify the output_grid in the range of the zero block
                    output_grid[zero_start_right : zero_end_right + 1] = fill_digit_right

    # Return the modified grid
    return output_grid
```
