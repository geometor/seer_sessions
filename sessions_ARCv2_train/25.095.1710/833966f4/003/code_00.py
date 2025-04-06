import math # Included for potential use, though not strictly necessary for the current logic.
from typing import List

"""
Processes a list of integers by conditionally swapping adjacent pairs at specific intervals.
It iterates through the list considering pairs starting at indices 0, 3, 6, ....
For pairs starting at indices corresponding to an even "group" index (p = i // 3 is 0, 2, 4, ...),
it swaps the pair (at indices i and i+1) if the element at index i is greater than the element at index i+1.
For pairs starting at indices corresponding to an odd "group" index (p = i // 3 is 1, 3, 5, ...),
it swaps the pair (at indices i and i+1) if the element at index i is less than the element at index i+1.
Elements at indices 2, 5, 8, ... are not directly involved in swaps but maintain their relative position
with respect to the (potentially swapped) pairs around them.
The function takes a list of integers and returns a new list with the transformed sequence.
"""

def transform(input_list: List[int]) -> List[int]:
    """
    Applies a conditional swapping rule to adjacent pairs of numbers
    at specific indices in the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A list containing the transformed sequence of integers.
    """
    # Create a mutable copy of the input list to store the results
    # This prevents modification of the original list if it's used elsewhere.
    output_list = list(input_list)
    n = len(output_list)

    # Iterate through the list with a step of 3, focusing on the starting index 'i' of potential pairs
    # The loop continues as long as 'i' is a valid index within the list.
    i = 0
    while i < n:
        # Check if the next index 'i + 1' is also within the list bounds to form a valid pair
        if i + 1 < n:
            # Calculate the 'pair group' index (p) based on the starting index 'i'
            # p = 0 for indices (0, 1)
            # p = 1 for indices (3, 4)
            # p = 2 for indices (6, 7), and so on.
            pair_group_index = i // 3

            # Apply the comparison and swap logic based on whether 'p' is even or odd
            if pair_group_index % 2 == 0:
                # Even pair groups (p = 0, 2, 4, ...): Swap if the first element is greater than the second
                if output_list[i] > output_list[i+1]:
                    # Perform the swap
                    output_list[i], output_list[i+1] = output_list[i+1], output_list[i]
            else:
                # Odd pair groups (p = 1, 3, 5, ...): Swap if the first element is less than the second
                if output_list[i] < output_list[i+1]:
                    # Perform the swap
                    output_list[i], output_list[i+1] = output_list[i+1], output_list[i]

        # Increment the index by 3 to move to the start of the next potential pair group
        # This naturally skips indices 2, 5, 8, ... as starting points for comparisons.
        i += 3

    # Return the modified list
    return output_list
