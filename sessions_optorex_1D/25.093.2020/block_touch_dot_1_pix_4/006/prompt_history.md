
## train_1

**input:**
```
0 3 3 3 3 3 3 3 3 2 0 0
```


**output:**
```
0 3 3 3 3 3 3 3 3 2 0 0
```


## train_2

**input:**
```
0 0 0 0 0 6 6 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 6 2 0 0 0 0
```


## train_3

**input:**
```
2 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
2 3 3 3 3 3 3 0 0 0 0 0
```


## train_4

**input:**
```
5 5 5 5 5 5 5 5 5 5 2 0
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 2 0
```


## train_5

**input:**
```
0 0 0 2 4 4 4 4 4 0 0 0
```


**output:**
```
0 0 0 2 4 4 4 4 4 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 9 9 9 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 0 2
```


## train_7

**input:**
```
4 0 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 2 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves transforming a sequence of single-digit integers into another sequence of the same length.
Observing the training examples:
- Most examples (train_1 to train_5) show the output being identical to the input.
- train_6 and train_7 show a change.
    - In train_6: `... 0 0 9 ...` becomes `... 0 0 0 9 ...`. It looks like a `0` that was immediately followed by a non-zero number (`9`) has moved one position to the left, swapping with its left neighbor (which was also `0`).
    - In train_7: `4 0 2 ...` becomes `0 4 2 ...`. Here, a `0` that was immediately followed by a non-zero number (`2`) has moved one position to the left, swapping with its left neighbor (`4`).
- The common pattern in the modified examples (train_6, train_7) seems to be locating the *first* instance of a `0` that is immediately followed by a non-zero digit. If such a `0` exists and it's not the very first element in the sequence, it swaps positions with the element immediately to its left.
- In the examples where no change occurs (train_1 to train_5), either there is no `0` followed by a non-zero digit (train_3, train_4), or the first such `0` is already at the beginning of the sequence (train_1), or swapping it with its left neighbor results in no visible change because the neighbor is also `0` (train_2, train_5).

## Facts


```yaml
objects:
  - name: sequence
    type: list of integers
    description: The input and output data structures.
  - name: element
    type: integer
    description: Individual numbers within the sequence.
properties:
  - object: element
    name: value
    type: integer
    description: The numerical value of the element (0-9).
  - object: element
    name: index
    type: integer
    description: The position of the element within the sequence (zero-based).
  - object: element
    name: is_zero
    type: boolean
    description: True if the element's value is 0.
  - object: element
    name: is_non_zero
    type: boolean
    description: True if the element's value is not 0.
relationships:
  - type: adjacency
    description: Elements can be adjacent (left neighbor, right neighbor) within the sequence.
    properties:
      - element_1: index i
      - element_2: index i+1 (right neighbor)
      - element_3: index i-1 (left neighbor)
actions:
  - name: scan
    description: Iterate through the sequence elements from left to right.
  - name: find_pattern
    description: Locate the first index `i` where element `i` is 0 and element `i+1` is non-zero.
    condition: Requires checking pairs of adjacent elements.
  - name: swap
    description: Exchange the positions of two elements in the sequence.
    condition: Applicable if the pattern is found at index `i > 0`. Swaps elements at `i` and `i-1`.
  - name: no_change
    description: The sequence remains unaltered.
    condition: Applicable if the pattern is not found, or if the pattern is found at index `i = 0`.
```


## Natural Language Program

1.  Iterate through the input sequence from the first element up to the second-to-last element. Let the current index be `i`.
2.  At each index `i`, check if the element at `i` is `0` AND the element at the next index `i+1` is non-zero.
3.  If this condition is met for the first time at index `i`:
    a.  Check if `i` is greater than 0 (i.e., the found `0` is not the very first element of the sequence).
    b.  If `i > 0`, swap the element at index `i` with the element at index `i-1`.
    c.  Stop iterating, as the transformation involves only the *first* occurrence of the pattern.
4.  If the condition in step 2 is never met, or if it's met only at index `i = 0`, make no changes to the sequence.
5.  Output the resulting sequence.
```python
import math

