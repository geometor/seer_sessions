
## train_1

**input:**
```
9 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 2 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 2 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 0 0 2 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 2 0
```


## train_4

**input:**
```
0 0 9 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 9 0 0 0 2 0 0 0
```


## train_5

**input:**
```
0 0 0 1 1 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 0 2 0 0 0
```


## train_6

**input:**
```
0 2 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 2 4 4 4 4 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 7
```


**output:**
```
0 0 0 0 0 0 0 0 2 7 0 0
```

Okay, let's analyze the input-output pairs to understand the transformation.

**1. Perception of Task Elements**

*   The input and output are sequences of integers, always 12 elements long in the examples.
*   The sequences contain single-digit non-negative integers, with '0' being common.
*   The number '2' appears exactly once in every input sequence and seems to play a pivotal role. Its position remains unchanged in the output.
*   Other non-zero numbers sometimes change position relative to the '2'.
*   Numbers *before* the '2' tend to shift *rightwards* towards the '2'.
*   Numbers *after* the '2' tend to shift *leftwards* towards the '2'.
*   The shift seems to happen only when there are exactly two consecutive '0's between the number and the position it moves to. The number effectively "jumps" over these two zeros.
*   Numbers adjacent to '2' (either immediately before or after) do not move.
*   If multiple numbers are eligible to move (e.g., a block like '4 4 4 4'), they maintain their relative order after the shift.
*   The processing order matters: processing elements *before* the '2' from right-to-left and elements *after* the '2' from left-to-right ensures correct placement when blocks of numbers are shifted.

**2. Facts (YAML)**


