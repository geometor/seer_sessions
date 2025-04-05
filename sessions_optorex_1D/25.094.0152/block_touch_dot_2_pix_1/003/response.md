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