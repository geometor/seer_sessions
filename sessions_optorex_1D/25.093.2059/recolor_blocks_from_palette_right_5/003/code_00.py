import collections
import numpy as np
from typing import List, Tuple

"""
Transforms a sequence of 12 integers based on the following rules:
1. Accept the input as a sequence (list or array) of 12 integers.
2. Identify the value of the first element as key1 and the value of the second element as key2.
3. Initialize the output sequence as a copy of the input sequence.
4. Scan the input sequence from the beginning (index 0) to the end (index 11) to find the start index and length of all contiguous subsequences consisting solely of the number 5. Record these subsequences (their start index and length) in the order they are found.
5. If at least one subsequence of 5s was found:
    * Retrieve the start index and length of the *first* recorded subsequence.
    * In the output sequence, replace the elements from that start index for that length with the value key1.
6. If at least two subsequences of 5s were found:
    * Retrieve the start index and length of the *second* recorded subsequence.
    * In the output sequence, replace the elements from that start index for that length with the value key2.
7. Return the modified output sequence.
"""

def find_runs(sequence: List[int], value: int) -> List[Tuple[int, int]]:
    """
    Finds the start index and length of all contiguous runs of a specific value.

    Args:
        sequence: The list of integers to search within.
        value: The integer value to find runs of.

    Returns:
        A list of tuples, where each tuple contains (start_index, length)
              for a run of the specified value.
    """
    runs = []
    i = 0
    n = len(sequence)
    while i < n:
        if sequence[i] == value:
            start_index = i
            # Find the end of the run
            while i < n and sequence[i] == value:
                i += 1
            length = i - start_index
            runs.append((start_index, length))
        else:
            # Move to the next element if not the target value
            i += 1
    return runs

def transform(input_sequence) -> List[int]:
    """
    Applies the sequence transformation rule.

    Args:
        input_sequence: A sequence (list or numpy array) of 12 integers.

    Returns:
        A list containing the transformed sequence of 12 integers.
    """
    # Ensure input is a list
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assuming it's already list-like if not ndarray
        input_list = list(input_sequence)

    # Check if the list has the expected length
    if len(input_list) != 12:
        # Handle error or return as is, depending on desired behavior
        # For now, let's raise an error for clarity
        raise ValueError("Input sequence must contain exactly 12 integers.")

    # Identify key1 and key2
    key1 = input_list[0]
    key2 = input_list[1]
    target_value = 5

    # Initialize the output list as a copy of the input list
    output_list = list(input_list)

    # Find all runs of the target value (5)
    runs_of_5 = find_runs(input_list, target_value)

    # Replace the first run of 5s with key1, if it exists
    if len(runs_of_5) >= 1:
        start1, len1 = runs_of_5[0]
        for i in range(start1, start1 + len1):
            output_list[i] = key1

    # Replace the second run of 5s with key2, if it exists
    if len(runs_of_5) >= 2:
        start2, len2 = runs_of_5[1]
        for i in range(start2, start2 + len2):
            output_list[i] = key2

    # Return the modified output sequence
    return output_list