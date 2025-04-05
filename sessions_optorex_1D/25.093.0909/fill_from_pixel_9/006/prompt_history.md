
## train_1

**input:**
```
0 7 1 1 1 0 0 0 0 0 0 0
```


**output:**
```
7 7 1 1 1 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 8 4 4 4 0 0 0
```


**output:**
```
8 8 8 8 8 8 4 4 4 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 5 7 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 7 7 7 7 7 7
```


## train_4

**input:**
```
0 0 0 1 1 1 1 1 1 8 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 8 8 8
```


## train_5

**input:**
```
0 0 0 0 7 4 4 4 0 0 0 0
```


**output:**
```
7 7 7 7 7 4 4 4 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 7 7 7 7 7 8 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 7 8 8
```


## train_7

**input:**
```
0 3 9 9 9 9 9 9 0 0 0 0
```


**output:**
```
3 3 9 9 9 9 9 9 0 0 0 0
```

Okay, let's break down the transformation.

**Perception of Elements:**

The input and output are both lists (or sequences) of single-digit integers, always of length 12 in the provided examples. The core transformation involves changing some, but not all, of the zero ('0') elements in the input sequence to non-zero digits. The non-zero digits present in the input sequence are preserved in the output sequence at their original positions. The key action seems to be the "spreading" or "filling" of certain non-zero digits into adjacent zero digits. Notably, this spreading only seems to originate from non-zero digits that appear as a block of length one (i.e., a single instance of that digit surrounded by different digits or zeros/boundaries). Non-zero digits that are part of a longer contiguous block of the same digit do not spread. The spreading stops when it encounters another non-zero digit or the boundary of the sequence.

**YAML Facts:**


```yaml
objects:
  - name: sequence
    type: list of integers
    properties:
      - length: 12 (fixed in examples)
      - elements: single digits (0-9)
  - name: element
    type: integer
    properties:
      - value: 0-9
      - index: position in the sequence (0-11)
  - name: block
    type: contiguous subsequence
    properties:
      - value: the digit repeated in the block (can be 0 or non-zero)
      - length: number of elements in the block
      - start_index: index of the first element
      - end_index: index of the last element
  - name: singular_non_zero_block
    type: block
    constraints:
      - value != 0
      - length == 1
  - name: zero_block
    type: block
    constraints:
      - value == 0

actions:
  - name: identify_blocks
    description: Segment the input sequence into contiguous blocks of identical digits.
  - name: identify_singular_non_zero_blocks
    description: Find all blocks identified in the previous step that have a non-zero value and a length of 1.
  - name: identify_adjacent_zero_blocks
    description: For each singular non_zero block, find any immediately adjacent zero blocks (left or right).
  - name: fill_zeros
    description: Modify the sequence by replacing the zeros in the adjacent zero blocks with the value of the corresponding singular non_zero block. The filling extends outwards from the singular block until a non-zero digit or the sequence boundary is encountered.

relationships:
  - type: adjacency
    description: Relationship between elements or blocks based on their indices in the sequence (e.g., element at index i is adjacent to elements at i-1 and i+1).
  - type: boundary_condition
    description: Checks if a block or element is at the start (index 0) or end (index 11) of the sequence.
```


**Natural Language Program:**

1.  Initialize the output sequence as a copy of the input sequence.
2.  Iterate through the input sequence from left to right (index `i` from 0 to length-1).
3.  For each element at index `i`, check if it represents a "singular non-zero block". This condition is met if:
    *   The element `input[i]` is not zero.
    *   AND ( `i` is 0 OR `input[i-1]` is not equal to `input[i]` )
    *   AND ( `i` is the last index OR `input[i+1]` is not equal to `input[i]` )
