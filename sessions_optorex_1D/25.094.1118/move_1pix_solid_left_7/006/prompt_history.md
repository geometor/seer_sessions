
## train_1

**input:**
```
0 0 0 8 8 8 8 8 8 8 8 0
```


**output:**
```
0 0 8 8 8 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 6 6 6
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 6 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 5 5 5 5 5 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 8 8 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 0 0
```


## train_6

**input:**
```
0 0 0 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 6 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 2 2 2 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception of Task Elements:**

The input and output are sequences of single digits, presented as space-separated strings. The primary characteristic of the input sequences is the presence of a contiguous block of identical non-zero digits surrounded by zeros. The transformation appears to involve shifting this non-zero block one position towards the beginning of the sequence, effectively swapping it with the zero immediately preceding it.

**YAML Fact Documentation:**


```yaml
Task: Shift Non-Zero Block Left

Input:
  Type: String
  Format: Space-separated single digits
  Content: Contains a sequence of digits, primarily '0', with one contiguous block of identical non-zero digits.

Output:
  Type: String
  Format: Space-separated single digits
  Content: A permutation of the input sequence.

Objects:
  - Sequence: The list of digits derived from the input/output string.
  - Zero: The digit '0'.
  - NonZeroBlock: A contiguous sub-sequence within the main Sequence, containing identical digits other than '0'.
  - PrecedingZero: The '0' element immediately before the NonZeroBlock in the input Sequence.

Relationships:
  - NonZeroBlock is surrounded by Zero elements in the input (except potentially at the very ends, although examples show internal blocks).
  - The Output Sequence is formed by moving the NonZeroBlock one position earlier in the Sequence compared to the Input Sequence.
  - The PrecedingZero from the input moves to the position immediately after where the NonZeroBlock ends in the output.

Actions:
  - Identify: Locate the start and end indices of the NonZeroBlock.
  - Identify: Locate the index of the PrecedingZero (which is start_index - 1).
  - Shift: Move the NonZeroBlock one position to the left.
  - Relocate: Move the PrecedingZero to the position immediately following the shifted NonZeroBlock.

Transformation:
  Rule: Swap the NonZeroBlock with the single Zero element immediately preceding it. All other elements retain their relative order.
  Constraint: Assumes there is exactly one such NonZeroBlock and at least one Zero preceding it.
```


**Natural Language Program:**

1.  Parse the input string into a list of digit strings.
2.  Find the starting index of the first non-zero digit block. If no non-zero digits exist, return the original input list joined back into a string.
3.  Find the ending index of this contiguous non-zero digit block.
4.  If the starting index is 0 (the block is already at the beginning), return the original input list joined back into a string.
5.  Extract the non-zero block (from the start index to the end index, inclusive).
6.  Extract the zero element immediately preceding the block (at start index - 1).
7.  Construct the output list:
    a.  Take all elements from the beginning of the input list up to (but not including) the preceding zero (index `start_index - 1`).
    b.  Append the extracted non-zero block.
    c.  Append the extracted preceding zero.
    d.  Append all remaining elements from the input list that came *after* the non-zero block (from index `end_index + 1` to the end).
8.  Join the elements of the newly constructed output list with spaces to form the final output string.
```python
import re

def find_non_zero_block(data_list):
    """
    Finds the start and end indices of the first contiguous block of 
    identical non-zero digits.

    Args:
        data_list: A list of strings representing digits.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
        Returns (-1, -1) if the block starts at index 0.
    """
    start_index = -1
    end_index = -1
    block_digit = None

    for i, digit in enumerate(data_list):
        if digit != '0':
            # Found the start of a potential block
            if start_index == -1:
                 # Check if block starts at the very beginning
                if i == 0:
                    return -1, -1 # Indicate block starts at index 0
                start_index = i
                block_digit = digit
            # Continue the block if the digit matches
            elif digit == block_digit:
                end_index = i
            # Found a different digit, block ended previously or it's a single digit
            else:
                if end_index == -1: # Handle single non-zero digit case
                    end_index = start_index
                break # Found the end of the first block
        elif start_index != -1:
            # Found a zero after the block started
            if end_index == -1: # Handle single non-zero digit case
                end_index = start_index
            break # End of block

    # Handle case where block goes to the end of the list
    if start_index != -1 and end_index == -1:
        # This handles blocks of size 1 at the end, or longer blocks ending at the list end.
        # Find the actual end of the block if not already set
        current_end = start_index
        for j in range(start_index + 1, len(data_list)):
            if data_list[j] == block_digit:
                current_end = j
            else:
                break
        end_index = current_end


    if start_index != -1 and end_index != -1:
        return start_index, end_index
    elif start_index != -1: # Handles a single non-zero digit not at the start
         return start_index, start_index
    else:
        return None # No non-zero block found


