import math
from typing import List, Tuple, Optional, Sequence, MutableSequence

"""
Modify a sequence of digits by replacing the first occurring longest contiguous run of identical non-zero digits with 1s.
"""

def find_runs(sequence: Sequence[int]) -> List[Tuple[int, int, int]]:
    """
    Identifies all contiguous runs of identical non-zero digits in the sequence.

    Args:
        sequence: A sequence (list or tuple) of integers.

    Returns:
        A list of tuples, where each tuple represents a run:
        (start_index, length, value). Returns an empty list if no runs are found.
    """
    runs = []
    if not sequence:
        return runs

    current_run_start = -1
    current_run_length = 0
    current_run_value = None

    for i, digit in enumerate(sequence):
        if digit != 0:
            # Non-zero digit encountered
            if current_run_length == 0:
                # Start a new run
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
            elif digit == current_run_value:
                # Continue the current run
                current_run_length += 1
            else:
                # End the previous run (different non-zero digit) and start a new one
                runs.append((current_run_start, current_run_length, current_run_value))
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
        else:
            # Zero encountered, end any current run
            if current_run_length > 0:
                runs.append((current_run_start, current_run_length, current_run_value))
            # Reset run tracking
            current_run_start = -1
            current_run_length = 0
            current_run_value = None

    # Add the last run if the sequence doesn't end with 0 and a run was active
    if current_run_length > 0:
        runs.append((current_run_start, current_run_length, current_run_value))

    return runs

def select_target_run(runs: List[Tuple[int, int, int]]) -> Optional[Tuple[int, int, int]]:
    """
    Selects the target run based on maximum length and earliest start index.

    Args:
        runs: A list of runs, each represented as (start_index, length, value).

    Returns:
        The target run tuple (start_index, length, value), or None if the input list is empty.
    """
    if not runs:
        # No non-zero runs found
        return None

    # Find the maximum length among all runs
    max_length = 0
    for _, length, _ in runs:
        if length > max_length:
            max_length = length
            
    # Alternative using max() if runs is not empty
    # max_length = max(run[1] for run in runs)


    # Filter the runs to keep only those with the maximum length
    longest_runs = [run for run in runs if run[1] == max_length]

    # From the longest runs, find the one that starts earliest (minimum start_index)
    # The min function with a key naturally handles finding the first one in case of ties in length
    # because it iterates sequentially.
    target_run = min(longest_runs, key=lambda run: run[0])

    return target_run


def transform(input_sequence: Sequence[int]) -> MutableSequence[int]:
    """
    Transforms the input sequence according to the specified rule:
    1. Find all contiguous runs of identical non-zero digits.
    2. Identify the first occurring longest run among them.
    3. Replace the digits in that specific run with 1s.
    4. Return the modified sequence.

    Args:
        input_sequence: A sequence (e.g., list or numpy array) of integers.

    Returns:
        A new list representing the transformed sequence.
    """
    # Initialize output_sequence as a mutable copy (list) of the input
    # This ensures the original input sequence is not modified.
    output_sequence = list(input_sequence)

    # Find all contiguous runs of identical non-zero digits
    runs = find_runs(input_sequence)

    # Select the target run (first longest)
    target_run = select_target_run(runs)

    # If a target run was identified, modify the output sequence
    if target_run:
        start_index, length, _ = target_run
        replacement_digit = 1
        # Iterate through the indices of the target run in the output sequence
        for i in range(start_index, start_index + length):
            # Replace the digit at the current index with 1
            output_sequence[i] = replacement_digit

    # Return the modified sequence
    return output_sequence