4.  If the element at index `i` meets the criteria for a singular non-zero block with value `V = input[i]`:
    a.  **Spread Left:** Check the element to the left (`input[i-1]`). If `i > 0` and `input[i-1]` is 0, then iterate backwards from index `j = i-1` towards the beginning of the sequence: as long as `j >= 0` and `input[j]` is 0, set `output[j] = V`. Stop if a non-zero element is encountered or the beginning of the sequence is reached.
    b.  **Spread Right:** Check the element to the right (`input[i+1]`). If `i < length-1` and `input[i+1]` is 0, then iterate forwards from index `k = i+1` towards the end of the sequence: as long as `k < length` and `input[k]` is 0, set `output[k] = V`. Stop if a non-zero element is encountered or the end of the sequence is reached.
5.  After checking all elements in the input sequence, the modified output sequence contains the final result.
```python
"""
Transforms a sequence of digits based on the following rule:
Identify non-zero digits that appear singularly (i.e., not adjacent to the same digit).
For each such singular non-zero digit, "spread" its value into adjacent zero ('0') elements
both to the left and to the right. The spreading continues until it encounters another
non-zero digit or the boundary of the sequence. The original non-zero digits, including
those that were part of longer blocks and those that were singular, retain their original
positions and values in the output. Only the zero elements adjacent to singular non-zero
elements are potentially modified.
"""

import copy

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    # Initialize output_sequence as a copy of the input to modify
    # Use the input_sequence for checks to ensure spreading only happens into original zeros
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through each element of the input sequence
    for i in range(n):
        current_val = input_sequence[i]

        # Check if the current element is non-zero
        if current_val != 0:
            # Determine if this non-zero element is singular
            # Check left boundary or if the left neighbor is different
            is_singular_left = (i == 0 or input_sequence[i-1] != current_val)
            # Check right boundary or if the right neighbor is different
            is_singular_right = (i == n - 1 or input_sequence[i+1] != current_val)

            # If the element is singular (both left and right conditions met)
            if is_singular_left and is_singular_right:
                # Spread the value (current_val) to the left into original zeros
                j = i - 1
                # Continue leftwards as long as we are within bounds and encounter original zeros
                while j >= 0 and input_sequence[j] == 0:
                    output_sequence[j] = current_val
                    j -= 1

                # Spread the value (current_val) to the right into original zeros
                k = i + 1
                # Continue rightwards as long as we are within bounds and encounter original zeros
                while k < n and input_sequence[k] == 0:
                    output_sequence[k] = current_val
                    k += 1

    # Return the modified sequence
    return output_sequence

# Helper function to parse the input string format if needed (outside the core transform)
def parse_input(input_str):
    return [int(x) for x in input_str.split()]

# Helper function to format the output list back to string if needed (outside the core transform)
def format_output(output_list):
    return " ".join(map(str, output_list))

```
```python
"""
Transforms a sequence of digits based on the following rule:
Identify non-zero digits in the input sequence that appear singularly, meaning their immediate
neighbors (if they exist) are different digits. For each such singular non-zero digit, "spread"
its value into adjacent zero ('0') elements in the sequence, both to the left and to the right.
The spreading from a singular digit continues outwards until it encounters another non-zero digit
(from the original input sequence) or the boundary of the sequence. The original positions and
values of all non-zero digits from the input sequence are preserved in the output sequence.
Zeros that are not adjacent to a singular non-zero digit, or are blocked by another non-zero
digit, remain zero. The process considers the original input sequence for identifying singular
digits and determining where spreading stops.
"""

import copy

def is_singular(sequence, index):
    """
    Checks if the element at the given index in the sequence is a singular non-zero element.

    Args:
        sequence: The input list of integers.
        index: The index of the element to check.

    Returns:
        True if the element is singular and non-zero, False otherwise.
    """
    n = len(sequence)
    current_val = sequence[index]

    # Must be non-zero
    if current_val == 0:
        return False

    # Check left neighbor (or boundary)
    is_singular_left = (index == 0 or sequence[index - 1] != current_val)

    # Check right neighbor (or boundary)
    is_singular_right = (index == n - 1 or sequence[index + 1] != current_val)

    return is_singular_left and is_singular_right

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    # Ensure input is a list, not a numpy array to avoid potential type issues
    # seen in testing environments. If it might be numpy, convert it.
    # Example conversion (add import numpy as np if needed):
    # if not isinstance(input_sequence, list):
    #    input_sequence = input_sequence.tolist() # Assuming it's a 1D numpy array

    # Initialize output_sequence as a copy of the input.
    # Modifications happen here, but checks use the original input_sequence.
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through each element of the original input sequence
    for i in range(n):
        current_val = input_sequence[i]

        # Check if the element at index i is singular based on the original sequence
        if is_singular(input_sequence, i):
            # If singular, spread its value left and right into original zeros

            # Spread Left
            j = i - 1
            # Continue leftwards as long as we are within bounds AND the element
            # in the ORIGINAL sequence at index j is 0.
            while j >= 0 and input_sequence[j] == 0:
                output_sequence[j] = current_val # Modify the output sequence
                j -= 1

            # Spread Right
            k = i + 1
            # Continue rightwards as long as we are within bounds AND the element
            # in the ORIGINAL sequence at index k is 0.
            while k < n and input_sequence[k] == 0:
                output_sequence[k] = current_val # Modify the output sequence
                k += 1

    # Return the modified sequence
    return output_sequence

```
```python
"""
Transforms a sequence of digits by identifying singular non-zero elements and
spreading their value into adjacent zeros. A non-zero element is singular if
its immediate neighbors (if they exist) have different values. The spreading
occurs outwards from the singular element, replacing zeros in a copy of the
sequence, until a non-zero element (from the original sequence) or the
sequence boundary is reached. Non-singular non-zero elements and original
zeros not affected by spreading remain unchanged.
"""

import copy
import numpy as np # Import numpy as the error indicated input might be numpy array

def is_singular(sequence, index, n):
    """
    Checks if the element at the given index in the sequence is a singular non-zero element.

    Args:
        sequence: The input list or 1D array of integers.
        index: The index of the element to check.
        n: The length of the sequence.

    Returns:
        True if the element is singular and non-zero, False otherwise.
    """
    current_val = sequence[index]

    # Must be non-zero to be considered for spreading
    if current_val == 0:
        return False

    # Check left neighbor (or boundary condition)
    # Singular if it's the first element OR the element to the left is different
    is_singular_left = (index == 0 or sequence[index - 1] != current_val)

    # Check right neighbor (or boundary condition)
    # Singular if it's the last element OR the element to the right is different
    is_singular_right = (index == n - 1 or sequence[index + 1] != current_val)

    # Must satisfy both conditions to be singular
    return is_singular_left and is_singular_right

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or 1D numpy array of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    # Ensure input is a standard Python list to avoid potential numpy ambiguity errors
    # This handles both list and numpy array inputs safely.
    if isinstance(input_sequence, np.ndarray):
        # Convert numpy array to list
        original_list = input_sequence.tolist()
    else:
        # Assume it's already list-like, create a copy
        original_list = list(input_sequence) # Ensure it's a list

    # Create a deep copy of the list to modify for the output
    output_list = copy.deepcopy(original_list)
    n = len(original_list)

    # Iterate through each index of the original sequence
    for i in range(n):
        # Check if the element at index i in the original sequence is singular
        if is_singular(original_list, i, n):
            # Get the value of the singular element
            spread_value = original_list[i]

            # Spread the value to the left into original zeros
            j = i - 1
            # Continue leftwards as long as we are within bounds AND
            # the element in the ORIGINAL sequence at index j is 0.
            while j >= 0 and original_list[j] == 0:
                output_list[j] = spread_value # Modify the output list
                j -= 1 # Move to the next element to the left

            # Spread the value to the right into original zeros
            k = i + 1
            # Continue rightwards as long as we are within bounds AND
            # the element in the ORIGINAL sequence at index k is 0.
            while k < n and original_list[k] == 0:
                output_list[k] = spread_value # Modify the output list
                k += 1 # Move to the next element to the right

    # Return the modified list
    return output_list
```
