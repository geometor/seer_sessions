```python
import numpy as np
from typing import List, Dict, Any, Union

"""
Transforms a one-dimensional sequence (list or array) of single-digit integers based on the following rule:
1.  Scan the input sequence from left to right to identify all contiguous runs (subsequences) composed of identical non-zero digits. For each run found, record its starting index, its length, and the digit it consists of. Ignore zeros when identifying runs.
2.  If no non-zero runs are identified, return the original input sequence unchanged.
3.  If one or more runs were identified, determine the maximum length among all found runs.
4.  Select the run that has this maximum length. If multiple runs share the maximum length, select the one that occurs earliest in the sequence (i.e., the one with the smallest starting index).
5.  Create a new sequence by copying the input sequence.
6.  Modify the new sequence by replacing the digits at the indices corresponding to the selected run (from its starting index up to its starting index plus its length minus one) with the digit '1'.
7.  Return the modified sequence.
"""

def _find_runs(sequence: np.ndarray) -> List[Dict[str, int]]:
    """
    Helper function to identify all contiguous runs of identical non-zero digits.

    Args:
        sequence: A 1D NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a run
        and contains 'start' (index), 'length', and 'value' (the digit).
        Returns an empty list if no non-zero runs are found.
    """
    runs = []
    n = len(sequence)
    i = 0
    while i < n:
        # Skip zeros
        if sequence[i] == 0:
            i += 1
            continue

        # Found the start of a potential non-zero run
        current_digit = sequence[i]
        start_index = i
        run_length = 1
        i += 1 # Move to the next potential element of the run

        # Extend the run while the digit matches and within bounds
        while i < n and sequence[i] == current_digit:
            run_length += 1
            i += 1

        # Store the found run
        runs.append({'start': start_index, 'length': run_length, 'value': current_digit})
        # The outer loop continues from the current 'i', which is now
        # positioned after the identified run or past the end of the sequence.

    return runs

def transform(input_sequence: Union[List[int], np.ndarray]) -> np.ndarray:
    """
    Applies the transformation rule to find the longest run of identical non-zero
    digits (leftmost in case of tie) and replaces it with ones.

    Args:
        input_sequence: The list or NumPy array of integers to transform.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Ensure input is a 1D NumPy array and create a copy for the output
    # Assuming the input is always fundamentally 1D, even if wrapped in a list
    if isinstance(input_sequence, list) and len(input_sequence) > 0 and isinstance(input_sequence[0], list):
         # Handle potential nested list input like [[...]] by taking the first element
         arr = np.array(input_sequence[0], dtype=int)
    else:
         arr = np.array(input_sequence, dtype=int)
         
    if arr.ndim > 1:
        # If somehow still multidimensional, flatten it
        arr = arr.flatten()

    output_arr = arr.copy()

    # 1. Find all contiguous runs of identical non-zero digits
    runs = _find_runs(arr)

    # 2. If no non-zero runs are found, return the original array
    if not runs:
        return output_arr # Return the copy

    # 3. Determine the maximum length among the runs
    max_length = 0
    for run in runs:
        max_length = max(max_length, run['length'])

    # 4. Select the first (leftmost) run that has the maximum length
    selected_run = None
    for run in runs:
        if run['length'] == max_length:
            selected_run = run
            break # Found the leftmost longest run, stop searching

    # Defensive check (should always find a run if 'runs' is not empty)
    if selected_run is None:
         return output_arr

    # 5. & 6. Modify the output array: replace the selected run with '1's
    start_index = selected_run['start']
    run_length = selected_run['length']
    # Use array slicing for efficient replacement
    output_arr[start_index : start_index + run_length] = 1

    # 7. Return the modified sequence
    return output_arr
```