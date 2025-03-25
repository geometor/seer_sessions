"""
Iterate through the input sequence, identifying runs of consecutive, identical digits.
Remove runs of length 1 that are bounded by zeros.
Keep runs of zeros.
Keep runs that are not bounded by zeros, or have lengths > 1
"""

import numpy as np

def find_runs(input_grid):
    """
    Finds runs of consecutive identical digits in a 1D array.
    Returns a list of tuples: (value, start_index, end_index, length).
    """
    runs = []
    if not input_grid:
        return runs

    current_value = input_grid[0]
    start_index = 0
    for i in range(1, len(input_grid)):
        if input_grid[i] != current_value:
            runs.append((current_value, start_index, i - 1, i - start_index))
            current_value = input_grid[i]
            start_index = i
    runs.append((current_value, start_index, len(input_grid) - 1, len(input_grid) - start_index))
    return runs

def is_bounded_by_zeros(run, input_grid):
    """
    Checks if a run is bounded by zeros or the start/end of the sequence.
    """
    value, start_index, end_index, _ = run
    if value == 0:
        return False  # Zero runs are handled separately

    before = start_index == 0 or input_grid[start_index - 1] == 0
    after = end_index == len(input_grid) - 1 or input_grid[end_index + 1] == 0
    return before and after

def transform(input_grid):
    """
    Transforms the input grid by removing runs of non-zero digits with
    length one, that are bounded by zero
    """
    runs = find_runs(input_grid)
    output_grid = []

    for run in runs:
        value, start_index, end_index, length = run

        # Keep runs of zeros
        if value == 0:
            output_grid.extend([value] * length)
            continue

        # Remove runs of length 1 bounded by zeros
        if is_bounded_by_zeros(run, input_grid) and length == 1:
            continue

        # keep everything else
        output_grid.extend([value] * length)

    return output_grid