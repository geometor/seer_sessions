```python
import numpy as np

def transform(input_list):
    """
    Shifts all non-zero elements in a 1D list two positions to the right.

    Args:
      input_list: A list of integers.

    Returns:
      A new list of integers with non-zero elements shifted right by 2 positions.
    """

    # Get the length of the input list
    n = len(input_list)

    # Initialize an output list of the same length, filled with zeros.
    output_list = [0] * n

    # Iterate through the input list
    # We only need to check up to index n-3 because elements at n-2 and n-1
    # would shift out of bounds if they were non-zero.
    for i in range(n):
        # Get the current element
        element = input_list[i]

        # Check if the element is non-zero
        if element != 0:
            # Calculate the target index for the shift
            target_index = i + 2

            # Check if the target index is within the bounds of the list
            if target_index < n:
                # Place the non-zero element into the output list at the shifted position
                output_list[target_index] = element

    # Return the modified output list
    return output_list

```