```python
import math # Standard math library, although not used in this specific logic

# Helper functions
def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    try:
        # Strip leading/trailing whitespace and split by space
        return [int(x) for x in input_str.strip().split()]
    except ValueError:
        # Handle potential errors if input contains non-numeric parts
        print(f"Error parsing input: Invalid characters found in '{input_str}'")
        return [] # Return empty list on error

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    # Convert each integer back to string and join with spaces
    return " ".join(map(str, output_list))

# Main transformation function
def transform(input_str: str) -> str:
    """
    Transforms an input sequence of integers based on specific movement rules relative to the number '2'.

    The transformation identifies the position of the number '2', which acts as a fixed pivot.
    Non-zero numbers located to the left of '2' are potentially shifted rightwards by two positions
    if the two positions immediately to their right (towards '2') are both zeros. This shifting
    process is repeated iteratively for the entire left side (from right-to-left) until no
    more such shifts are possible in a full pass.
    Similarly, non-zero numbers located to the right of '2' are potentially shifted leftwards by
    two positions if the two positions immediately to their left (towards '2') are both zeros.
    This shifting process is repeated iteratively for the entire right side (from left-to-right)
    until no more such shifts are possible in a full pass.
    Numbers immediately adjacent to '2' (at index idx2-1 or idx2+1) do not shift via this rule,
    as the rule requires two intermediate zeros.
    """

    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    if not input_list: # Handle case where parsing failed
        return "Error: Input could not be parsed"

    # Create a mutable copy of the input list to work with
    output_list = list(input_list)
    n = len(output_list) # Length of the sequence

    # Find the index of the pivot element '2'.
    # Assume '2' exists exactly once based on provided examples.
    try:
        idx2 = output_list.index(2)
    except ValueError:
        # If '2' is not found, the transformation rule cannot be applied as defined.
        # Return the original list formatted as a string.
        print("Warning: Pivot element '2' not found in the input sequence.")
        return format_output(output_list) # Or raise an error if appropriate

    # --- Process Left Side (Shift Rightwards towards '2') ---
    # This loop continues as long as swaps are being made on the left side
    while True:
        swapped_left = False
        # Iterate from right-to-left, starting from the element at index idx2-3 down to 0.
        # This ensures we check potential swaps furthest from '2' first in each pass.
        # The range ensures we only check indices i where i+2 < idx2.
        for i in range(idx2 - 3, -1, -1):
            # Check condition: element at i is non-zero, and elements at i+1, i+2 are zero
            if output_list[i] != 0 and output_list[i+1] == 0 and output_list[i+2] == 0:
                # Perform the swap: move element from i to i+2
                output_list[i], output_list[i+2] = output_list[i+2], output_list[i]
                swapped_left = True # Indicate that a change occurred in this pass

        # If a full pass completes without any swaps, the left side is stable
        if not swapped_left:
            break

    # --- Process Right Side (Shift Leftwards towards '2') ---
    # This loop continues as long as swaps are being made on the right side
    while True:
        swapped_right = False
        # Iterate from left-to-right, starting from the element at index idx2+3 up to n-1.
        # This ensures we check potential swaps furthest from '2' first in each pass.
        # The range ensures we only check indices i where i-2 > idx2.
        for i in range(idx2 + 3, n):
            # Check condition: element at i is non-zero, and elements at i-1, i-2 are zero
            if output_list[i] != 0 and output_list[i-1] == 0 and output_list[i-2] == 0:
                 # Perform the swap: move element from i to i-2
                output_list[i], output_list[i-2] = output_list[i-2], output_list[i]
                swapped_right = True # Indicate that a change occurred in this pass

        # If a full pass completes without any swaps, the right side is stable
        if not swapped_right:
            break

    # Format the final transformed list back into a space-separated string
    return format_output(output_list)

```
```python
import copy

"""
Transforms an input sequence of integers based on specific movement rules relative to the number '2'.

The transformation identifies the position of the number '2', which acts as a fixed pivot.
Non-zero numbers located to the left of '2' are potentially shifted rightwards by two positions
if the two positions immediately to their right (towards '2') are both zeros. This shifting
process is repeated iteratively for the entire left side (from right-to-left within each pass)
until no more such shifts are possible in a full pass.
Similarly, non-zero numbers located to the right of '2' are potentially shifted leftwards by
two positions if the two positions immediately to their left (towards '2') are both zeros.
This shifting process is repeated iteratively for the entire right side (from left-to-right
within each pass) until no more such shifts are possible in a full pass.
Numbers immediately adjacent to '2' (at index idx2-1 or idx2+1) do not shift via this rule,
as the rule requires two intermediate zeros.
"""


def find_pivot_index(sequence: list[int], pivot_value: int = 2) -> int:
    """Finds the index of the pivot element."""
    try:
        return sequence.index(pivot_value)
    except ValueError:
        # Handle case where pivot is not found, though examples imply it always exists.
        # Returning -1 or raising an error are options. For this task, we assume it exists.
        return -1 # Indicate not found

def shift_elements(sequence: list[int], start_index: int, end_index: int, direction: str) -> bool:
    """
    Performs one pass of shifting elements either left or right based on the rules.
    Returns True if any element was shifted, False otherwise.
    """
    swapped_in_pass = False
    if direction == 'right': # Processing left side, shifting elements right
        # Iterate right-to-left: check elements further from pivot first in this pass
        for i in range(end_index, start_index - 1, -1):
            # Check boundary condition (i+2 must be within sequence and before pivot)
            # Note: The loop range already implicitly handles some bounds.
            # Explicit check `i+2 < pivot_index` would be needed if pivot_index wasn't the boundary.
            if i + 2 < len(sequence): # Ensure index i+2 is valid
                # Check shift condition: non-zero at i, zeros at i+1, i+2
                if sequence[i] != 0 and sequence[i+1] == 0 and sequence[i+2] == 0:
                    # Perform swap
                    sequence[i], sequence[i+2] = sequence[i+2], sequence[i]
                    swapped_in_pass = True # Mark that a swap occurred
    elif direction == 'left': # Processing right side, shifting elements left
         # Iterate left-to-right: check elements further from pivot first in this pass
        for i in range(start_index, end_index + 1):
             # Check boundary condition (i-2 must be within sequence and after pivot)
             # Note: The loop range already implicitly handles some bounds.
             # Explicit check `i-2 > pivot_index` would be needed if pivot_index wasn't the boundary.
            if i - 2 >= 0: # Ensure index i-2 is valid
                # Check shift condition: non-zero at i, zeros at i-1, i-2
                if sequence[i] != 0 and sequence[i-1] == 0 and sequence[i-2] == 0:
                    # Perform swap
                    sequence[i], sequence[i-2] = sequence[i-2], sequence[i]
                    swapped_in_pass = True # Mark that a swap occurred
    return swapped_in_pass

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the shifting transformation to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers with elements shifted according to the rules.
    """
    # Create a mutable copy of the input sequence to work with
    output_sequence = copy.deepcopy(input_sequence)
    n = len(output_sequence)

    # Find the index of the pivot element '2'.
    idx2 = find_pivot_index(output_sequence, 2)

    # Handle case where pivot '2' is not found. Return original sequence.
    if idx2 == -1:
        print("Warning: Pivot element '2' not found. Returning original sequence.")
        return output_sequence

    # --- Process Left Side (Shift Rightwards towards '2') ---
    # Repeat shifting passes as long as elements are being moved on the left side.
    while True:
        # Define the range for the left side pass: from index 0 up to idx2 - 3.
        # We iterate from right-to-left within the shift_elements function.
        start_left = 0
        end_left = idx2 - 3 # The last index to check is idx2 - 3 for a rightward shift to idx2 - 1
        
        # Ensure valid range before calling shift_elements
        if end_left >= start_left:
             # Perform a pass of rightward shifts
            swapped = shift_elements(output_sequence, start_left, end_left, 'right')
            # If no elements were swapped in this pass, the left side is stable.
            if not swapped:
                break
        else:
             # No elements to process on the left side that meet the distance criteria
             break


    # --- Process Right Side (Shift Leftwards towards '2') ---
    # Repeat shifting passes as long as elements are being moved on the right side.
    while True:
        # Define the range for the right side pass: from index idx2 + 3 up to n - 1.
        # We iterate from left-to-right within the shift_elements function.
        start_right = idx2 + 3 # The first index to check is idx2 + 3 for a leftward shift to idx2 + 1
        end_right = n - 1

        # Ensure valid range before calling shift_elements
        if start_right <= end_right:
            # Perform a pass of leftward shifts
            swapped = shift_elements(output_sequence, start_right, end_right, 'left')
             # If no elements were swapped in this pass, the right side is stable.
            if not swapped:
                break
        else:
            # No elements to process on the right side that meet the distance criteria
            break


    # Return the modified sequence
    return output_sequence
```
```python
import numpy as np
# import copy # Not strictly needed as np.copy() is used.

"""
Transforms an input sequence of integers (represented as a NumPy array) based on specific movement rules relative to the number '2'.

The transformation identifies the position of the number '2', which acts as a fixed pivot.
Non-zero numbers located to the left of '2' are potentially shifted rightwards by two positions
if the two positions immediately to their right (towards '2') are both zeros. This shifting
process is repeated iteratively for the entire left side (from right-to-left within each pass)
until no more such shifts are possible in a full pass.
Similarly, non-zero numbers located to the right of '2' are potentially shifted leftwards by
two positions if the two positions immediately to their left (towards '2') are both zeros.
This shifting process is repeated iteratively for the entire right side (from left-to-right
within each pass) until no more such shifts are possible in a full pass.
Numbers immediately adjacent to '2' (at index idx2-1 or idx2+1) or separated by one zero
do not meet the shift conditions (i.e., the rule requires checking i+1, i+2 or i-1, i-2).
The pivot '2' itself never moves.
"""

def find_pivot_index(sequence: np.ndarray, pivot_value: int = 2) -> int:
    """
    Finds the index of the first occurrence of the pivot element in the sequence.

    Args:
        sequence: The input NumPy array.
        pivot_value: The integer value to find (default is 2).

    Returns:
        The index of the first occurrence of the pivot value, or -1 if not found.
    """
    indices = np.where(sequence == pivot_value)[0]
    if len(indices) == 0:
        # Handle case where pivot is not found.
        # print(f"Warning: Pivot element '{pivot_value}' not found.") # Keep console clean
        return -1 # Indicate not found
    # Examples imply exactly one pivot, but if multiple exist, use the first one.
    return indices[0]

def shift_elements(sequence: np.ndarray, start_index: int, end_index: int, direction: str) -> bool:
    """
    Performs one pass of shifting elements either left or right based on the rules.
    Modifies the sequence in place.

    Args:
        sequence: The NumPy array to modify.
        start_index: The starting index for the pass (inclusive).
        end_index: The ending index for the pass (inclusive).
        direction: 'right' for shifting elements on the left side towards the pivot,
                   'left' for shifting elements on the right side towards the pivot.

    Returns:
        True if any element was shifted during this pass, False otherwise.
    """
    swapped_in_pass = False
    n = len(sequence)
    if direction == 'right': # Processing left side, shifting elements right
        # Iterate right-to-left: checks elements further from pivot first in this pass
        for i in range(end_index, start_index - 1, -1):
            # Check boundary condition: i+2 must be a valid index within the array
            if i + 2 < n:
                # Check shift condition: non-zero at i, zeros at i+1, i+2
                if sequence[i] != 0 and sequence[i+1] == 0 and sequence[i+2] == 0:
                    # Perform swap using NumPy tuple assignment for swapping
                    sequence[i], sequence[i+2] = sequence[i+2], sequence[i]
                    swapped_in_pass = True # Mark that a swap occurred
    elif direction == 'left': # Processing right side, shifting elements left
         # Iterate left-to-right: checks elements further from pivot first in this pass
        for i in range(start_index, end_index + 1):
             # Check boundary condition: i-2 must be a valid index within the array
            if i - 2 >= 0:
                # Check shift condition: non-zero at i, zeros at i-1, i-2
                if sequence[i] != 0 and sequence[i-1] == 0 and sequence[i-2] == 0:
                    # Perform swap using NumPy tuple assignment for swapping
                    sequence[i], sequence[i-2] = sequence[i-2], sequence[i]
                    swapped_in_pass = True # Mark that a swap occurred
    return swapped_in_pass

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the iterative shifting transformation to the input NumPy array.

    Args:
        input_sequence: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with elements shifted according to the rules.
    """
    # Initialize output_sequence as a mutable copy of the input
    output_sequence = input_sequence.copy()
    n = len(output_sequence)

    # Find the index of the pivot element '2'.
    idx2 = find_pivot_index(output_sequence, 2)

    # If pivot '2' is not found, return the original sequence copy as per rule assumption.
    if idx2 == -1:
        # print("Warning: Pivot element '2' not found. Returning original sequence.") # Keep console clean
        return output_sequence # Return the unmodified copy

    # --- Process Left Side (Shift Rightwards towards '2') ---
    # Repeat shifting passes until no more swaps occur on the left side.
    while True:
        # Define the range for potential starting positions 'i' on the left side pass.
        # The rightmost element that could shift right is at idx2 - 3.
        start_left = 0
        end_left = idx2 - 3

        # Only proceed if there are elements to check (range is valid)
        if end_left >= start_left:
             # Perform one pass of rightward shifts.
             # The shift_elements function iterates right-to-left (end_left down to start_left).
             # It modifies output_sequence in place.
            swapped = shift_elements(output_sequence, start_left, end_left, 'right')
            # If no elements were swapped in this pass, the left side has reached stability.
            if not swapped:
                break
        else:
             # No elements on the left side are far enough from '2' to potentially shift.
             break


    # --- Process Right Side (Shift Leftwards towards '2') ---
    # Repeat shifting passes until no more swaps occur on the right side.
    while True:
        # Define the range for potential starting positions 'i' on the right side pass.
        # The leftmost element that could shift left is at idx2 + 3.
        start_right = idx2 + 3
        end_right = n - 1

        # Only proceed if there are elements to check (range is valid)
        if start_right <= end_right:
            # Perform one pass of leftward shifts.
            # The shift_elements function iterates left-to-right (start_right up to end_right).
            # It modifies output_sequence in place.
            swapped = shift_elements(output_sequence, start_right, end_right, 'left')
             # If no elements were swapped in this pass, the right side has reached stability.
            if not swapped:
                break
        else:
            # No elements on the right side are far enough from '2' to potentially shift.
            break

    # Return the modified sequence
    return output_sequence
```
