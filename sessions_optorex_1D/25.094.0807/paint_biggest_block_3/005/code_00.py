import numpy as np
from typing import List, Tuple, Optional, Sequence

"""
Modify a sequence of digits represented as a NumPy array by:
1. Identifying all contiguous runs of identical non-zero digits.
2. Finding the maximum length among these runs.
3. Selecting the run(s) with this maximum length.
4. Among the longest runs, choosing the one that appears first (minimum start index).
5. Replacing the digits within this chosen run with the digit 1.
Return the modified sequence as a NumPy array.
"""

def find_runs(sequence: List[int]) -> List[Tuple[int, int, int]]:
    """
    Identifies all contiguous runs of identical non-zero digits in a list.

    Args:
        sequence: A list of integers.

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

    # Iterate through the list to find runs
    for i, digit in enumerate(sequence):
        if digit != 0: # Check if the digit is non-zero
            # Non-zero digit encountered
            if current_run_length == 0:
                # Start a new run
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
            elif digit == current_run_value:
                # Continue the current run if the digit matches
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
        The target run tuple (start_index, length, value), or None if no runs exist.
    """
    if not runs:
        # No non-zero runs found
        return None

    # Find the maximum length among all identified runs
    max_length = 0
    for _, length, _ in runs:
        if length > max_length:
            max_length = length
    
    # Filter the runs to keep only those with the maximum length
    longest_runs = [run for run in runs if run[1] == max_length]

    # From the longest runs, find the one that starts earliest (minimum start_index)
    # The min function with a key naturally handles finding the first one in case of ties
    target_run = min(longest_runs, key=lambda run: run[0])

    return target_run

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array according to the specified rule.
    """
    # Convert input NumPy array to a Python list for easier processing
    input_list = input_grid.tolist()

    # Initialize output list as a copy of the input list
    output_list = list(input_list)

    # Find all contiguous runs of identical non-zero digits in the list
    runs = find_runs(input_list)

    # Select the target run (first occurring longest run)
    target_run = select_target_run(runs)

    # If a target run was identified, modify the output list
    if target_run:
        start_index, length, _ = target_run
        replacement_digit = 1
        # Iterate through the indices of the target run in the output list
        for i in range(start_index, start_index + length):
            # Replace the digit at the current index with 1
            output_list[i] = replacement_digit

    # Convert the modified output list back to a NumPy array
    output_grid = np.array(output_list, dtype=input_grid.dtype)

    return output_grid