import numpy as np
from collections import namedtuple

"""
Identifies and isolates the longest contiguous sequence (run) of a single 
non-zero digit within an input sequence of digits. If multiple runs share 
the maximum length, the one appearing earliest (smallest start index) is chosen. 
The output sequence retains only the digits from this chosen run in their 
original positions, with all other positions set to zero. The output sequence
has the same length as the input sequence.
"""

# Define a structure to hold information about a run
RunInfo = namedtuple("RunInfo", ["digit", "start", "end", "length"])

def find_runs(digit_sequence):
    """
    Scans the input sequence to identify all contiguous runs of non-zero digits.

    Args:
        digit_sequence: A list or NumPy array of integers.

    Returns:
        A list of RunInfo objects, each describing a contiguous run.
    """
    runs = []
    if len(digit_sequence) == 0:
        return runs

    current_run_digit = None
    current_run_start = -1

    # Iterate through the sequence with index
    for i, digit in enumerate(digit_sequence):
        # Convert potential numpy types to standard int for comparison
        current_digit_int = int(digit) 
        
        if current_digit_int != 0:
            # Check if we are continuing a run or starting a new one
            if current_digit_int == current_run_digit:
                # Continue existing run - no action needed here
                pass
            else:
                # End previous run if one exists
                if current_run_digit is not None:
                    runs.append(RunInfo(current_run_digit, current_run_start, i - 1, i - current_run_start))
                
                # Start a new run
                current_run_digit = current_digit_int
                current_run_start = i
        else:
            # Current digit is zero, end any active run
            if current_run_digit is not None:
                runs.append(RunInfo(current_run_digit, current_run_start, i - 1, i - current_run_start))
            
            # Reset run tracking
            current_run_digit = None
            current_run_start = -1

    # After the loop, check if a run was active at the end of the sequence
    if current_run_digit is not None:
        runs.append(RunInfo(current_run_digit, current_run_start, len(digit_sequence) - 1, len(digit_sequence) - current_run_start))

    return runs

def find_longest_run(runs):
    """
    Determines the run with the maximum length from a list of runs.
    If multiple runs share the maximum length, selects the one with the 
    smallest start index.

    Args:
        runs: A list of RunInfo objects.

    Returns:
        The selected RunInfo object representing the target run, 
        or None if the input list of runs is empty.
    """
    if not runs:
        return None

    # Find the maximum length among all runs
    max_length = 0
    for run in runs:
        if run.length > max_length:
            max_length = run.length

    # Filter runs to keep only those with the maximum length
    longest_runs = [run for run in runs if run.length == max_length]

    # If there's only one longest run, it's the target
    if len(longest_runs) == 1:
        return longest_runs[0]

    # If there are multiple runs with the same max length, find the earliest one
    best_run = longest_runs[0]
    for run in longest_runs[1:]:
        if run.start < best_run.start:
            best_run = run

    return best_run


def transform(input_sequence):
    """
    Transforms an input sequence of digits based on the longest run rule.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A NumPy array of integers representing the transformed sequence.
    """
    # Ensure input is treated as a sequence (handles lists and numpy arrays)
    sequence = np.array(input_sequence) 
    n = len(sequence)

    # Initialize the output sequence with zeros, matching input length and type
    output_sequence = np.zeros_like(sequence)

    # Find all contiguous runs of non-zero digits in the input
    runs = find_runs(sequence)

    # Determine the target run (longest, then earliest)
    target_run = find_longest_run(runs)

    # If a target run was identified, populate the output sequence
    if target_run:
        # Iterate through the indices covered by the target run
        for i in range(target_run.start, target_run.end + 1):
            # Set the corresponding elements in the output sequence to the run's digit
            output_sequence[i] = target_run.digit

    # Return the resulting sequence
    return output_sequence