def transform(input_str):
    """
    Transforms the input string by finding the first contiguous block of 
    identical non-zero digits and swapping it with the single zero 
    immediately preceding it. If the block is already at the beginning 
    or no non-zero block exists, the original string is returned.
    """
    # Parse the input string into a list of digit strings.
    input_list = input_str.split(' ')

    # Find the start and end indices of the non-zero block.
    block_indices = find_non_zero_block(input_list)

    # If no block found, return original string
    if block_indices is None:
        return input_str

    start_index, end_index = block_indices

    # If block starts at index 0, return original string
    if start_index == -1:
        return input_str
        
    # Ensure the element before the block is actually '0' (as per pattern)
    # Although find_non_zero_block implies it, good to be explicit/safe
    if start_index == 0 or input_list[start_index - 1] != '0':
         # This case covers blocks starting at index 0 or blocks not preceded by '0'
         # Based on examples, blocks are always preceded by '0' unless at index 0
        return input_str


    # Extract the parts of the list for rearrangement
    prefix = input_list[:start_index - 1]
    preceding_zero = [input_list[start_index - 1]] # Keep as list for concatenation
    non_zero_block = input_list[start_index : end_index + 1]
    suffix = input_list[end_index + 1:]

    # Construct the output list by swapping the preceding zero and the block
    output_list = prefix + non_zero_block + preceding_zero + suffix

    # Join the elements of the output list with spaces
    output_str = ' '.join(output_list)

    return output_str
```
```python
"""
Transforms a 1D NumPy array by finding the first contiguous block of identical 
non-zero integers. If such a block exists and is preceded by a zero, 
the block is swapped with that preceding zero. If the block starts at 
index 0 or no non-zero block is found, the original array is returned.
"""

import numpy as np

def find_first_non_zero_block(arr):
    """
    Finds the start and end indices of the first contiguous block of 
    identical non-zero integers in a 1D NumPy array.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found and is 
        preceded by a zero.
        Returns (-1, -1) if a block is found starting at index 0.
        Returns None if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    block_digit = None

    for i, digit in enumerate(arr):
        # Found a non-zero digit
        if digit != 0:
            # If this is the start of a potential block
            if start_index == -1:
                # Check if the block starts at the very beginning
                if i == 0:
                    return -1, -1  # Indicate block starts at index 0
                # Check if the preceding element is 0 (required for the swap)
                if arr[i - 1] == 0:
                     start_index = i
                     block_digit = digit
                     end_index = i # Initialize end index
                else:
                    # Found a non-zero not preceded by 0, skip (based on pattern)
                    # Or handle differently if requirements change
                    continue 
            # If continuing an existing block
            elif digit == block_digit:
                end_index = i
            # If found a different non-zero digit, the first block ended
            elif digit != block_digit:
                 break # Stop after the first block is fully identified
        # Found a zero
        elif digit == 0:
            # If we were tracking a block, it just ended
            if start_index != -1:
                break # Stop after the first block is fully identified

    # After loop, check if a valid block was found
    if start_index != -1:
        # Ensure end_index is set (handles single-element blocks)
        if end_index == -1:
            end_index = start_index
        return start_index, end_index
    else:
        # No block preceded by zero was found
        return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block-shifting transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied, or the 
        original array if no transformation is applicable.
    """
    # Find the first contiguous block of identical non-zero numbers preceded by a zero
    block_indices = find_first_non_zero_block(input_grid)

    # Case 1: No suitable block found
    if block_indices is None:
        return input_grid.copy() # Return a copy to avoid modifying original

    start_index, end_index = block_indices

    # Case 2: Block starts at index 0 (signaled by start_index == -1)
    if start_index == -1:
         return input_grid.copy() # Return a copy

    # Case 3: Valid block found, perform the swap
    
    # Extract the parts of the array for rearrangement
    # Part before the preceding zero
    prefix = input_grid[:start_index - 1] 
    # The zero element that precedes the block
    preceding_zero = np.array([input_grid[start_index - 1]]) 
    # The non-zero block itself
    non_zero_block = input_grid[start_index : end_index + 1]
    # Part after the non-zero block
    suffix = input_grid[end_index + 1:]

    # Construct the output array by concatenating parts in the new order
    # Order: prefix, non_zero_block, preceding_zero, suffix
    output_grid = np.concatenate((prefix, non_zero_block, preceding_zero, suffix))

    return output_grid
