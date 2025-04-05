import numpy as np
import math

"""
Transforms a 1D sequence of 0s and 2s based on contiguous runs of 2s.
Specifically, identifies runs of '2's that end either at the sequence boundary
or immediately before a '0'. For such runs, the last floor(L/2) elements
(where L is the length of the run) are changed from '2' to '8'.
Zeros remain unchanged. Assumes input might be a 2D numpy array with one row,
flattens it to 1D for processing.
"""

def find_runs_of_twos(sequence):
    """
    Identifies contiguous runs of the number 2 in a 1D sequence.

    Args:
        sequence: A 1D list or numpy array of integers.

    Returns:
        A list of tuples, where each tuple represents a run
        (start_index, end_index, length).
    """
    runs = []
    n = len(sequence)
    i = 0
    while i < n:
        # Check if the current element is 2
        if sequence[i] == 2:
            start_index = i
            # Find the end of the run of 2s
            while i < n and sequence[i] == 2:
                i += 1
            end_index = i - 1
            length = end_index - start_index + 1
            # Record the run details
            runs.append((start_index, end_index, length))
        else:
            # Move to the next element if it's not 2
            i += 1
    return runs

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (sequence).

    Args:
        input_grid: A 1D or 2D numpy array containing the sequence of 0s and 2s.
                   If 2D, assumes shape (1, N) and flattens.

    Returns:
        A 1D numpy array representing the transformed sequence (0s, 2s, and 8s).
    """
    # Ensure input is a NumPy array and handle potential 2D shape (e.g., (1, N))
    if not isinstance(input_grid, np.ndarray):
        input_sequence = np.array(input_grid)
    else:
        input_sequence = input_grid

    # Store original shape if needed for reshaping output, although 1D is often expected
    original_shape = input_sequence.shape
    if input_sequence.ndim > 1:
       # Flatten the array, assuming it's like [[...]]
       input_sequence = input_sequence.flatten()


    # 1. Create a mutable copy of the (flattened) input sequence.
    output_sequence = np.copy(input_sequence)
    n = len(input_sequence)

    # 2. Identify all contiguous runs of the value `2`.
    # Use the helper function to get runs as (start, end, length) tuples.
    runs = find_runs_of_twos(input_sequence)

    # 3. Iterate through each identified run of `2`s.
    for start, end, length in runs:
        
        # 4. Check if the run satisfies the termination condition.
        #    A run qualifies if it ends at the sequence end OR the next element is 0.
        terminates_correctly = False
        if end == n - 1:  # Condition i: Run ends at the last index
            terminates_correctly = True
        elif end + 1 < n and input_sequence[end + 1] == 0: # Condition ii: Element after run exists and is 0
            terminates_correctly = True

        # 5. If the termination condition is met, apply the change.
        if terminates_correctly:
            # Calculate the number of elements to change: floor(length / 2).
            num_changes = length // 2 # Integer division automatically floors

            # If there are elements to change (run length >= 2)
            if num_changes > 0:
                # Iterate through the indices of the last 'num_changes' elements of the run.
                # The range starts from (end - num_changes + 1) up to 'end' inclusive.
                for i in range(end - num_changes + 1, end + 1):
                    # Change the value in the output_sequence at index `i` to `8`.
                    output_sequence[i] = 8

    # 6. Return the modified output sequence.
    # The output is kept as a 1D array as the core logic operates on the sequence.
    # Reshaping back to original_shape could be done here if strictly required by the environment,
    # but often ARC tasks accept flattened output for 1D sequence tasks.
    # Example: return output_sequence.reshape(original_shape) # Uncomment if needed
    return output_sequence