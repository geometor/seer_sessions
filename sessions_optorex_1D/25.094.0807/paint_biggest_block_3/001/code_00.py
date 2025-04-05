import math
from typing import List, Tuple, Optional

"""
Modify a sequence of digits by replacing the first occurring longest contiguous run of identical non-zero digits with 1s.
"""

def find_runs(sequence: List[int]) -> List[Tuple[int, int, int]]:
    """
    Identifies all contiguous runs of identical non-zero digits in the sequence.

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

    for i, digit in enumerate(sequence):
        if digit != 0:
            # Start of a new run or continuation of the current one
            if current_run_length == 0:
                # Start a new run
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
            elif digit == current_run_value:
                # Continue the current run
                current_run_length += 1
            else:
                # End the previous run and start a new one
                runs.append((current_run_start, current_run_length, current_run_value))
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
        else:
            # Digit is 0, end any current run
            if current_run_length > 0:
                runs.append((current_run_start, current_run_length, current_run_value))
            # Reset run tracking
            current_run_start = -1
            current_run_length = 0
            current_run_value = None

    # Add the last run if the sequence doesn't end with 0
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
        return None

    # Find the maximum length
    max_length = 0
    for _, length, _ in runs:
        if length > max_length:
            max_length = length

    # Filter runs with maximum length
    longest_runs = [run for run in runs if run[1] == max_length]

    # Find the run with the minimum start index among the longest ones
    target_run = min(longest_runs, key=lambda run: run[0])

    return target_run


def transform(input_str: str) -> str:
    """
    Transforms the input string sequence according to the specified rule:
    1. Parse the input string into a list of integers.
    2. Find all contiguous runs of identical non-zero digits.
    3. Identify the first occurring longest run.
    4. Replace the digits in that run with 1s.
    5. Format the modified list back into a space-separated string.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string representing the transformed sequence.
    """
    # 1. Parse input string into a list of integers
    input_sequence = [int(d) for d in input_str.split()]
    
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)

    # 2. Find all contiguous runs of identical non-zero digits
    runs = find_runs(input_sequence)

    # 3. Select the target run (first longest)
    target_run = select_target_run(runs)

    # 4. If a target run exists, replace its elements with 1s in the output sequence
    if target_run:
        start_index, length, _ = target_run
        replacement_digit = 1
        for i in range(start_index, start_index + length):
            output_sequence[i] = replacement_digit

    # 5. Format the modified list back into a space-separated string
    output_str = " ".join(map(str, output_sequence))
    
    return output_str
