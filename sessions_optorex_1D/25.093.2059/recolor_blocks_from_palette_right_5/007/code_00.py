import collections
import numpy as np
from typing import List, Tuple, Sequence, Union

"""
Transforms a sequence of 12 integers based on the following rules:
1. Accept the input as a sequence (list or array) of 12 integers.
2. Identify the integer at index 0 as key1 and the integer at index 1 as key2. Define the target_value as 5.
3. Initialize an output_sequence as a copy of the input_sequence.
4. Find all contiguous subsequences (runs) within the input_sequence consisting solely of the target_value (5), where the starting index of the run is 2 or greater. Store these runs (e.g., as pairs of start index and length) in the order they appear. Let's call this list candidate_runs.
5. Check if candidate_runs contains at least one run AND if key1 is not equal to target_value. If both conditions are true:
    * Get the start index and length of the *first* run in candidate_runs.
    * In the output_sequence, replace the elements from that start index for that length with the value key1.
6. Check if candidate_runs contains at least two runs AND if key2 is not equal to target_value. If both conditions are true:
    * Get the start index and length of the *second* run in candidate_runs.
    * In the output_sequence, replace the elements from that start index for that length with the value key2.
7. Return the output_sequence.
"""

def find_runs(sequence: List[int], value: int, start_scan_index: int) -> List[Tuple[int, int]]:
    """
    Finds the start index and length of all contiguous runs of a specific value,
    starting the scan from a given index. Indices returned are relative to the
    original sequence start (index 0).

    Args:
        sequence: The list of integers to search within.
        value: The integer value to find runs of.
        start_scan_index: The index in the sequence to begin scanning from.

    Returns:
        A list of tuples, where each tuple contains (start_index, length)
              for a run of the specified value found at or after start_scan_index.
    """
    runs = []
    i = start_scan_index
    n = len(sequence)
    while i < n:
        if sequence[i] == value:
            run_start_index = i
            # Find the end of the run
            while i < n and sequence[i] == value:
                i += 1
            length = i - run_start_index
            runs.append((run_start_index, length))
        else:
            # Move to the next element if not the target value
            i += 1
    return runs

def transform(input_sequence: Union[List[int], np.ndarray]) -> List[int]:
    """
    Applies the conditional sequence transformation rule.

    Args:
        input_sequence: A sequence (list or numpy array) of 12 integers.

    Returns:
        A list containing the transformed sequence of 12 integers.
    """
    # Ensure input is a list and has the correct length
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assuming it's already list-like if not ndarray
        input_list = list(input_sequence)

    if len(input_list) != 12:
        raise ValueError("Input sequence must contain exactly 12 integers.")

    # Step 2: Identify keys and target value.
    key1 = input_list[0]
    key2 = input_list[1]
    target_value = 5

    # Step 3: Initialize output_sequence as a copy.
    output_list = list(input_list)

    # Step 4: Find candidate runs (runs of 5 starting at index 2 or later).
    candidate_runs = find_runs(input_list, target_value, start_scan_index=2)

    # Step 5: Conditionally replace the first candidate run.
    if len(candidate_runs) >= 1 and key1 != target_value:
        start_idx, length = candidate_runs[0]
        # Replace elements in the output list
        for i in range(start_idx, start_idx + length):
            output_list[i] = key1

    # Step 6: Conditionally replace the second candidate run.
    if len(candidate_runs) >= 2 and key2 != target_value:
        start_idx, length = candidate_runs[1]
        # Replace elements in the output list
        for i in range(start_idx, start_idx + length):
            output_list[i] = key2

    # Step 7: Return the modified output sequence.
    return output_list