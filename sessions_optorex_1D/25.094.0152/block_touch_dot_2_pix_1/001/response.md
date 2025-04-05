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