```
```python
"""
Transforms a 1D NumPy array by finding the first contiguous block of identical 
non-zero integers. If such a block exists and is preceded by a zero, 
the block is swapped with that preceding zero. If the block starts at 
index 0 or no non-zero block is found, the original array is returned.
"""

import numpy as np

def find_first_non_zero_block(arr: np.ndarray) -> tuple | None:
    """
    Finds the start and end indices of the first contiguous block of 
    identical non-zero integers in a 1D NumPy array that is preceded by a zero.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a suitable block is found.
        Returns None if no non-zero block is found, or if the first block 
        found starts at index 0 or is not preceded by a zero.
    """
    start_index = -1
    end_index = -1
    block_digit = None

    for i, digit in enumerate(arr):
        # Found a non-zero digit
        if digit != 0:
            # If this is the start of a potential block
            if start_index == -1:
                # Check if the block starts at the very beginning or not preceded by 0
                if i == 0 or arr[i - 1] != 0:
                    # If it starts at 0, it doesn't fit the swap pattern.
                    # If not preceded by 0, it doesn't fit the swap pattern.
                    # Continue searching in case there's another block later that *does* fit.
                    # We only care about the *first* block *that meets the criteria*.
                    continue 
                else: # Preceded by zero, potential block start
                     start_index = i
                     block_digit = digit
                     end_index = i # Initialize end index
            # If continuing an existing block (started in the 'else' above)
            elif digit == block_digit:
                end_index = i
            # If found a different non-zero digit, the first suitable block ended
            elif digit != block_digit and start_index != -1: 
                 break # Stop after the first suitable block is fully identified
        # Found a zero
        elif digit == 0:
            # If we were tracking a suitable block, it just ended
            if start_index != -1:
                break # Stop after the first suitable block is fully identified

    # After loop, check if a valid block was found (start_index must have been set)
    if start_index != -1:
        return start_index, end_index
    else:
        # No block preceded by zero was found
        return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block-shifting transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied, or a copy of the 
        original array if no transformation is applicable.
    """
    
    # Locate the contiguous block of identical non-zero integers preceded by zero.
    block_indices = find_first_non_zero_block(input_grid)

    # If no such block exists return the original sequence unchanged.
    if block_indices is None:
        return input_grid.copy() 

    start_index, end_index = block_indices
    
    # Identify the index of the element immediately before the block.
    preceding_zero_index = start_index - 1

    # Create a copy to avoid modifying the original input array in place
    output_grid = input_grid.copy()

    # Extract the non-zero block
    non_zero_block = output_grid[start_index : end_index + 1]
    
    # Extract the preceding zero element (as an array slice)
    preceding_zero = output_grid[preceding_zero_index : preceding_zero_index + 1] # Slice maintains array type

    # Perform the swap in the output grid:
    # Place the non-zero block starting at the preceding zero's original position
    output_grid[preceding_zero_index : preceding_zero_index + len(non_zero_block)] = non_zero_block
    
    # Place the preceding zero immediately after the shifted block
    output_grid[preceding_zero_index + len(non_zero_block) : preceding_zero_index + len(non_zero_block) + 1] = preceding_zero

    # The elements before the preceding_zero_index and after the end_index 
    # remain in their original places in the copied output_grid.

    # Return the newly constructed sequence.
    return output_grid
```