"""
Transforms a sequence of integers based on a specific pattern.

The rule is:
1. Find the first index `i` where the element `seq[i]` is 0 and the next element `seq[i+1]` is non-zero.
2. If such an index `i` is found and `i` is greater than 0 (not the first element), swap the element at index `i` (the zero) with the element at index `i-1` (its left neighbor).
3. Only the first occurrence of this pattern triggers the swap.
4. If the pattern is not found, or if it's found at index `i = 0`, the sequence remains unchanged.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    sequence = parse_input(input_str)
    
    # Create a mutable copy to potentially modify
    output_sequence = list(sequence)
    n = len(output_sequence)
    
    # Find the index of the first pattern occurrence
    target_index = -1
    for i in range(n - 1):
        # Check if element i is 0 AND element i+1 is non-zero
        if output_sequence[i] == 0 and output_sequence[i+1] != 0:
            target_index = i
            # Stop searching after finding the first occurrence
            break
            
    # Apply the swap rule if the pattern was found and not at the beginning
    if target_index != -1:
        # Check if the index is greater than 0
        if target_index > 0:
            # Swap the element at target_index with the element at target_index - 1
            output_sequence[target_index], output_sequence[target_index - 1] = \
                output_sequence[target_index - 1], output_sequence[target_index]
                
    # Format the resulting list back into a string
    return format_output(output_sequence)

# Example usage with provided train cases (for verification):
# train_1_input = "0 3 3 3 3 3 3 3 3 2 0 0"
# train_1_output = transform(train_1_input) # Expected: "0 3 3 3 3 3 3 3 3 2 0 0" (i=0, no swap)
# print(f"Train 1 Output: {train_1_output}")

# train_6_input = "0 0 0 0 0 0 9 9 9 0 0 2"
# train_6_output = transform(train_6_input) # Expected by NL program: "0 0 0 0 0 0 9 9 9 0 0 2" (i=5, swap 0 and 0)
# print(f"Train 6 Output: {train_6_output}") # Note: This differs from the provided example output.

# train_7_input = "4 0 2 0 0 0 0 0 0 0 0 0"
# train_7_output = transform(train_7_input) # Expected: "0 4 2 0 0 0 0 0 0 0 0 0" (i=1, swap 0 and 4)
# print(f"Train 7 Output: {train_7_output}")

```
```python
import math # Although not used in the final logic, keeping standard imports
import numpy as np # Assuming input might be numpy array based on previous errors

"""
Transforms a sequence of integers based on the following rule:
1. Find the first contiguous block of one or more non-zero numbers in the sequence.
2. If no such block exists, the sequence remains unchanged.
3. If a block is found (starting at `start_index`, ending at `end_index`), search the sequence *after* this block (from index `end_index + 1` onwards).
4. Find the first index `i` in this subsequent part where the element `sequence[i]` is 0 and the next element `sequence[i+1]` is non-zero.
5. If no such index `i` is found after the block, the sequence remains unchanged.
6. If such an index `i` is found, move the element `sequence[i]` (the zero) to the `start_index` of the non-zero block found in step 1. The elements originally from `start_index` to `i-1` are shifted one position to the right.
7. Only the first non-zero block and the first qualifying zero after it trigger the transformation.
"""

def parse_input(input_data) -> list[int]:
    """Parses the input into a list of integers."""
    if isinstance(input_data, str):
        return [int(x) for x in input_data.split()]
    elif isinstance(input_data, np.ndarray):
        # Assuming a 1D array or the first row if 2D
        if input_data.ndim == 2:
             input_list = input_data[0].tolist()
        elif input_data.ndim == 1:
             input_list = input_data.tolist()
        else:
             raise ValueError("Input data must be a string or a 1D/2D numpy array.")
        return [int(x) for x in input_list] # Ensure elements are integers
    elif isinstance(input_data, list):
        return [int(x) for x in input_data] # Ensure elements are integers
    else:
        raise TypeError(f"Unsupported input type: {type(input_data)}")


def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_first_non_zero_block(sequence: list[int]) -> tuple[int, int]:
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.

    Args:
        sequence: The list of integers.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    n = len(sequence)

    for i in range(n):
        if sequence[i] != 0:
            start_index = i
            break # Found the start of the first block

    if start_index == -1:
        return -1, -1 # No non-zero numbers found

    # Find the end of this block
    end_index = start_index
    for i in range(start_index + 1, n):
        if sequence[i] != 0:
            end_index = i
        else:
            break # End of the block reached

    return start_index, end_index

def find_first_zero_pattern_after(sequence: list[int], start_scan_index: int) -> int:
    """
    Finds the index of the first '0 followed by non-zero' pattern starting from a given index.

    Args:
        sequence: The list of integers.
        start_scan_index: The index from which to start scanning (inclusive).

    Returns:
        The index `i` where sequence[i] == 0 and sequence[i+1] != 0,
        or -1 if no such pattern is found from the start_scan_index onwards.
    """
    n = len(sequence)
    for i in range(start_scan_index, n - 1):
        if sequence[i] == 0 and sequence[i+1] != 0:
            return i # Found the pattern
    return -1 # Pattern not found

def transform(input_data) -> str:
    """
    Applies the transformation rule to the input sequence.
    """
    # Parse input into a list of integers
    sequence = parse_input(input_data)
    n = len(sequence)

    # Step 1 & 2: Find the first non-zero block
    block_start_index, block_end_index = find_first_non_zero_block(sequence)

    if block_start_index == -1:
        # No non-zero block found, return original sequence
        return format_output(sequence)

    # Step 3 & 4 & 5: Find the first '0 followed by non-zero' after the block
    scan_start = block_end_index + 1
    zero_to_move_index = find_first_zero_pattern_after(sequence, scan_start)

    if zero_to_move_index == -1:
        # No qualifying zero found after the block, return original sequence
        return format_output(sequence)

    # Step 6 & 7: Perform the move operation
    # Create a mutable copy
    output_sequence = list(sequence)
    # Remove the zero from its original position
    zero_value = output_sequence.pop(zero_to_move_index)
    # Insert the zero at the start of the non-zero block
    output_sequence.insert(block_start_index, zero_value)

    # Step 8: Format and return the modified sequence
    return format_output(output_sequence)

```
```python
import math # common libraries are available
import numpy as np # common libraries are available

"""
Transforms a sequence of integers based on the following rule:
1. Find the start and end indices (`block_start_index`, `block_end_index`) of the first contiguous block of non-zero numbers.
2. If no non-zero block exists, the sequence remains unchanged.
3. Search the sequence *after* this block (from index `block_end_index + 1` onwards) for the first index `i` where `sequence[i]` is 0 and `sequence[i+1]` is non-zero.
4. If no such index `i` is found after the block, the sequence remains unchanged.
5. If such an index `i` is found, move the element `sequence[i]` (the zero) to the `block_start_index`. The elements originally from `block_start_index` to `i-1` are shifted one position to the right to accommodate the inserted zero.
6. Only the first non-zero block and the first qualifying zero found after it trigger this transformation.
"""

def parse_input(input_data) -> list[int]:
    """Parses the input into a list of integers."""
    # Handle potential numpy array input specifically
    if isinstance(input_data, np.ndarray):
        # Flatten if multi-dimensional, though examples suggest 1D/row focus
        input_list = input_data.flatten().tolist()
    # Handle string input
    elif isinstance(input_data, str):
        # Split the string by spaces and convert each part to an integer
        input_list = [int(x) for x in input_data.split()]
    # Handle list input (ensure elements are integers)
    elif isinstance(input_data, list):
        input_list = [int(x) for x in input_data]
    else:
        raise TypeError(f"Unsupported input type: {type(input_data)}")
    return input_list

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_first_non_zero_block(sequence: list[int]) -> tuple[int, int]:
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.

    Args:
        sequence: The list of integers.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    n = len(sequence)

    # Find the start of the first block
    for i in range(n):
        if sequence[i] != 0:
            start_index = i
            break

    # If no non-zero number was found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of this block
    end_index = start_index
    for i in range(start_index + 1, n):
        if sequence[i] != 0:
            end_index = i
        else:
            # The block ends at the previous index
            break

    return start_index, end_index

def find_first_zero_pattern_after(sequence: list[int], start_scan_index: int) -> int:
    """
    Finds the index 'i' of the first '0 followed by non-zero' pattern,
    starting the scan from a given index.

    Args:
        sequence: The list of integers.
        start_scan_index: The index from which to start scanning (inclusive).

    Returns:
        The index `i` where sequence[i] == 0 and sequence[i+1] != 0,
        or -1 if no such pattern is found from the start_scan_index onwards.
    """
    n = len(sequence)
    # Iterate from the start scan index up to the second-to-last element
    for i in range(start_scan_index, n - 1):
        # Check the pattern: current element is 0, next is non-zero
        if sequence[i] == 0 and sequence[i+1] != 0:
            return i # Found the pattern at index i

    # If the loop completes without finding the pattern
    return -1

def transform(input_data) -> str:
    """
    Applies the transformation rule to the input sequence.
    Input can be a space-separated string, a list of ints, or a numpy array.
    Output is a space-separated string.
    """
    # 1. Parse Input
    sequence = parse_input(input_data)
    n = len(sequence)
    # Create a mutable copy for potential modification
    output_sequence = list(sequence)

    # 2. Identify First Non-Zero Block
    block_start_index, block_end_index = find_first_non_zero_block(output_sequence)

    # 3. Handle No Block Case
    if block_start_index == -1:
        # If no non-zero block found, return the original sequence formatted as string
        return format_output(output_sequence)

    # 4. Search for Pattern After Block
    # Start searching from the index immediately after the block ends
    scan_start_index = block_end_index + 1
    zero_to_move_index = find_first_zero_pattern_after(output_sequence, scan_start_index)

    # 5. Handle No Pattern Case
    if zero_to_move_index == -1:
        # If the '0 followed by non-zero' pattern is not found after the block,
        # return the original sequence formatted as string
        return format_output(output_sequence)

    # 6. Perform Move Operation
    # Only proceed if both the block and the pattern were found
    # a. Temporarily store and remove the zero from its original position
    zero_value = output_sequence.pop(zero_to_move_index)
    # b. Insert the stored zero value at the start index of the non-zero block
    output_sequence.insert(block_start_index, zero_value)

    # 7. Output Result
    # Format the modified list into a space-separated string
    return format_output(output_sequence)

```
